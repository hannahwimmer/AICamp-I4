from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
from moviepy import VideoFileClip
from faster_whisper import WhisperModel
import subprocess
import os
from ollama import chat, ChatResponse



def detect_scenes(video_path: str = "data/example_video.mp4", threshold: float = 27.0) -> list[tuple[float, float]]:
    """
    Detect scenes in a specified video. Params:
    video_path: the path to the video
    threshold: PyScene Detect compares histograms of consecutive frames
    
    If the difference between two frames exceeds the set threshold, a scene boundary
    is assumed.
    """

    # set up the scene manager of the scenedetect package
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))

    # open and let the manager analyze the video
    video = open_video(video_path)
    scene_manager.detect_scenes(video)

    # get a list of the scene timestamps (tuples of start and end time) in seconds
    scene_list = scene_manager.get_scene_list()
    scene_times = [(start.get_seconds(), end.get_seconds()) for start, end in scene_list]

    return scene_times


def cut_scenes(
    scene_list: list[tuple[float, float]], 
    video_path: str = "data/example_video.mp4",
    output_dir: str = "temp/scenes") -> str:
    """
    Cut a given video into segments according to defined scene boundaries. Params:
    video_path: path to the video
    scenes: list of (start_time, end_time) tuples
    output_dir: path for saving the video segments
    """
    # if the output directory doesn't exist, create it
    os.makedirs(output_dir, exist_ok=True)

    # load the full video into a MoviePy VideoFileClip object
    clip = VideoFileClip(video_path)

    for idx, (start_time, end_time) in enumerate(scene_list):

        # extract relevant portion of the video
        subclip = clip.subclipped(start_time, end_time)

        # write to declarated output path. note:
        # H.264: video compression standard
        # aac: advanced audio coding, lossy audio codec
        out_path = os.path.join(output_dir, f"scene_{idx+1}.mp4")
        subclip.write_videofile(out_path, codec="libx264", audio_codec="aac")   

    clip.close()
    return output_dir



def transcribe_scenes(
    scenes_dir: str = "temp/scenes", 
    output_dir: str = "temp/transcripts"):
    """
    Transcribe all scene video files in scenes_dir using Whisper.
    scenes_dir: directory of the scene videos
    model_name: name of the whisper model used ('tiny', 'base', ...)
    """

    model = WhisperModel("tiny", device="cpu")
    os.makedirs(output_dir, exist_ok=True)

    # look through all the files in scenes_dir
    for file_name in sorted(os.listdir(scenes_dir)):

        # check if the specific file is a video file
        if file_name.lower().endswith((".mp4", ".mov", ".mkv", ".avi")):

            # fetch the specific scene and transcribe
            file_path = os.path.join(scenes_dir, file_name)
            segments, _ = model.transcribe(file_path)
            transcript = "\n".join([segment.text.strip() for segment in segments])

            txt_filename = os.path.splitext(file_name)[0] + ".txt"
            txt_path = os.path.join(output_dir, txt_filename)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(transcript)

    return output_dir

def summarize_transcript(
    transcripts_dir: str = "temp/transcripts", 
    output_dir : str = "temp/transcripts/summaries"):

    os.makedirs(output_dir, exist_ok=True)

    # define a prompt for the LLM
    prompt = f"""Summarize the following text. Do not verify facts, and do not add
        commentary. Only output a concise summary in five sentences maximum. """
    
    # look through all the files in transcripts_dir
    for file_name in sorted(os.listdir(transcripts_dir)):

        # check if the specific file is a .txt file
        if file_name.lower().endswith(".txt"):

            # fetch the specific transcript and extract the text
            file_path = os.path.join(transcripts_dir, file_name)
            with open(file_path, "r", encoding="utf-8") as f:
                transcript = f.read()

            response: ChatResponse = chat(
                model='llama3.2:1b', 
                messages=[{'role': 'user', 'content': prompt + transcript}])
            result = response["message"]["content"]
            txt_filename = os.path.splitext(file_name)[0] + "_summary.txt"
            txt_path = os.path.join(output_dir, txt_filename)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(result)

if __name__ == "__main__":
    summarize_transcript()