import pandas as pd
from dagster import asset
from functions import fetch_video, load_model, track_objects, save_dataframe
import time

@asset(
    description="Loads a specified video file",
    group_name="extraction"
)
def load_video():
    video_path = "data/flamingo.mp4"
    return fetch_video(video_path)


@asset(
    description="Fetches the specified YOLO model",
    group_name="extraction"
)
def fetch_model():
    model_name = "yolo11n.pt"  # <-- hardcoded YOLO-model we want to use
    return load_model(model_name)


"""
generally: dagster assesses the causal sequence of assets implicitly by forcing us to
name function inputs after other assets.
---------------------
Example: get_object_trajectories(load_video, fetch_model). If we change how the inputs
    are called here, dagster will throw an error because it doesn't know where those
    inputs should come from.
---------------------
if the asset doesn't take an input but STILL depends on another asset, you can declare
the connection EXPLICITLY via the "deps" property of the asset decorator.
--> I put this as a comment in the following as it is not necessary here (our functions
    take inputs, so we have to declare those after assets anyway and dagster will grasp
    the causal order)
"""

@asset(
    # deps=[load_video, fetch_model],   # not necessary to declare again explicitly here
    description="Tracks objects in the video and returns their trajectories",
    group_name="transformation"
)
def get_object_trajectories(load_video, fetch_model) -> pd.DataFrame:
    video = load_video
    model = fetch_model
    return track_objects(video, model)


@asset(
    # deps=[get_object_trajectories],   # not necessary to declare again explicitly here
    description="Saves trajectories to CSV in results folder",
    group_name="loading"
)
def save_tracks(get_object_trajectories) -> str:
    df_tracks = get_object_trajectories
    output_dir = "data/results"
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = f"tracks_{timestr}.csv"
    return save_dataframe(df_tracks, filename, output_dir)
