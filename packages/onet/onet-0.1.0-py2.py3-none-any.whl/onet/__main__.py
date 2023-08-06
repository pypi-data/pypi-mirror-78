#!/usr/bin/env python3

"""Train and predict procedures for binary image classification."""

import argparse

import onet

parser = argparse.ArgumentParser(description=__doc__)
subparsers = parser.add_subparsers(title="procedures")

train_parser = subparsers.add_parser("train")
train_parser.set_defaults(subcommand="train")
train_parser.add_argument(
    "-o",
    "--output",
    default="model/",
    help="Location to save model.",
)
train_parser.add_argument(
    "-e",
    "--epochs",
    type=int,
    default=onet.DEFAULT_EPOCHS,
    help="Number of epochs for training.",
)
train_parser.add_argument(
    "-b",
    "--batch-size",
    type=int,
    default=onet.DEFAULT_BATCH_SIZE,
    help="Batch size to use for training.",
)
train_parser.add_argument(
    "-m",
    "--base-model",
    choices=onet.BASE_MODELS,
    default=onet.DEFAULT_BASE_MODEL,
    help="Base model for the training.",
)
train_parser.add_argument(
    "-c",
    "--color-mode",
    choices=onet.COLOR_MODES,
    default=onet.DEFAULT_COLOR_MODE,
    help="Color mode of the images.",
)
train_parser.add_argument(
    "directory",
    help=(
        "A directory containing images for training"
        " (one sub-folder per class, only two sub-folders)."
    )
)

predict_parser = subparsers.add_parser("predict")
predict_parser.set_defaults(subcommand="predict")
predict_parser.add_argument(
    "-m",
    "--model",
    default="model/",
    help="Location of the model folder.",
)
predict_parser.add_argument(
    "directory",
    help=(
        "A directory containing images for prediction"
        " (read all images, including in sub-folders)."
    )
)


def train(args: argparse.Namespace):
    """Command for the training."""
    model = onet.train(
        epochs=args.epochs,
        directory=args.directory,
        batch_size=args.batch_size,
        base_model=args.base_model,
        color_mode=args.color_mode,
    )
    model.save(args.output)


def predict(args: argparse.Namespace):
    """Command for the prediction."""
    predictions = onet.predict(
        model=args.model,
        directory=args.directory,
    )

    for path, proba in predictions:
        print(f"{path}\t{proba}")


def main(args: list = None):
    """Entry point of the script."""
    args = parser.parse_args(args)

    if args.subcommand == "train":
        train(args)
    elif args.subcommand == "predict":
        predict(args)
    else:
        raise ValueError(f"Unknown procedure: {args.subcommand}")


if __name__ == "__main__":
    main()
