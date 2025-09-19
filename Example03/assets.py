from dagster import asset, job, reconstructable
from functions import detect_scenes, cut_scenes, transcribe_scenes, summarize_transcript

@asset(
    description="returns directory of full video",
    group_name="extraction"
       )
def upload_video(context) -> str:
    output_dir = "data/example_video.mp4"
    context.log.info(f"Saved video to {output_dir}")
    return output_dir

@asset(
    description="returns tuple list of starting and ending time points per segment",
    deps=[upload_video], group_name="segmentation"
    )
def segment(upload_video: str) -> list[tuple[float, float]]:
    return detect_scenes(video_path=upload_video)

@asset(
    description="returns directory of segmented scenes",
    group_name="segmentation"
    )
def cut(context, segment: list[tuple[float, float]], upload_video: str) -> str:
    output_dir = cut_scenes(scene_list=segment, video_path=upload_video)
    context.log.info(f"Scenes cut into {output_dir}")
    return output_dir

@asset(
    description="returns directory of scene transcriptions",
    group_name="text_extraction"
    )
def transcribe(context, cut: str) -> str:
    output_dir = transcribe_scenes(scenes_dir=cut)
    context.log.info(f"Scenes transcribed into {output_dir}")
    return output_dir

@asset(
    description="returns directory of summarized transcriptions",
    group_name="text_extraction",
    owners=["hannah.wimmer@fh-joanneum.at"])
def summarize(context, transcribe: str) -> None:
    output_dir = summarize_transcript(transcripts_dir=transcribe)
    context.log.info(f"Scenes summarized into {output_dir}")
    return output_dir

@job
def video_processing_pipeline():
    summarize()

if __name__ == "__main__":
    video_processing_pipeline()


reconstructable_foo_job = reconstructable(video_processing_pipeline)