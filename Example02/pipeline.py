from dagster import Definitions, define_asset_job, ScheduleDefinition, AssetSelection
from assets import load_video, fetch_model, get_object_trajectories, save_tracks

# Job: run all assets
video_job = define_asset_job("video_job", selection=AssetSelection.all())

# Schedule: every 5 minutes
video_schedule = ScheduleDefinition(
    job=video_job,
    cron_schedule="*/5 * * * *",
)

# Dagster definitions
defs = Definitions(
    assets=[load_video, fetch_model, get_object_trajectories, save_tracks],
    jobs=[video_job],
    schedules=[video_schedule],
)
