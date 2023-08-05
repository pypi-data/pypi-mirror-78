"""test_pt.py: script to run pytorch utilities."""

import torch
import torch.nn.functional as F

from shinyutils import shiny_arg_parser
from shinyutils.pt import FCNet, NNTrainer, PTOpt

FCNet.add_parser_args(shiny_arg_parser, "test", "fcnet")
PTOpt.add_parser_args(shiny_arg_parser, "test", "ptopt")
shiny_arg_parser.add_argument("--n-samples", type=int, default=1000)
shiny_arg_parser.add_argument("--batch-size", type=int, default=8)
shiny_arg_parser.add_argument("--train-iters", type=int, default=100)
args = shiny_arg_parser.parse_args()

fcnet = FCNet.from_args(args, "test")
print(fcnet)

ptopt = PTOpt.from_args(fcnet.parameters(), args, "test")
print(ptopt)

X = torch.rand(args.n_samples, args.test_fcnet_indim)
Y = torch.rand(args.n_samples, args.test_fcnet_outdim)

nntrainer = NNTrainer(args.batch_size)
nntrainer.set_dataset((X, Y))
nntrainer.train(fcnet, ptopt, F.mse_loss, args.train_iters)
