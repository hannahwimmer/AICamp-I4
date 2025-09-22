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
Kommentar: Dagster bewertet die kausale Reihenfolge der Assets implizit, indem es uns
dazu zwingt, die Funktionsparameter nach anderen Assets zu benennen.
---------------------
Beispiel: get_object_trajectories(load_video, fetch_model). Wenn wir ändern, wie die
Inputs hier genannt werden, wirft Dagster einen Fehler, weil es nicht weiß, woher diese
Inputs kommen sollen.
---------------------
Wenn ein Asset keinen Input annimmt, aber DENNOCH von einem anderen Asset abhängt, kann
die Verbindung EXPLIZIT über die "deps"-Eigenschaft des Asset-Decorators angegeben werden.
--> Ich habe dies im Folgenden als Kommentar hinzugefügt, da es hier nicht notwendig ist
    (unsere Funktionen nehmen Eingaben, also müssen wir diese sowieso nach den Assets
    deklarieren und Dagster erkennt die kausale Reihenfolge automatisch)
"""

@asset(
    # deps=[load_video, fetch_model],   # muss hier nicht unbedingt explizit deklariert werden (siehe Kommentar)
    description="Tracks objects in the video and returns their trajectories",
    group_name="transformation"
)
def get_object_trajectories(load_video, fetch_model) -> pd.DataFrame:
    video = load_video
    model = fetch_model
    return track_objects(video, model)


@asset(
    # deps=[get_object_trajectories],   # muss hier nicht unbedingt explizit deklariert werden (siehe Kommentar)
    description="Saves trajectories to CSV in results folder",
    group_name="loading"
)
def save_tracks(get_object_trajectories) -> str:
    df_tracks = get_object_trajectories
    output_dir = "data/results"
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = f"tracks_{timestr}.csv"
    return save_dataframe(df_tracks, filename, output_dir)
