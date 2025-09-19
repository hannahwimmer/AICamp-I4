import streamlit as st
from functions import detect_scenes
import pandas as pd

st.title("Segmentation, transcription, and summarization of videos")
st.set_page_config(layout="wide")
tab1, tab2, tab3, tab4 = st.tabs(["Loading a video from a folder", "Segmenting the video", "Transcribing the video", "Summarizing the transcription"])

with tab1:
    st.header("Loading a video from a folder")
    st.markdown("First, we'll load some video from our data folder. We'll use " \
        "`st.video(<video_path>)` to show the video in the web application. That's how it " \
        "looks like in the end:")
    st.video("data/example_video.mp4")


with tab2:
    st.header("Segmenting the video")
    st.markdown("For scene segmentation, we use the `scenedetect` package. This works by " \
    "comparing histograms of consecutive frames against each other. If the difference " \
    "is too large (see parameter `threshold`), the package detects that time point as a " \
    "boundary between two separate scenes. \n" \
    "\n" \
    "Our `detect_scenes` function gives the start and end time point of each scene. In " \
    "the end, we can print the results as a pandas dataframe.")

    segment_video = st.button("Start video segmentation")
    if segment_video:
        with st.spinner("Processing... please wait ⏳"):
            scene_boundaries = pd.DataFrame(detect_scenes(), 
                columns=["start time", "end time"])
            print(scene_boundaries)
            st.dataframe(scene_boundaries)

with tab3:
    st.header("Transcribe the video segments")
    st.markdown("Now we want to have not only the video and audio, but a written " \
        "transcription of what was spoken. For this, we'll use `Whisper`, a model specifically " \
        "designed for automated speech recognition. Let's see how this works for a video " \
    "slice:")


    scene = st.selectbox("Select a scene:", 
        ["Scene 1", "Scene 2", "Scene 3", "Scene 4", "Scene 5", "Scene 6", "Scene 7"])
    scene = "scene_" + scene.split(" ")[1]
    st.video(f"data/scenes_demo/{scene}.mp4")
    with open(f"data/transcripts_demo/{scene}.txt", "r", encoding="utf-8") as f:
        text = f.read()
    st.markdown("**Whisper transcription:**")
    container = st.container(border=True)
    container.markdown(text)

with tab4:
    st.header("Summarize the transcription with an Ollama model")
    st.markdown("Now it might be that the transcription is quite long. Check this scene out, " \
        "for example:")
    st.video("data/scenes_demo/scene_3.mp4")
    st.markdown("Here's Whisper's transcription for that video segment - it's very long, as " \
        "you can see:")
    st.markdown("**Whisper transcription**")
    container = st.container(border=True)
    with open("data/transcripts_demo/scene_3.txt", "r", encoding="utf-8") as f:
        text = f.read()
    text = text.replace("\n", " ") # remove the newlines for better display
    container.text(text)

    st.markdown("It would be super helpful to have a large language model (LLM) summarize " \
        "all of that text for us, don't you think? Let's use the `llama3.2:1b` model " \
        "provided by Ollama. It's about 1.3GB large, has ~1b parameters, and takes a context " \
        "of 128K tokens. Here's what this model returns when asked to summarize the provided " \
        "text in at most five sentences:")
    with open("data/summaries_demo/scene_3_summary.txt", "r", encoding="utf-8") as f:
        text = f.read()
    st.markdown("**Ollama summary:**")
    container = st.container(border=True)
    container.text(f"{text}")

    st.markdown("The model is quite small, so it's no surprise that it fails to comply with " \
        "the >five sentences maximum< requirement. Still, it does quite a good job overall!")