from matlab_cp2tform import get_similarity_transform_for_cv2
import numpy as np
import cv2
from Person import Person


def alignment(src_img, src_pts):
    ref_pts = [
        [30.2946, 51.6963],
        [65.5318, 51.5014],
        [48.0252, 71.7366],
        [33.5493, 92.3655],
        [62.7299, 92.2041],
    ]
    crop_size = (96, 112)
    src_pts = np.array(src_pts).reshape(5, 2)

    s = np.array(src_pts).astype(np.float32)
    r = np.array(ref_pts).astype(np.float32)

    tfm = get_similarity_transform_for_cv2(s, r)
    face_img = cv2.warpAffine(src_img, tfm, crop_size)
    return face_img


def display_results(
    frame, persons, src_size, tracked_person=None, selected_person=None
):
    dst_size = (frame.shape[1], frame.shape[0])
    for p in persons:
        bbox = p.bbox.copy()
        bbox[0] = bbox[0] * dst_size[0] / src_size[0]
        bbox[1] = bbox[1] * dst_size[1] / src_size[1]
        bbox[2] = bbox[2] * dst_size[0] / src_size[0]
        bbox[3] = bbox[3] * dst_size[1] / src_size[1]

        # applying the bounding box to the frame for each person
        cv2.rectangle(
            frame,
            (int(bbox[0]), int(bbox[1])),
            (int(bbox[2]), int(bbox[3])),
            (0, 0, 255),
            2,
        )
        # if the target is set than the similarity is displayed
        if p.similarity != -1:
            xmin, ymin, _, _ = np.int32(bbox)
            cv2.putText(
                frame,
                f"Sim: {p.similarity:.2f}",
                (xmin, ymin - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 255, 0),
                1,
            )
    if selected_person is not None:
        bbox = selected_person.bbox.copy()
        bbox[0] = bbox[0] * dst_size[0] / src_size[0]
        bbox[1] = bbox[1] * dst_size[1] / src_size[1]
        bbox[2] = bbox[2] * dst_size[0] / src_size[0]
        bbox[3] = bbox[3] * dst_size[1] / src_size[1]
        # applying the bounding box to the frame for each person
        cv2.rectangle(
            frame,
            (int(bbox[0]), int(bbox[1])),
            (int(bbox[2]), int(bbox[3])),
            (255, 0, 0),
            2,
        )

    if tracked_person is not None:
        bbox = tracked_person.bbox.copy()
        bbox[0] = bbox[0] * dst_size[0] / src_size[0]
        bbox[1] = bbox[1] * dst_size[1] / src_size[1]
        bbox[2] = bbox[2] * dst_size[0] / src_size[0]
        bbox[3] = bbox[3] * dst_size[1] / src_size[1]
        # applying the bounding box to the frame for each person
        cv2.rectangle(
            frame,
            (int(bbox[0]), int(bbox[1])),
            (int(bbox[2]), int(bbox[3])),
            (0, 255, 0),
            2,
        )

