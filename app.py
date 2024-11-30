import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for the generative AI model
prompt = """You are a YouTube video summarizer. You will summarize the entire video transcript in points, providing the summary in under 250 words. Please summarize the following text: """

# Function to extract YouTube transcript
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split('=')[1]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item["text"] for item in transcript_data])
        return transcript
    except Exception as e:
        st.error(f"Error retrieving transcript: {e}")
        return None

# Function to generate summary using Google Generative AI
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return None

# Streamlit app UI with enhanced design
st.set_page_config(page_title="YouTube Video Summarizer", page_icon="📹", layout="centered")

# Header Section
st.title("📹 YouTube Video Summarizer")
st.markdown("""
<style>                
    .main-header {
        font-size: 24px;
        color: #4CAF50;
        font-weight: bold;
        text-align: center;
    }
    .summary-container {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    .summary-header {
        font-size: 20px;
        font-weight: bold;
        color: #FF5733;
    }
</style>
""", unsafe_allow_html=True)

# Input Section
st.markdown("<p class='main-header'>Turn any YouTube video into concise, easy-to-read notes!</p>", unsafe_allow_html=True)
youtube_link = st.text_input("🎥 Enter YouTube Video Link:")

# Display Thumbnail
if youtube_link:
    try:
        video_id = youtube_link.split('=')[1]
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", caption="Video Thumbnail", use_container_width=True)
    except IndexError:
        st.error("Invalid YouTube link format. Please enter a valid link.")

# Generate Summary Button
if youtube_link and st.button("✨ Generate Summary"):
    with st.spinner("🔄 Processing..."):
        try:
            transcript_text = extract_transcript_details(youtube_link)
            if transcript_text:
                summary = generate_gemini_content(transcript_text, prompt)
                if summary:
                    with st.container():
                        st.markdown("<div class='summary-container'>", unsafe_allow_html=True)
                        st.markdown("<p class='summary-header'>📝 Detailed Notes:</p>", unsafe_allow_html=True)
                        st.write(summary)
                        st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("No transcript available for this video.")
        except Exception as e:
            st.error(f"Error processing video: {e}")
