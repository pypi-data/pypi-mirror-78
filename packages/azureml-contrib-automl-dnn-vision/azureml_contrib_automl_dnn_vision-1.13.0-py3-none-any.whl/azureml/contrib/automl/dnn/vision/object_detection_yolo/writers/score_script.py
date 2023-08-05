# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Score images from model produced by another run."""

import argparse
import logging

from azureml.contrib.automl.dnn.vision.common.utils import _safe_exception_logging, _set_logging_parameters
from azureml.contrib.automl.dnn.vision.object_detection_yolo.common.constants import ScoringParameters, YoloLiterals
from azureml.contrib.automl.dnn.vision.object_detection_yolo.writers.score import score
from azureml.train.automl import constants

logger = logging.getLogger(__name__)


@_safe_exception_logging
def main():
    """Wrapper method to execute script only when called and not when imported."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--run_id', help='run id of the experiment that generated the model')
    parser.add_argument('--experiment_name', help='experiment that ran the run which generated the model')
    parser.add_argument('--output_file', help='path to output file')
    parser.add_argument('--root_dir', help='path to root dir for files listed in image_list_file')
    parser.add_argument('--image_list_file', help='image object detection files list')
    parser.add_argument("--batch_size", type=int, help="batch size for inference",
                        default=ScoringParameters.DEFAULT_SCORING_BATCH_SIZE)
    parser.add_argument('--output_dataset_target_path', help='datastore target path for output dataset files')
    parser.add_argument('--input_dataset_id', help='input dataset id')

    # inference settings
    parser.add_argument("--box_score_thresh", type=float,
                        help="during inference, only return proposals with a score \
                            greater than box_score_thresh. The score is the multiplication of \
                            the objectness score and classification probability",
                        default=ScoringParameters.DEFAULT_BOX_SCORE_THRESH)
    parser.add_argument("--box_iou_thresh", type=float,
                        help="IOU threshold used during inference in nms post processing",
                        default=ScoringParameters.DEFAULT_BOX_IOU_THRESH)

    args, unknown = parser.parse_known_args()

    # Set up logging
    task_type = constants.Tasks.IMAGE_OBJECT_DETECTION
    _set_logging_parameters(task_type, args)

    if unknown:
        logger.info("Got unknown args, will ignore them: {}".format(unknown))

    model_settings = {
        YoloLiterals.BOX_SCORE_THRESH: args.box_score_thresh,
        YoloLiterals.BOX_IOU_THRESH: args.box_iou_thresh
    }

    score(args.run_id, experiment_name=args.experiment_name, output_file=args.output_file,
          root_dir=args.root_dir, image_list_file=args.image_list_file, batch_size=args.batch_size,
          output_dataset_target_path=args.output_dataset_target_path,
          input_dataset_id=args.input_dataset_id, **model_settings)


if __name__ == "__main__":
    # execute only if run as a script
    main()
