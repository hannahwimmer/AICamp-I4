import streamlit as st
from core.main_form import process_form
from core.main_unstructured_text import process_pdf
import os
import pandas as pd


# Seitenkonfiguration einstellen
st.set_page_config(page_title="PDF Information Extraction", layout="wide")


def display_form_data():
    st.title("Information extraction from a PDF form")
    st.text("This app extracts structured data from a PDF form and displays it.")

    uploaded_file_form = st.file_uploader(
        "Choose a PDF form", type="pdf", key="form_upload"
    )
    if uploaded_file_form is not None:
        form_path = "data/uploaded_form.pdf"
        os.makedirs("data", exist_ok=True)
        with open(form_path, "wb") as f:
            f.write(uploaded_file_form.read())

        if os.path.exists(form_path):
            with st.spinner("Processing form PDF..."):
                process_form(file_name="uploaded_form", save_dir="data/results")
            st.badge("Processing complete! Check the data/results folder for output CSV files.", color="red")

            metadata_path = "data/results/uploaded_form_metadata.csv"
            tabular_path = "data/results/uploaded_form_tabulardata.csv"

            if os.path.exists(metadata_path):
                df_meta = pd.read_csv(metadata_path, header=None, names=["Field", "Value"])
                metadata = dict(zip(df_meta["Field"], df_meta["Value"]))

                st.subheader("Agent Information")
                st.metric(":red[Registered Agent]", metadata.get("Registered Agent", "N/A"), border=True)
                st.metric(":red[Registered Agent ID]", metadata.get("Registered Agent ID", "N/A"), border=True)
                st.metric(":red[Incorporation Date]", metadata.get("Date of Incorporation/Qualiﬁcation", "N/A"), border=True)
                st.metric(":red[Registered Department]", metadata.get("Registered Department", "N/A"), border=True)
                st.metric(":red[Job Title]", metadata.get("Job Title", "N/A"), border=True)

                st.subheader("Company Details")
                st.write("**:red[Corporation Name]**", metadata.get("Corporation Name", "N/A"))
                st.write("**:red[City ZIP County]**", metadata.get("City ZIP County", "N/A"))
                with st.expander("Business Statement"):
                    st.write(metadata.get("Brief statement of type of business of the corporation", ""))

                st.subheader("Report Information")
                st.write("**:red[Reporting Month]**", metadata.get("Reporting Month", "N/A"))
                st.write("**:red[Total Working Hours]**", metadata.get("Total working hours", "N/A"))
                st.write("**:red[File Number]**", metadata.get("File Number", "N/A"))
                with st.expander("Progress Summary"):
                    st.write(metadata.get("Progress summary", ""))

                st.subheader("Work Travel Information")
                st.write("**:red[Business Trips]**", metadata.get("Have there been any business trips", "N/A"))
                st.write("**:red[Destination]**", metadata.get("If yes provide destination and duration", "N/A"))
                st.write("**:red[Reimbursement necessary?]**", metadata.get("Are there additional documents for a reimbursement to consider", "N/A"))

                if os.path.exists("data/results/uploaded_file_tabulardata.csv"):
                    df_tab = pd.read_csv("data/results/uploaded_file_tabulardata.csv")
                    df_tab.drop(columns=["Unnamed: 0"], inplace=True, errors="ignore")
                    st.subheader("Involvement in Projects")
                    st.dataframe(df_tab.reset_index(drop=True))


def display_unstructured_data(summarize: bool = False):
    st.title("Information extraction from a regular PDF")
    st.text("This app extracts structured data from unstructured PDF text and displays it.")

    uploaded_file_text = st.file_uploader("Choose a PDF file", type="pdf", key="text_upload")
    if uploaded_file_text is not None:
        text_path = "data/uploaded_text.pdf"
        with open(text_path, "wb") as f:
            f.write(uploaded_file_text.read())

        if os.path.exists(text_path):
            with st.spinner("Digest PDF..."):
                process_pdf(file_name="uploaded_text", save_dir="data/results", 
                            summarize=summarize)
            st.badge("Processing complete! Check the data/results folder for output CSV files.", color="red")

            csv_path = "data/results/uploaded_text_sections.csv"
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)

                row = df.iloc[0]
                st.header(row["Title"])
                for section in ["Abstract", "Introduction", "Methods", "Discussion", "Conclusion"]:
                    st.subheader(section)
                    st.write(row.get(section, ""))

                if len(df) > 1:
                    summary_row = df.iloc[1]
                    st.subheader("Summaries (generated by LLM)")
                    for section in ["Abstract", "Introduction", "Methods", "Discussion", "Conclusion"]:
                        with st.expander(section + " Summary"):
                            st.markdown(f":red[{summary_row.get(section, '')}]")

                


if __name__ == "__main__":
    tab1, tab2 = st.tabs(["Form Data", "Unstructured Data"])
    with tab1:
        display_form_data()
    with tab2:
        display_unstructured_data(summarize=True)
