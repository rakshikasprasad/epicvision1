import streamlit as st
import cv2
import os

# Define the function to extract images from video
def get_frames_from_video(filename):
    cam = cv2.VideoCapture(filename)
    frame_rate = cam.get(cv2.CAP_PROP_FPS)
    st.text("Frame Rate: " + str(frame_rate))
    frame_interval = int(frame_rate)

    try:
        if not os.path.exists('inputs'):
            os.makedirs('inputs')
    except OSError:
        st.warning('Error: Creating directory for data')

    current_frame = 0
    num_frames_extracted = 0

    while True:
        ret, frame = cam.read()
        if ret:
            if current_frame % frame_interval == 0:
                frame_number = int(current_frame / frame_interval)
                image_name = f'./inputs/frame{frame_number}.jpg'
                num_frames_extracted += 1
                cv2.imwrite(image_name, frame)

            current_frame += 1
        else:
            break

    st.text("No. of frame/Images: " + str(num_frames_extracted))
    cam.release()
    cv2.destroyAllWindows()
    st.success("Images extracted successfully.\nSaved to 'inputs' folder.")

def main():
    st.title("Video to Frames for Image Reconstruction")
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])
    
    if uploaded_file is not None:
        with open("temp.mp4", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        get_frames_from_video("temp.mp4")
        
        os.remove("temp.mp4")

if __name__ == '__main__':
    main()
