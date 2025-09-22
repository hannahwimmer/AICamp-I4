import streamlit as st

st.title("Unsere großartige Web-App!")
st.set_page_config(page_title="Unsere App", layout="wide")

st.header("Abschnitt 1")

st.text("Grüß euch! Hier ist gewöhnlicher Text...")

"Hier kommt noch mehr gewöhnlicher Text..."

st.markdown("""Das ist auch regulärer Text, aber in einer :red[Markdown Umgebung]. So 
    können wir den Text auch :orange[nach Belieben] :blue[formatieren], **sehen Sie**?""")