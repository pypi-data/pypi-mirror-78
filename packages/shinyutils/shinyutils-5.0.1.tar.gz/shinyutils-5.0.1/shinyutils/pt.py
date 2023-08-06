"""pt.py: utilities for pytorch."""

try:
    import torch
except ImportError as e:
    e.msg += ": install shinyutils[pytorch]"  # type: ignore
    raise e

import inspect
import logging
from argparse import (
    _ArgumentGroup,
    Action,
    ArgumentParser,
    ArgumentTypeError,
    Namespace,
)
from typing import (
    Any,
    Callable,
    Iterable,
    List,
    Mapping,
    Optional,
    overload,
    Tuple,
    Type,
    Union,
)
from unittest.mock import Mock

# pylint: disable=ungrouped-imports
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
from torch.optim.lr_scheduler import _LRScheduler
from torch.optim.optimizer import Optimizer  # pylint: disable=no-name-in-module
from torch.utils.data import DataLoader, Dataset, TensorDataset
from tqdm import trange

from shinyutils import shiny_arg_parser
from shinyutils.argp import (
    ClassType,
    CommaSeparatedInts,
    KeyValuePairsType,
    OutputDirectoryType,
)
from shinyutils.subcls import get_subclasses

try:
    from torch.utils.tensorboard import SummaryWriter
except ImportError:
    ENABLE_TB = False
    logging.info(
        "tensorboard logging disabled: could not import SummaryWriter: "
        "install tensorboard[python] or shinyutils[pytorch]"
    )
else:
    ENABLE_TB = True

DEFAULT_DEVICE = (
    torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
)


__all__ = ["DEFAULT_DEVICE", "PTOpt", "FCNet", "NNTrainer", "SetTBWriterAction"]


class PTOpt:

    """Wrapper around pytorch optimizer and learning rate scheduler."""

    def __init__(
        self,
        weights: Iterable[torch.Tensor],
        optim_cls: Type[Optimizer],
        optim_params: Mapping[str, Any],
        lr_sched_cls: Optional[Type[_LRScheduler]] = None,
        lr_sched_params: Optional[Mapping[str, Any]] = None,
    ) -> None:
        self.optimizer = optim_cls(weights, **optim_params)
        if lr_sched_cls is None:
            self.lr_sched: Optional[_LRScheduler] = None
        else:
            if lr_sched_params is None:
                lr_sched_params = dict()
            self.lr_sched = lr_sched_cls(self.optimizer, **lr_sched_params)

    def __repr__(self) -> str:
        r = repr(self.optimizer)
        if self.lr_sched is not None:
            r += f"\n{self.lr_sched!r}"
        return r

    def zero_grad(self) -> None:
        self.optimizer.zero_grad()

    def step(self) -> None:
        self.optimizer.step()
        if self.lr_sched is not None:
            self.lr_sched.step()

    @classmethod
    def from_args(
        cls, weights: Iterable[torch.Tensor], args: Namespace, arg_prefix: str = ""
    ) -> "PTOpt":
        if arg_prefix:
            arg_prefix += "_"
        argvars = vars(args)
        if f"{arg_prefix}lr_sched_cls" not in argvars:
            argvars[f"{arg_prefix}lr_sched_cls"] = None
            argvars[f"{arg_prefix}lr_sched_params"] = None
        return cls(
            weights,
            argvars[f"{arg_prefix}optim_cls"],
            argvars[f"{arg_prefix}optim_params"],
            argvars[f"{arg_prefix}lr_sched_cls"],
            argvars[f"{arg_prefix}lr_sched_params"],
        )

    @staticmethod
    def add_parser_args(
        base_parser: Union[ArgumentParser, _ArgumentGroup],
        arg_prefix: str = "",
        group_title: Optional[str] = None,
        default_optim_cls: Optional[Type[Optimizer]] = Adam,
        default_optim_params: Optional[Mapping[str, Any]] = None,
        add_lr_decay: bool = True,
    ) -> Union[ArgumentParser, _ArgumentGroup]:
        """Add options to the base parser for pytorch optimizer and lr scheduling."""
        if arg_prefix:
            arg_prefix += "-"
        if group_title is not None:
            base_parser = base_parser.add_argument_group(group_title)

        base_parser.add_argument(
            f"--{arg_prefix}optim-cls",
            type=ClassType(Optimizer),
            choices=get_subclasses(Optimizer),
            required=default_optim_cls is None,
            default=default_optim_cls,
        )

        if default_optim_params is None:
            default_optim_params = dict()
        base_parser.add_argument(
            f"--{arg_prefix}optim-params",
            type=KeyValuePairsType(),
            default=default_optim_params,
        )

        if not add_lr_decay:
            return base_parser

        base_parser.add_argument(
            f"--{arg_prefix}lr-sched-cls",
            type=ClassType(_LRScheduler),
            choices=get_subclasses(_LRScheduler),
            default=None,
        )

        base_parser.add_argument(
            f"--{arg_prefix}lr-sched-params",
            type=KeyValuePairsType(),
            default=dict(),
        )

        return base_parser

    @staticmethod
    def add_help(
        base_parser: Union[ArgumentParser, _ArgumentGroup],
        group_title: Optional[str] = "pytorch help",
    ) -> None:
        class _ShowHelp(Action):
            def __call__(self, parser, namespace, values, option_string=None):
                cls_name = values.__name__
                cls_sig = inspect.signature(values)
                print(f"{cls_name}{cls_sig}")
                parser.exit()

        if group_title is not None:
            base_parser = base_parser.add_argument_group(group_title)

        base_parser.add_argument(
            "--explain-optimizer",
            type=ClassType(Optimizer),
            action=_ShowHelp,
            help="describe arguments of a torch optimizer",
        )
        base_parser.add_argument(
            "--explain-lr-sched",
            type=ClassType(_LRScheduler),
            action=_ShowHelp,
            help="describe arguments of a torch lr scheduler",
        )


