import streamlit as st
from PIL import Image
import numpy as np
import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet
import gfpgan

# Function to enhance image using GFP-GAN
def enhance_image(input_image):
    # Load the pre-trained GFP-GAN model
    # Note: Update the model path as per your GFP-GAN model file location
    model_path = 'C:\RAKSHIKA\capstone\draft\GFPGAN.pth' # Update this path
    model = gfpgan.GFPGANer(model_path=model_path, upscale=1, arch='clean', channel_multiplier=2)

    # Convert PIL Image to Numpy array (RGB)
    img_np = np.array(input_image)

    # If necessary, convert from RGB (PIL default) to BGR (OpenCV default)
    img_np = img_np[:, :, ::-1]

    # Enhance the image using GFP-GAN
    # Note: The arguments to `enhance` may vary depending on GFP-GAN version
    _, _, output = model.enhance(img_np, has_aligned=False, only_center_face=False, paste_back=True)

    # Convert the output from BGR back to RGB and then to PIL Image for Streamlit
    enhanced_image = Image.fromarray(output[:, :, ::-1])

    return enhanced_image

# Streamlit app
def main():
    st.title("Image Enhancement using GFP-GAN")

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        if st.button('Enhance Image'):
            with st.spinner('Enhancing...'):
                # Enhance the image
                enhanced_image = enhance_image(image)
                st.image(enhanced_image, caption='Enhanced Image', use_column_width=True)

if __name__ == '__main__':
    main()
