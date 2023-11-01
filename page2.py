import torch
import streamlit as st
from PIL import Image
from RealESRGAN import RealESRGAN

def main():
    # Load the RealESRGAN model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = RealESRGAN(device, scale=4)
    model.load_weights('weights/RealESRGAN_x4.pth', download=True)

    st.title("RealESRGAN Super-Resolution App")

    # Create a file uploader to allow users to upload their own images
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_image is not None:
        # Preprocess the uploaded image
        input_image = Image.open(uploaded_image).convert('RGB')

        # Apply super-resolution with RealESRGAN
        sr_image = model.predict(input_image)

        # Display the original input image and RealESRGAN super-resolved output
        st.subheader("Original Input Image")
        st.image(input_image, caption="Input Image", use_column_width=True)

        st.subheader("RealESRGAN Super-Resolved Image")
        st.image(sr_image, caption="RealESRGAN Output", use_column_width=True)

    st.write("Upload an image to apply super-resolution with RealESRGAN.")

if __name__ == '__main__':
    main()
