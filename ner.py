from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import os
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from nltk import word_tokenize, pos_tag, ne_chunk
import nltk

# Ensure NLTK packages are downloaded
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def extract_text_and_perform_ner(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = convert_from_path(pdf_path)

    extracted_text = ""
    for i, image in enumerate(images):
        enhanced_image = enhance_image(image)
        text = pytesseract.image_to_string(enhanced_image)
        extracted_text += text + "\n"

    # Save extracted text to a text file
    text_file_path = os.path.join(output_folder, 'extracted_text.txt')
    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(extracted_text)

    # Generate editable PDF
    generate_editable_pdf(extracted_text, output_folder)

    print("Editable PDF generated successfully.")

def enhance_image(image):
    grayscale = image.convert('L')
    contrast = ImageEnhance.Contrast(grayscale)
    enhanced_contrast = contrast.enhance(2.0)
    sharpened = enhanced_contrast.filter(ImageFilter.SHARPEN)
    return sharpened

def generate_editable_pdf(extracted_text, output_folder):
    pdf_output_path = os.path.join(output_folder, 'editable_pdf.pdf')

    # Create a PDF canvas
    c = canvas.Canvas(pdf_output_path)

    # Split the extracted text into lines and add to PDF
    lines = extracted_text.split('\n')
    y_position = 800  # Adjust the starting y-position as needed
    for line in lines:
        c.drawString(100, y_position, line)  # Adjust the x and y positions as needed
        y_position -= 15  # Adjust the line spacing as needed

    c.save()

# Example usage
pdf_path = 'input.pdf'  # Replace with your actual PDF file path
output_folder = './results'
extract_text_and_perform_ner(pdf_path, output_folder)
