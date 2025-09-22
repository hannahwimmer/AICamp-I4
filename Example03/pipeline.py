from dagster import Definitions, load_assets_from_modules, ScheduleDefinition
import assets

all_assets = load_assets_from_modules([assets])
defs = Definitions(
    assets=all_assets,
    jobs=[assets.video_processing_pipeline]
)


""" # für die Planung .... 
five_minute_schedule = ScheduleDefinition(
    job=pipeline.video_processing_pipeline,
    cron_schedule="*/5 * * * *",  # alle 5 Minuten
    name="video_processing_every_5_minutes",
)


defs = Definitions(
    assets=all_assets,
    jobs=[pipeline.video_processing_pipeline],
    schedules=[five_minute_schedule],  # <-- hier den Zeitplan hinzufügen
)


# Cron-Schema:
┌───────────── Minute (0 - 59)
│ ┌───────────── Stunde (0 - 23)
│ │ ┌───────────── Tag des Monats (1 - 31)
│ │ │ ┌───────────── Monat (1 - 12)
│ │ │ │ ┌───────────── Wochentag (0 - 6) (Sonntag=0)
│ │ │ │ │
* * * * *
"""

