from dagster import Definitions, load_assets_from_modules, ScheduleDefinition
import assets

all_assets = load_assets_from_modules([assets])
defs = Definitions(
    assets=all_assets,
    jobs=[assets.video_processing_pipeline]
)


""" # for scheduling .... 
five_minute_schedule = ScheduleDefinition(
    job=pipeline.video_processing_pipeline,
    cron_schedule="*/5 * * * *",  # every 5 minutes
    name="video_processing_every_5_minutes",
)


defs = Definitions(
    assets=all_assets,
    jobs=[pipeline.video_processing_pipeline],
    schedules=[five_minute_schedule],  # <-- add your schedule here
)


# ad cron scheme:
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday=0)
│ │ │ │ │
* * * * *
"""
