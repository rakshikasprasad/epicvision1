import streamlit as st
from deepface import DeepFace
import os
from fpdf import FPDF
import base64
from mailjet_rest import Client

def analyze_image_and_send_report(uploaded_image, user_email):
    # Create a temporary directory to save the uploaded image
    temp_dir = "temp_images"
    os.makedirs(temp_dir, exist_ok=True)
    image_path = os.path.join(temp_dir, uploaded_image.name)

    # Save the uploaded image to the temporary directory
    with open(image_path, "wb") as f:
        f.write(uploaded_image.read())

    # Analyze the uploaded image using DeepFace
    objs = DeepFace.analyze(img_path=image_path, actions=['age', 'gender'])

    # Display the uploaded image
    st.image(image_path, caption="Uploaded Image", use_column_width=True)

    # Display the analysis results
    st.write("Analysis Results:")
    st.write(f"Age: {objs[0]['age']}")  # Access age value correctly
    st.write(f"Gender: {objs[0]['dominant_gender']}")  # Access gender value correctly

    # Generate a PDF report with input and output
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="DeepFace Analysis Report", ln=True, align='C')
    pdf.ln(10)
    pdf.image(image_path, x=20, w=170)
    pdf.ln(90)
    pdf.multi_cell(0, 10, f"Age: {objs[0]['age']}")  # Access age value correctly
    pdf.multi_cell(0, 10, f"Gender: {objs[0]['dominant_gender']}")  # Access gender value correctly
    report_directory = "reports"
    os.makedirs(report_directory, exist_ok=True)
    report_path = os.path.join(report_directory, "analysis_report.pdf")

    # Save the PDF report
    pdf.output(report_path)

    # Add a button to open the saved PDF report
    with open(report_path, "rb") as pdf_file:
        pdf_base64 = base64.b64encode(pdf_file.read()).decode("utf-8")
        st.markdown(f'<a href="data:application/pdf;base64,{pdf_base64}" download="analysis_report.pdf">Click here to download the PDF report</a>', unsafe_allow_html=True)

    if user_email:
        # Define your Mailjet API credentials
        api_key = '0ead2c3626ae020259731902be3d5388'
        api_secret = '708678863cf12d8c6435e2ecb7ed9f47'
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')

        # Create the email message
        message = {
            'Messages': [
                {
                    'From': {
                        'Email': 'studyaccrakshika@gmail.com',
                        'Name': 'EpicVision',
                    },
                    'To': [
                        {
                            'Email': user_email,
                            'Name': 'Recipient Name',
                        },
                    ],
                    'Subject': 'Criminal Suspect Report',
                    'TextPart': 'Attached is the Criminal Suspect Report.',
                    'Attachments': [
                        {
                            'ContentType': 'application/pdf',
                            'Filename': 'analysis_report.pdf',
                            'Base64Content': pdf_base64,
                        },
                    ],
                },
            ]
        }

        # Send the email using Mailjet
        response = mailjet.send.create(data=message)
        if response.status_code == 200:
            st.write(f"Report sent to {user_email}")
        else:
            st.error("Failed to send the email. Please check your Mailjet API credentials.")
    else:
        st.warning("Please enter your email address before sending the report.")

def main():
    st.title("DeepFace Image Analyzer")

    # Create a Streamlit file uploader widget to allow users to upload an image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    user_email = st.text_input("Enter your email address")

    if st.button("Send Report via Email"):
        analyze_image_and_send_report(uploaded_image, user_email)

    if uploaded_image is not None:
        analyze_image_and_send_report(uploaded_image, user_email)
    else:
        st.write("Please upload an image.")

if __name__ == '__main__':
    main()
