import pyttsx3
import streamlit as st
import io
import threading
import time # For a small delay if needed

st.set_page_config(page_title="Text-to-Speech Converter", layout="centered")

st.title("Text-to-Speech Converter")
st.write("Type or change the text below, and the audio will attempt to play automatically.")

text = st.text_input("Enter your text here:", key="user_text_input")

# --- Function to generate and save audio in a separate thread ---
def generate_audio_threaded(text_to_speak, audio_buffer_param):  
    print(f"[Thread] Starting audio generation for text: '{text_to_speak[:50]}...'")
    try:
        engine = pyttsx3.init()
        print("[Thread] pyttsx3 engine initialized in thread.")

        voices = engine.getProperty('voices')

        #for i in voices:
    
        if voices:
            print(f"[Thread] Found {len(voices)} voices. Using voice ID: {voices[1].id}")
            engine.setProperty('voice', voices[1].id)
        else:
            print("[Thread] WARNING: No voices found in thread.")
            # Critical: if no voices, engine might not be able to do anything
            return # Exit early if no voices

        engine.say(text_to_speak)
        print("[Thread] Text queued for saying.")

        # Attempt to save to the BytesIO object
        # Note: Some pyttsx3 drivers might not fully support BytesIO directly without
        # a temporary file underneath. This is less common now, but keep in mind.
        engine.save_to_file(text_to_speak, "text_to_speech.mp3")
        print("[Thread] Text queued for saving to buffer.")

        engine.runAndWait() # This processes the commands
        print("[Thread] runAndWait() completed in thread.")

        # Verify if anything was written to the buffer from inside the thread
        current_pos = audio_buffer_param.tell()
        print(f"[Thread] Audio buffer current position after runAndWait: {current_pos} bytes.")
        if current_pos == 0:
            print("[Thread] WARNING: Audio buffer is still empty after runAndWait().")

    except Exception as e:
        print(f"[Thread] FATAL ERROR in audio generation thread: {e}")
        import traceback
        traceback.print_exc() # Print full traceback for thread errors


# --- Streamlit UI Logic ---
if text:
    st.info("Generating audio... Please wait. Check your terminal for detailed logs.")

    # Create a BytesIO buffer
    audio_buffer = io.BytesIO()

    # Create and start the thread
    audio_thread = threading.Thread(target=generate_audio_threaded, args=(text, audio_buffer))
    audio_thread.start()

    with st.spinner("Processing speech..."):
        audio_thread.join() # Wait for the thread to finish

    # After the thread has completed and joined
    # if audio_buffer.tell() > 0:
    #     audio_buffer.seek(0)

    #     st.success("Audio generated successfully!")

    #     st.audio(audio_buffer.read(), format='audio/mp3', start_time=0, autoplay=True)

    #     st.download_button(
    #         label="Download Audio",
    #         data=audio_buffer.getvalue(),
    #         file_name="generated_speech.mp3",
    #         mime="audio/mp3"
    #     )
    # else:
    #     st.error("Failed to generate audio. Please try again or check your pyttsx3 setup. (Buffer empty)")
    #     st.caption("Common reasons: No TTS voices installed, or pyttsx3 issue with environment.")

else:
    st.info("Please enter some text in the box above to generate speech.")