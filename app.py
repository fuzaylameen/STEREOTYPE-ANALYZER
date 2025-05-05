import streamlit as st
import os
import cv2
import tempfile
import csv
from deepface import DeepFace
import numpy as np
from main import process_pdf_and_analyze  # Your original script function


def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = int(frame_count / fps)

    frames = []
    for second in range(duration):
        cap.set(cv2.CAP_PROP_POS_FRAMES, second * fps)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)

    cap.release()
    return frames, duration

def analyze_frame_for_gender_emotion(frame):
    try:
        result = DeepFace.analyze(frame, actions=['gender', 'emotion'], enforce_detection=False)
        return result
    except Exception:
        return None

def check_for_stereotype(analysis):
    stereotypical = False
    gender = None
    emotion = None

    for person in analysis:
        gender = person['dominant_gender'].lower()
        emotion = person['dominant_emotion'].lower()
        if (gender == 'man' and emotion == 'angry') or (gender == 'woman' and emotion == 'fear'):
            stereotypical = True

    return gender, emotion, stereotypical

def save_to_csv(data, filename="gender_emotion_data.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Frame", "Gender", "Emotion", "Stereotypical"])
        writer.writerows(data)

def analyze_trailer(video_path):
    frames, duration = extract_frames(video_path)
    total_frames = len(frames)
    stereotypical_frames = 0
    frame_data = []

    with st.spinner("Analyzing trailer... Please wait."):
        progress = st.progress(0)
        for frame_count, frame in enumerate(frames):
            analysis = analyze_frame_for_gender_emotion(frame)
            if analysis:
                gender, emotion, stereotypical = check_for_stereotype(analysis)
                frame_data.append([frame_count + 1, gender, emotion, stereotypical])
                if stereotypical:
                    stereotypical_frames += 1
            progress.progress((frame_count + 1) / total_frames)

    save_to_csv(frame_data)
    return stereotypical_frames, total_frames, "gender_emotion_data.csv"



st.set_page_config(page_title="Stereotype Analyzer", layout="wide")

st.title("🎥 Gender Stereotype Detection in Media")

tab1, tab2 = st.tabs(["📄 Script PDF Analyzer", "🎬 Trailer Video Analyzer"])


with tab1:
    st.subheader("Analyze a Movie Script (PDF)")
    st.write("Upload a movie script in PDF format. The system will translate, clean, and analyze it for gender-stereotypical dialogues.")
    
    pdf_file = st.file_uploader("📄 Upload Script PDF", type=["pdf"], key="script_pdf")

    if pdf_file is not None:
        with open("temp_uploaded_script.pdf", "wb") as f:
            f.write(pdf_file.read())

        st.success("✅ PDF uploaded successfully. Click below to analyze.")

        if st.button("🔍 Analyze Script"):
            with st.spinner("Processing script... this may take a minute ⏳"):
                process_pdf_and_analyze("temp_uploaded_script.pdf")
            st.success("✅ Script analysis complete!")

            if os.path.exists("similarity_results.csv"):
                with open("similarity_results.csv", "rb") as f:
                    st.download_button("📥 Download All Results", f, file_name="similarity_results.csv", mime="text/csv")

            if os.path.exists("stereotypical_lines.csv"):
                with open("stereotypical_lines.csv", "rb") as f:
                    st.download_button("📥 Download Stereotypical Lines Only", f, file_name="stereotypical_lines.csv", mime="text/csv")
    else:
        st.info("👈 Upload a script PDF to begin.")


with tab2:
    st.subheader("Analyze a Trailer Video")
    st.write("Upload a movie trailer to detect emotional and gender-based stereotypes in visual scenes.")

    video_file = st.file_uploader("🎞️ Upload Trailer Video (MP4/MOV/AVI)", type=["mp4", "mov", "avi"], key="trailer_video")

    if video_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(video_file.read())
            temp_video_path = tmp_file.name

        if st.button("🚀 Start Video Analysis"):
            stereotypical_frames, total_frames, csv_path = analyze_trailer(temp_video_path)

            st.subheader("📊 Final Analysis Summary")
            st.write(f"Total frames processed: {total_frames}")
            st.write(f"Stereotypical frames detected: {stereotypical_frames}")

            if stereotypical_frames > 15:
                st.error("🔴 The trailer is classified as **Stereotypical**.")
            else:
                st.success("🟢 The trailer is classified as **Not Stereotypical**.")

            with open(csv_path, "rb") as f:
                st.download_button("📥 Download Frame Analysis CSV", data=f, file_name="trailer_analysis.csv", mime="text/csv")
    else:
        st.info("👈 Upload a video file to begin.")
