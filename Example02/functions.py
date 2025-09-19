import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort
from ultralytics import YOLO
import pandas as pd
import os


def fetch_video(video_path: str):
    return video_path


def load_model(model_name: str):
    return YOLO(model_name)


def track_objects(video_path, model):
    video = cv2.VideoCapture(video_path)
    tracker = DeepSort(max_age=30)

    # init dataframe and frame counter
    columns = ["frame", "track_id", "x_center", "y_center"]
    df_tracks = pd.DataFrame(columns=columns)
    frame_idx = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # YOLO detections
        results = model(frame_rgb)
        boxes = results[0].boxes.xyxy.cpu().numpy()
        scores = results[0].boxes.conf.cpu().numpy()

        detections = []
        for box, score in zip(boxes, scores):
            x1, y1, x2, y2 = box
            width = x2 - x1
            height = y2 - y1
            detections.append([[x1, y1, width, height], float(score)])

        # DeepSORT update
        tracks = tracker.update_tracks(detections, frame=frame_rgb)
        for track in tracks:
            if not track.is_confirmed() or track.original_ltwh is None:
                continue

            x1, y1, width, height = track.original_ltwh
            track_id = track.track_id
            x_center = x1 + width / 2
            y_center = y1 + height / 2

            df_tracks = pd.concat([df_tracks, pd.DataFrame([{
                "frame": frame_idx,
                "track_id": track_id,
                "x_center": x_center,
                "y_center": y_center
            }])], ignore_index=True)

        frame_idx += 1

    video.release()
    df_tracks = df_tracks.astype({"frame": int, "track_id": int})
    df_tracks.reset_index(drop=True, inplace=True)
    return df_tracks


def save_dataframe(dataframe: pd.DataFrame, filename: str, output_dir: str = "data/results"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    save_path = os.path.join(output_dir, filename)
    dataframe.to_csv(save_path, index=False)
    return save_path
