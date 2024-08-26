import streamlit as st
from langchain_community.document_loaders import YoutubeLoader
from pytube.exceptions import PytubeError
import time

st.set_page_config(page_icon="🔗", page_title="Youtube Video Transcription")

###--- Title ---###
st.markdown("""
    <h1 style='text-align: center;'>
        <span style='color: #F81F6F;'>Youtube Video</span> 
        <span style='color: #f5f8fc;'>Transcript Generator</span>
    </h1>
""", unsafe_allow_html=True)

languages = {"Urdu":"ur", "Hindi":"hi", "English":"en", "French":"fr", "Arabic":"ar"}

columns = st.columns([4,2])

with columns[0]:
    url = st.text_input("Enter a Youtube Video URL:")

with columns[1]:
    target_lang = st.selectbox("Target Language", languages.keys())

if st.button("Get Transcript", use_container_width=True):
    if url:
        if "youtube.com" in url or "youtu.be" in url:
            cols = st.columns([1,4])
            video_id = YoutubeLoader.extract_video_id(url)
            cols[0].image(f"https://img.youtube.com/vi/{video_id}/0.jpg", caption="Video Thumbnail")
            
            attempt = 0
            success = False
            with st.spinner(":green[Loading the transcript]"):
                while attempt < 10 and not success:
                    attempt += 1
                    try:
                        loader = YoutubeLoader.from_youtube_url("https://www.youtube.com/watch?v=" + video_id,
                                                            add_video_info=True,
                                                            language=["hi", "ur", "en"],
                                                            translation=languages[target_lang])
                        data = loader.load()

                        if data:
                            st.write(data)
                            transcript = data[0].page_content
            
                            with cols[1].container(height=250, border=True):
                                st.write(transcript)
            
                            st.download_button(
                                label="Download Transcript",
                                key="download",
                                data=transcript,
                                file_name='transcript.txt',
                                mime='text/plain',
                                type="primary"
                            )
                            success = True
                        
                    except PytubeError as e:
                        if attempt == 10:
                            st.error(f"Pytube error: {e}", icon="❌")
                        else:
                            time.sleep(2)
                            
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {e}.", icon="❌")
                        break
        else:
            st.error("Please enter a valid URL", icon="❌")

    else:
        st.info("Please enter a URL to get transcription.")
