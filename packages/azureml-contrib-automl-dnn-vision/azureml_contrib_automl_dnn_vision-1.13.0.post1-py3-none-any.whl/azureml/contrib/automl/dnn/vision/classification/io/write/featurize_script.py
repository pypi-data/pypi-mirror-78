# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Featurize images from model produced by another run."""

from azureml.train.automl import constants
from azureml.contrib.automl.dnn.vision.classification.inference.score import featurize
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.contrib.automl.dnn.vision.common.utils import _safe_exception_logging, _set_logging_parameters
import argparse

logger = get_logger(__name__)


@_safe_exception_logging
def main():
    """Wrapper method to execute script only when called and not when imported."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_id', help='run id of the experiment that generated the model')
    parser.add_argument('--experiment_name', help='experiment that ran the run which generated the model')
    parser.add_argument('--output_file', help='path to output file')
    parser.add_argument('--root_dir', help='path to root dir for files listed in image_list_file')
    parser.add_argument('--image_list_file', help='image files list')
    parser.add_argument('--input_dataset_id', help='input dataset id')

    args, unknown = parser.parse_known_args()

    # Set up logging
    task_type = constants.Tasks.IMAGE_CLASSIFICATION
    _set_logging_parameters(task_type, args)

    # TODO JEDI
    # When we expose the package to customers we need to revisit. We should not log any unknown
    # args when the customers send their hp space.
    if unknown:
        logger.info("Got unknown args, will ignore them: {}".format(unknown))

    featurize(args.run_id, experiment_name=args.experiment_name, output_file=args.output_file,
              root_dir=args.root_dir, image_list_file=args.image_list_file,
              input_dataset_id=args.input_dataset_id)


if __name__ == "__main__":
    # execute only if run as a script
    main()
