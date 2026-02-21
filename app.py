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
    model_name='gemini-2.5-flash',
    system_instruction="Jesteś asystentem wsparcia technicznego firmy ELEMENTO. Twoim zadaniem jest pomoc pracownikom przedszkoli w obsłudze programu KSAT 3. Pisz prostym językiem, unikaj żargonu IT (np. zamiast "wyczyść cache", pisz "odśwież stronę przyciskiem F5"). Jeśli rozwiązanie wymaga kliknięcia w menu, opisz to krok po kroku. Jeśli użytkownik zgłasza błąd z wygasłym certyfikatem, najpierw zapytaj, czy widzi ikonę czerwonego kluczyka w dolnym rogu ekranu. Jeśli nie znasz odpowiedzi, poproś o kontakt z serwisem ELEMENTO. Twoim celem jest uspokojenie użytkownika i merytoryczna pomoc. Odmawiaj odpowiedzi na pytania niezwiązane z KSAT 3 (np. przepisy kulinarne)."
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
