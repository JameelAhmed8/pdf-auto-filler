from pdf2image import convert_from_path
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import os
import nltk
from nltk import ne_chunk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Ensure NLTK packages are downloaded
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def extract_text_and_perform_ner(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = convert_from_path(pdf_path)

    for i, image in enumerate(images):
        enhanced_image = enhance_image(image)
        text = pytesseract.image_to_string(enhanced_image)
        print(text)
        named_entities = named_entity_recognition(text)

        #print(f"----- Page {i + 1} -----")
        #print(named_entities)


def enhance_image(image):
    grayscale = image.convert('L')
    contrast = ImageEnhance.Contrast(grayscale)
    enhanced_contrast = contrast.enhance(2.0)
    sharpened = enhanced_contrast.filter(ImageFilter.SHARPEN)
    return sharpened


def named_entity_recognition(text):
    # Tokenize the text
    word_tokens = word_tokenize(text)

    # Part-of-Speech Tagging
    pos_tags = pos_tag(word_tokens)

    # Named Entity Recognition
    named_entities = ne_chunk(pos_tags)

    return named_entities


# Example usage
pdf_path = 'input.pdf'  # Replace with your actual PDF file path
output_folder = './results'
extract_text_and_perform_ner(pdf_path, output_folder)