class FCNet(nn.Module):

    """Template for a fully connected network."""

    _ActType = Callable[[torch.Tensor], torch.Tensor]

    def __init__(
        self,
        in_dim: int,
        out_dim: int,
        hidden_sizes: List[int],
        hidden_act: _ActType = F.relu,
        out_act: Optional[_ActType] = None,
    ) -> None:
        super().__init__()
        layer_sizes = [in_dim] + hidden_sizes + [out_dim]
        self.layers = nn.ModuleList(
            [nn.Linear(ls, ls_n) for ls, ls_n in zip(layer_sizes, layer_sizes[1:])]
        )
        self.hidden_act = hidden_act
        self.out_act = out_act

    def __repr__(self) -> str:
        out_act_repr = self.out_act.__name__ if self.out_act is not None else "None"
        return (
            "hidden, output activation: "
            + f"{self.hidden_act.__name__}, {out_act_repr}"
            + f"\n{super().__repr__()}"
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        for layer in self.layers[:-1]:
            x = self.hidden_act(layer(x))
        x = self.layers[-1](x)
        if self.out_act is not None:
            x = self.out_act(x)
        return x

    @classmethod
    def from_args(cls, args: Namespace, arg_prefix: str = ""):
        if arg_prefix:
            arg_prefix += "_"
        argvars = vars(args)
        return cls(
            argvars[f"{arg_prefix}fcnet_indim"],
            argvars[f"{arg_prefix}fcnet_outdim"],
            argvars[f"{arg_prefix}fcnet_hidden_sizes"],
            argvars[f"{arg_prefix}fcnet_hidden_act"],
            argvars[f"{arg_prefix}fcnet_out_act"],
        )

    @staticmethod
    def add_parser_args(
        base_parser: Union[ArgumentParser, _ArgumentGroup],
        arg_prefix: str = "",
        group_title: Optional[str] = None,
        default_indim: Optional[int] = None,
        default_outdim: Optional[int] = None,
        default_hidden_sizes: Optional[int] = None,
        default_hidden_act: Optional[_ActType] = F.relu,
        default_out_act: Optional[_ActType] = None,
    ):
        """Add options to base_parser for building a FCNet object."""

        class _Act:
            metavar = "func"

            def __call__(self, string):
                try:
                    return getattr(F, string)
                except AttributeError:
                    raise ArgumentTypeError(
                        f"invalid activation function: {string}"
                    ) from None

        if arg_prefix:
            arg_prefix += "-"
        if group_title is not None:
            base_parser = base_parser.add_argument_group(group_title)

        base_parser.add_argument(
            f"--{arg_prefix}fcnet-indim",
            type=int,
            required=default_indim is None,
            default=default_indim,
        )
        base_parser.add_argument(
            f"--{arg_prefix}fcnet-outdim",
            type=int,
            required=default_outdim is None,
            default=default_outdim,
        )
        base_parser.add_argument(
            f"--{arg_prefix}fcnet-hidden-sizes",
            type=CommaSeparatedInts(),
            required=default_hidden_sizes is None,
            default=default_hidden_sizes,
        )
        base_parser.add_argument(
            f"--{arg_prefix}fcnet-hidden-act",
            type=_Act(),
            required=default_hidden_act is None,
            default=default_hidden_act,
        )
        base_parser.add_argument(
            f"--{arg_prefix}fcnet-out-act",
            type=_Act(),
            required=False,
            default=default_out_act,
        )


class NNTrainer:
    """Helper class for training a model on a dataset."""

    def __init__(
        self,
        batch_size: int,
        data_load_workers: int = 0,
        shuffle: bool = True,
        pin_memory: bool = True,
        drop_last: bool = True,
        device: torch.device = DEFAULT_DEVICE,
    ) -> None:
        self._batch_size = batch_size
        self._data_load_workers = data_load_workers
        self._shuffle = shuffle
        self._pin_memory = pin_memory
        self._drop_last = drop_last
        self._device: torch.device = device

        self._dataset: Dataset
        self._data_loader: DataLoader

    @overload
    def set_dataset(self, value: Dataset) -> None:
        ...

    @overload
    def set_dataset(self, value: Tuple[torch.Tensor, ...]) -> None:
        ...

    @overload
    def set_dataset(self, value: Tuple[np.ndarray, ...]) -> None:
        ...

    def set_dataset(self, value):
        if isinstance(value, Dataset):
            self._dataset = value
        elif isinstance(value, tuple):
            if isinstance(value[0], np.ndarray):
                value = [torch.from_numpy(val_i) for val_i in value]
            self._dataset = TensorDataset(*value)
        else:
            raise ValueError(f"can't set dataset from type {type(value)}")

        self._data_loader = DataLoader(
            self._dataset,
            self._batch_size,
            self._shuffle,
            num_workers=self._data_load_workers,
            pin_memory=self._pin_memory,
            drop_last=self._drop_last,
        )

    def train(
        self,
        model: nn.Module,
        opt: PTOpt,
        loss_fn: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
        iters: int,
        pbar_desc: str = "Training",
    ):
        if self._dataset is None:
            raise RuntimeError("dataset not set: call set_dataset before train")
        bat_iter = iter(self._data_loader)

        logging.info(f"moving model to {self._device}")
        model = model.to(self._device)

        with trange(iters, desc=pbar_desc) as pbar:
            for _ in pbar:
                try:
                    x_bat, y_bat = next(bat_iter)
                except StopIteration:
                    bat_iter = iter(self._data_loader)
                    x_bat, y_bat = next(bat_iter)
                x_bat, y_bat = x_bat.to(self._device), y_bat.to(self._device)

                yhat_bat = model(x_bat)
                loss = loss_fn(yhat_bat, y_bat)
                pbar.set_postfix(loss=float(loss))

                opt.zero_grad()
                loss.backward()
                opt.step()


class SetTBWriterAction(Action):
    """Set attribute in argparse namespace holding tensorboard writer."""

    attr = "tb_writer"

    def __call__(self, parser, namespace, values, option_strings=None):
        if values is None:
            values = Mock(SummaryWriter)
        else:
            values = SummaryWriter(values)
        setattr(namespace, SetTBWriterAction.attr, values)


def _better_lr_sched_repr(lr_sched: _LRScheduler):
    """Replacement for default __repr__ in _LRScheduler."""
    return (
        lr_sched.__class__.__name__
        + "(\n    "
        + "\n    ".join(
            f"{k}: {v}"
            for k, v in lr_sched.state_dict().items()
            if not k.startswith("_")
        )
        + "\n)"
    )


setattr(_LRScheduler, "__repr__", _better_lr_sched_repr)

PTOpt.add_help(shiny_arg_parser)

if ENABLE_TB:
    shiny_arg_parser.add_argument(
        "--tb-dir",
        type=OutputDirectoryType(),
        help="tensorboard log directory",
        default=None,
        action=SetTBWriterAction,
    )
    shiny_arg_parser.set_defaults(**{SetTBWriterAction.attr: Mock(SummaryWriter)})
