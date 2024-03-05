# import streamlit as st
# from PyPDF2 import PdfReader
# import base64
#
# # Upload a PDF file
# pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
#
# if pdf_file is not None:
#     # Read the PDF file
#     pdf_reader = PdfReader(pdf_file)
#     num_pages = len(pdf_reader.pages)
#
#     # Convert the PDF to base64
#     pdf_base64 = base64.b64encode(pdf_file.getvalue()).decode('utf-8')
#     pdf_display = f'<embed src="data:application/pdf;base64,{pdf_base64}" width="700" height="1000" type="application/pdf">'
#
#     # Display the PDF
#     st.markdown(pdf_display, unsafe_allow_html=True)


import streamlit as st
from PyPDF2 import PdfReader
import base64
import os

# Path to the folder containing PDF files
pdf_folder = "./pdfs"

# List PDF files in the folder
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]

# Dropdown to select a PDF file
selected_pdf = st.selectbox("Select a PDF file", pdf_files)

# Read the selected PDF file
pdf_path = os.path.join(pdf_folder, selected_pdf)
with open(pdf_path, "rb") as file:
    pdf_bytes = file.read()

# Convert the PDF to base64
pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
pdf_display = f'<embed src="data:application/pdf;base64,{pdf_base64}" width="700" height="1000" type="application/pdf">'

# Display the PDF
st.markdown(pdf_display, unsafe_allow_html=True)
