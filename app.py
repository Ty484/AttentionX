import streamlit as st
import whisper
from moviepy.editor import VideoFileClip
import os

st.title("🎬 AttentionX - AI Video Clipper")

# Create output folder
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# Upload video
uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

if uploaded_file:
    video_path = "input_video.mp4"
    
    # Save uploaded file
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.success("✅ Video uploaded successfully!")

    if st.button("🚀 Process Video"):
        st.info("Processing... please wait ⏳")

        # Load Whisper model (use "tiny" for faster processing)
        model = whisper.load_model("tiny")

        # Transcribe video
        result = model.transcribe(video_path)

        st.subheader("📜 Transcript")
        st.write(result["text"])

        # Keywords to detect important parts
        keywords = ["important", "success", "key", "mistake", "learn"]

        selected_segments = []
        for segment in result["segments"]:
            text = segment["text"].lower()
            if any(word in text for word in keywords):
                selected_segments.append(segment)

        # Fallback if nothing found
        if len(selected_segments) == 0:
            selected_segments = result["segments"][:3]

        # Limit to 3 clips
        selected_segments = selected_segments[:3]

        video = VideoFileClip(video_path)

        st.subheader(" Generated Clips")

        for i, seg in enumerate(selected_segments):
            start = seg["start"]
            end = seg["end"]

            clip = video.subclip(start, end)
            output_path = f"outputs/clip_{i}.mp4"

            clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

            st.video(output_path)
            st.write(f" {seg['text']}")

        st.success(" Done! Clips generated successfully.")