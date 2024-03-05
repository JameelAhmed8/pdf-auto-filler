import streamlit as st
from pdf2image import convert_from_path
from PIL import ImageEnhance, ImageFilter
import pytesseract
from fpdf import FPDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
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
    text_content = convert_pdf_to_images_and_create_pdf(
        pdf_path=pdf_path,
        output_folder='./temp',
        output_pdf_path='./temp/output_searchable.pdf'
    )

    # ...

    # Display editable text
    edited_text = st.text_area("Edit the extracted text", "\n".join(map(str, text_content)))

    # Confirmation button
    if st.button("Confirm and Generate PDF"):
        # Save edited text to a new PDF
        text_to_pdf(edited_text.encode('latin-1', 'replace').decode('latin-1'), './temp/output_searchable_confirmed.pdf')
        st.success("New searchable PDF generated!")

        # Provide download link for the generated PDF
        st.subheader("Download Generated PDF:")
        st.markdown(
            f"[Download PDF](/Users/apple/Desktop/imageDataExtract/temp/output_searchable_confirmed.pdf)",
            unsafe_allow_html=True
        )