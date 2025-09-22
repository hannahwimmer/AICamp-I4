from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
from moviepy import VideoFileClip
from faster_whisper import WhisperModel
import subprocess
import os
from ollama import chat, ChatResponse



def detect_scenes(video_path: str = "data/example_video.mp4", threshold: float = 27.0) -> list[tuple[float, float]]:
    """
    Erkennung von Szenen in einem angegebenen Video. Parameter:
    video_path: Pfad zum Video
    threshold: PySceneDetect vergleicht Histogramme aufeinanderfolgender Frames
    
    Wenn der Unterschied zwischen zwei Frames den festgelegten Schwellenwert überschreitet, 
    wird eine Szenengrenze angenommen.
    """

    # Szene-Manager des scenedetect-Pakets einrichten
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))

    # Video öffnen und vom Manager analysieren lassen
    video = open_video(video_path)
    scene_manager.detect_scenes(video)

    # Liste der Szenen-Zeitstempel (Tupel aus Start- und Endzeit) in Sekunden abrufen
    scene_list = scene_manager.get_scene_list()
    scene_times = [(start.get_seconds(), end.get_seconds()) for start, end in scene_list]

    return scene_times



def cut_scenes(
    scene_list: list[tuple[float, float]], 
    video_path: str = "data/example_video.mp4",
    output_dir: str = "temp/scenes") -> str:
    """
    Schneidet ein gegebenes Video in Segmente entsprechend definierter Szenengrenzen. Parameter:
    video_path: Pfad zum Video
    scenes: Liste von (start_time, end_time)-Tupeln
    output_dir: Pfad zum Speichern der Videosegmente
    """
    # Falls das Ausgabeverzeichnis nicht existiert, wird es erstellt
    os.makedirs(output_dir, exist_ok=True)

    # Das komplette Video als MoviePy VideoFileClip-Objekt laden
    clip = VideoFileClip(video_path)

    for idx, (start_time, end_time) in enumerate(scene_list):

        # Relevanten Teil des Videos extrahieren
        subclip = clip.subclipped(start_time, end_time)

        # In den angegebenen Ausgabeordner schreiben. Hinweis:
        # H.264: Videokompressionsstandard
        # AAC: Advanced Audio Coding, verlustbehafteter Audiocodec
        out_path = os.path.join(output_dir, f"scene_{idx+1}.mp4")
        subclip.write_videofile(out_path, codec="libx264", audio_codec="aac")   

    clip.close()
    return output_dir



def transcribe_scenes(
    scenes_dir: str = "temp/scenes", 
    output_dir: str = "temp/transcripts"):
    """
    Transkribiere alle Szenenvideodateien im Verzeichnis scenes_dir mit Whisper.
    scenes_dir: Verzeichnis der Szenenvideos
    model_name: Name des verwendeten Whisper-Modells ('tiny', 'base', ...)
    """

    model = WhisperModel("tiny", device="cpu")
    os.makedirs(output_dir, exist_ok=True)

    # Alle Dateien im Verzeichnis scenes_dir durchlaufen
    for file_name in sorted(os.listdir(scenes_dir)):

        # Prüfen, ob es sich bei der Datei um eine Videodatei handelt
        if file_name.lower().endswith((".mp4", ".mov", ".mkv", ".avi")):

            # Die jeweilige Szene laden und transkribieren
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

    # Definiere eine Eingabeaufforderung (Prompt) für das LLM
    prompt = f"""Summarize the following text. Do not verify facts, and do not add
        commentary. Only output a concise summary in five sentences maximum. """
    
    # Alle Dateien im Verzeichnis transcripts_dir durchlaufen
    for file_name in sorted(os.listdir(transcripts_dir)):

        # Prüfen, ob es sich bei der Datei um eine .txt-Datei handelt
        if file_name.lower().endswith(".txt"):

            # Das jeweilige Transkript laden und den Text extrahieren
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