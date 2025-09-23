from gtts import gTTS
import streamlit as st
import io

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="gTTS Text-to-Speech Converter", layout="centered")

st.title("🗣️ gTTS Text-to-Speech")
st.write("Type or change the text below to generate and play audio.")

# --- Text Input ---
text = st.text_area("Enter your text here:",
                     value="Hello, this is a test using Google Text-to-Speech!",
                     height=150,
                     key="user_text_input")

# --- Language Selection (Optional but good practice for gTTS) ---
# You can make this a user-selectable dropdown if needed
lang = st.selectbox("Select Language:",
                    options=['en', 'te', 'hi', 'fr', 'es'], # Example languages
                    index=0, # Default to English
                    format_func=lambda x: {'en': 'English', 'te': 'Telugu', 'hi': 'Hindi', 'fr': 'French', 'es': 'Spanish'}.get(x, x),
                    key='language_selector')

# --- Generate and Play Audio Logic ---
# This block runs whenever the script reruns (e.g., text input changes, or button is clicked)
if text: # Only proceed if there's text input
    # Display a loading message while audio is generated
    with st.spinner(f"Generating audio for '{lang}'..."):
        try:
            # Create a gTTS object
            # Pass the text and selected language
            tts = gTTS(text, lang=lang, tld='com')

            # Save the audio to an in-memory BytesIO object
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0) # Rewind the buffer to the beginning

            st.success("Audio generated successfully!")

            # Play the audio in Streamlit
            st.audio(audio_buffer.read(), format='audio/mp3', start_time=0, autoplay=True)

            # Provide a download button
            st.download_button(
                label="Download Audio",
                data=audio_buffer.getvalue(), # Get all bytes for download
                file_name=f"gtts_speech_{lang}.mp3",
                mime="audio/mp3"
            )

        except Exception as e:
            st.error(f"Error generating audio: {e}")
            st.caption("Common issues: No internet connection, unsupported language, or Google might temporarily block requests if too frequent.")
else:
    st.info("Please enter some text in the box above to generate speech.")

st.markdown("---")
st.caption("Powered by Google Text-to-Speech (gTTS). Requires an internet connection.")