import streamlit as st
from pdf2image import convert_from_path
from PIL import ImageEnhance, ImageFilter
import pytesseract
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import fillpdf
from fillpdf import fillpdfs
from PyPDF2 import PdfReader
import base64
import os

def convert_pdf_to_images_and_create_pdf(pdf_path, output_folder, output_pdf_path):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = convert_from_path(pdf_path)
    text_content = []

    for image in images:
        enhanced_image = enhance_image(image)
        text = pytesseract.image_to_string(enhanced_image)
        text_content.append(text)

    create_searchable_pdf(text_content, output_pdf_path)
    print(f"Converted and processed {len(images)} pages and created a searchable PDF.")

    return text_content  # Add this line to return text_content

def enhance_image(image):
    grayscale = image.convert('L')
    contrast = ImageEnhance.Contrast(grayscale)
    enhanced_contrast = contrast.enhance(2.0)
    sharpened = enhanced_contrast.filter(ImageFilter.SHARPEN)
    return sharpened

def text_to_pdf(text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text)
    pdf.output(output_path)

def create_searchable_pdf(text_content, output_pdf_path):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    for page_text in text_content:
        add_page_text(c, page_text)
        c.showPage()
    c.save()

def add_page_text(canvas_obj, text):
    # Set the cursor to the top of a new page
    x_cursor, y_cursor = 72, 800  # Starting position
    canvas_obj.setFont("Helvetica", 12)  # Set font
    line_height = 14  # Line height

    for line in text.split('\n'):
        if y_cursor < 0:  # Check if we're at the bottom of the page
            canvas_obj.showPage()
            y_cursor = 800
        canvas_obj.drawString(x_cursor, y_cursor, line)
        y_cursor -= line_height

# Streamlit app
st.title("PDF Text Editor and Converter")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.success("File successfully uploaded!")

    # Save the uploaded file to a temporary location
    pdf_path = os.path.join('./temp', 'uploaded_pdf.pdf')
    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(uploaded_file.read())



    # Display extracted text
    st.subheader("Extracted Text:")
    # text_content = convert_pdf_to_images_and_create_pdf(
    #     pdf_path=pdf_path,
    #     output_folder='./temp',
    #     output_pdf_path='./temp/output_searchable.pdf'
    # )

    # ...
    text_content= fillpdfs.get_form_fields("form.pdf", sort=False, page_number=None)

    # Display editable text
    # Display editable text
    edited_text = st.text_area("Edit the extracted text",
                               "\n".join(f"{key}: {value}" for key, value in text_content.items()))

    # Assume edited_text is the edited text from the text area
    edited_lines = edited_text.split('\n')
    data_dict = {}
    for line in edited_lines:
        parts = line.split(':')
        key = parts[0].strip()
        value = parts[1].strip() if len(parts) > 1 else None
        data_dict[key] = value

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

    # Confirmation button
    if st.button("Confirm Selection and Fill the PDF"):
        # Save edited text to a new PDF
        fillpdfs.write_fillable_pdf('form.pdf', 'new.pdf', data_dict)

        # Provide download link for the generated PDF
        st.subheader("Download Generated PDF:")
        # st.markdown(
        #     f"[Download PDF](/Users/jameel/Downloads/imageDataExtract/new.pdf)",
        #     unsafe_allow_html=True
        # )

        # Display PDF file
        # Path to the existing PDF file
        pdf_path = "/Users/jameel/Downloads/imageDataExtract/new.pdf"

        # Display a download button for the PDF file
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
        st.markdown(f'<a href="data:application/pdf;base64,{pdf_b64}" download="new.pdf">Download PDF file</a>',
                    unsafe_allow_html=True)