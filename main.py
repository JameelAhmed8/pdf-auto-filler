import easyocr
import fitz  # PyMuPDF
import spacy
from PIL import Image
import numpy as np

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def convert_pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

def extract_text_from_image(image):
    reader = easyocr.Reader(['en'])  # Initialize EasyOCR reader
    image_np = np.array(image)  # Convert PIL image to numpy array
    return " ".join([result[1] for result in reader.readtext(image_np, paragraph=True)])

def extract_text_from_file(file_path):
    if file_path.lower().endswith('.pdf'):
        images = convert_pdf_to_images(file_path)
    else:
        images = [Image.open(file_path)]

    extracted_text = ""
    for img in images:
        extracted_text += extract_text_from_image(img)
    return extracted_text

def extract_entities(text):
    # Process the text with spaCy
    doc = nlp(text)

    # Extract entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

if __name__ == "__main__":
    file_path = './input.pdf'  # or image file
    output_file_path = '/Users/apple/Desktop/imageDataExtract/output.txt'

    text = extract_text_from_file(file_path)

    # Extract entities
    entities = extract_entities(text)

    # Write the extracted text and entities to a file
    with open(output_file_path, 'w') as file:
        file.write("Extracted Text:\n")
        file.write(text)
        file.write("\n\nExtracted Entities:\n")
        for entity, label in entities:
            file.write(f"{entity} ({label})\n")

    print(f"Extracted text and entities have been written to {output_file_path}")