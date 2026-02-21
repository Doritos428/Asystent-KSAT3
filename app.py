import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Asystent KSAT 3 - ELEMENTO", page_icon="🏢")
st.title("Pomoc techniczna KSAT 3")
st.subheader("Cyfrowy Asystent ELEMENTO")
st.info("Witaj! Opisz swój problem z programem, a postaram się pomóc krok po kroku.")

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Błąd konfiguracji: Brak klucza API w Secrets!")

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="TU_WKLEJ_TRESC_Z_PUNKTU_A"
)
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("W czym mogę dzisiaj pomóc?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})