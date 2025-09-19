from PyPDF2 import PdfReader
import pandas as pd
import os
import re
from typing import Dict
from ollama import chat, ChatResponse

SECTION_HEADERS = ["Abstract", "Introduction", "Methods", "Discussion", "Conclusion"]

# build a regex pattern to match section headers
SECTION_PATTERN = re.compile("|".join(SECTION_HEADERS))

def extract_data(file_path: str) -> str:
    """Extract all text from a PDF file as a single string."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def clean_text(text: str) -> str:
    # strip text of \n (new lines) to enable saving to CSV
    text = re.sub(r"\n", " ", text)

    # additionally, strip multiple spaces
    text = re.sub(r"\s+", " ", text)
    
    return text.strip()

def transform_data(text: str) -> Dict[str, str]:
    """
    Split text into sections using regex.
    Returns a dict: {section_name: section_text}.
    """
    sections = {}
    # Find all section headers
    matches = list(SECTION_PATTERN.finditer(text))
    
    for i, match in enumerate(matches):
        section_name = match.group(0)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        if i == 0:  # Capture any text before the first section as 'Title'
            title = text[:match.start()].strip()
            if title:
                sections["Title"] = clean_text(title)
        section_text = text[start:end].strip()
        sections[section_name] = clean_text(section_text)
    return pd.DataFrame([sections])


def load_data(df: pd.DataFrame, save_dir: str, file_name: str):
    """Save DataFrame to CSV."""
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, f"{file_name}_sections.csv")
    df.to_csv(path, index=True)
    print(f"Sections saved to: {path}")



def summarize_text(dataframe: pd.DataFrame):

    # define a prompt for the LLM
    prompt = f"""Summarize the following text. Do not verify facts, and do not add
        commentary. Only output a concise summary in five sentences maximum."""
    
    summaries = []
    for col in dataframe.columns:
        text = dataframe[col].iloc[0] 
        response: ChatResponse = chat(
            model='llama3.2:1b', 
            messages=[{'role': 'user', 'content': prompt + text}])
        result = response["message"]["content"]
        while result.startswith("Here is"):
            response: ChatResponse = chat(
                model='llama3.2:1b', 
                messages=[{'role': 'user', 'content': prompt + text}])
            result = response["message"]["content"]
        summaries.append(result)
    
    summary_df = pd.concat([dataframe, pd.DataFrame([summaries], columns=dataframe.columns)], axis=0)
    summary_df.index = ["Original Text", "Summary"]
    return summary_df


def process_pdf(file_name: str, save_dir: str = "data/results", summarize: bool = False):
    file_path = os.path.join("data", f"{file_name}.pdf")
    text = extract_data(file_path)
    sections = transform_data(text)
    summary_df = summarize_text(sections) if summarize else sections
    load_data(summary_df, save_dir, file_name)


if __name__ == "__main__":
    process_pdf("Why Dashboarding is Amazing")
