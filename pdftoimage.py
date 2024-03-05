import PyPDF2
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import nltk
from nltk import ne_chunk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from reportlab.pdfgen import canvas
import os

# NLTK setup
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def extract_text_and_perform_ner(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    images = convert_from_path(pdf_path)
    all_named_entities = []

    for image in images:
        enhanced_image = enhance_image(image)
        text = pytesseract.image_to_string(enhanced_image)
        named_entities = named_entity_recognition(text)
        all_named_entities.extend(named_entities)

    return all_named_entities

def enhance_image(image):
    grayscale = image.convert('L')
    contrast = ImageEnhance.Contrast(grayscale)
    enhanced_contrast = contrast.enhance(2.0)
    sharpened = enhanced_contrast.filter(ImageFilter.SHARPEN)
    return sharpened

def named_entity_recognition(text):
    word_tokens = word_tokenize(text)
    pos_tags = pos_tag(word_tokens)
    named_entities = ne_chunk(pos_tags)
    return named_entities


def get_form_fields(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    return pdf_reader.get_form_text_fields()

def process_ner_results(ner_results):
    processed_data = {}
    for page in ner_results:
        for entity in page:
            if isinstance(entity, nltk.Tree):
                entity_type = entity.label()
                entity_text = ' '.join(c[0] for c in entity.leaves())
                if entity_type not in processed_data:
                    processed_data[entity_type] = []
                processed_data[entity_type].append(entity_text)
    return processed_data

def map_entities_to_form_fields(processed_ner_data, form_fields):
    data_to_fill = {}
    keyword_to_entity_type = {
        'name': 'PERSON',
        'organization': 'ORGANIZATION',
        'city': 'GPE',
        'state': 'GPE',
        # Add more keyword-entity mappings as needed
    }
    for field_name in form_fields:
        for keyword, entity_type in keyword_to_entity_type.items():
            if keyword in field_name.lower() and processed_ner_data.get(entity_type):
                data_to_fill[field_name] = processed_ner_data[entity_type][0]
                break
    return data_to_fill

def fill_pdf(input_pdf_path, output_pdf_path, data_to_fill):
    pdf_reader = PyPDF2.PdfReader(input_pdf_path)
    pdf_writer = PyPDF2.PdfWriter()

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        try:
            pdf_writer.add_page(page)
            pdf_writer.update_page_form_field_values(page, data_to_fill)
        except Exception as e:
            print(f"Error processing page {page_num}: {e}")

    with open(output_pdf_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)


def create_overlay_pdf(input_pdf_path, output_pdf_path, data_to_fill, coordinates):
    input_pdf = PyPDF2.PdfReader(input_pdf_path)
    for page_num, page in enumerate(input_pdf.pages):
        # Convert PDF page to image
        image = convert_from_path(input_pdf_path, first_page=page_num + 1, last_page=page_num + 1)[0]
        image_path = f"temp_page_{page_num}.png"
        image.save(image_path, "PNG")

        # Create a new PDF and overlay text onto the image
        overlay_pdf = canvas.Canvas(output_pdf_path)
        overlay_pdf.drawImage(image_path, 0, 0, width=image.width, height=image.height)

        for field, text in data_to_fill.items():
            if field in coordinates:
                x, y = coordinates[field]
                overlay_pdf.drawString(x, y, text)

        overlay_pdf.showPage()
        overlay_pdf.save()
        os.remove(image_path)  # Clean up temporary image file


# Extract text and perform NER
extracted_pdf_path = 'input.pdf'
output_folder = './results'
ner_results = extract_text_and_perform_ner(extracted_pdf_path, output_folder)
processed_ner_data = process_ner_results(ner_results)

# Example mapping and coordinates (these need to be set up manually)
form_fields = get_form_fields(extracted_pdf_path)
data_to_fill = map_entities_to_form_fields(processed_ner_data, form_fields)
coordinates = {
    'field_name': (100, 100),  # Example coordinates
    # Add coordinates for each field
}

# Create overlay PDF
output_pdf_path = 'filled_form.pdf'
create_overlay_pdf(extracted_pdf_path, output_pdf_path, data_to_fill, coordinates)
