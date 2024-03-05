#!/usr/bin/python

import argparse
import tempfile
import os
import time
import fitz  # PyMuPDF
import spacy
from PIL import Image
import io

from AbbyyOnlineSdk import *

from AbbyyOnlineSdk import AbbyyOnlineSdk

nlp = spacy.load("en_core_web_sm")
processor = None

def setup_processor():
    if "ABBYY_APPID" in os.environ:
        processor.ApplicationId = os.environ["ABBYY_APPID"]

    if "ABBYY_PWD" in os.environ:
        processor.Password = os.environ["ABBYY_PWD"]

        # Proxy settings
    if "http_proxy" in os.environ:
        proxy_string = os.environ["http_proxy"]
        print("Using http proxy at {}".format(proxy_string))
        processor.Proxies["http"] = proxy_string

    if "https_proxy" in os.environ:
        proxy_string = os.environ["https_proxy"]
        print("Using https proxy at {}".format(proxy_string))
        processor.Proxies["https"] = proxy_string


def convert_pdf_to_images(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

def recognize_image(image, language, output_format):
        settings = ProcessingSettings()
        settings.Language = language
        settings.OutputFormat = output_format

        # Save image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_image_file:
            image.save(temp_image_file, format='PNG')
            temp_image_file_path = temp_image_file.name

        try:
            task = processor.process_image(temp_image_file_path, settings)
            if task is None:
                print("Error")
                return
            if task.Status == "NotEnoughCredits":
                print("Not enough credits to process the document.")
                return

            while task.is_active():
                time.sleep(5)
                task = processor.get_task_status(task)

            if task.Status == "Completed":
                processor.download_result(task, temp_image_file_path)
                with open(temp_image_file_path, 'r') as file:
                    result_text = file.read()
                return result_text
            else:
                print("Error processing task")
        finally:
            # Clean up the temporary file
            os.remove(temp_image_file_path)


def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def process_pdf(file_path, result_file_path, language, output_format):
    images = convert_pdf_to_images(file_path)
    extracted_text = ""

    for img in images:
        text = recognize_image(img, language, output_format)
        if text:
            extracted_text += text + "\n"

    entities = extract_entities(extracted_text)

    with open(result_file_path, 'w', encoding='utf-8') as file:
        file.write("Extracted Text:\n")
        file.write(extracted_text)
        file.write("\n\nExtracted Entities:\n")
        for entity, label in entities:
            file.write(f"{entity} ({label})\n")

    print(f"Extracted text and entities have been written to {result_file_path}")

def main():
    global processor
    processor = AbbyyOnlineSdk()

    setup_processor()

    parser = argparse.ArgumentParser(description="Process a PDF file and extract text and entities")
    parser.add_argument('source_file')
    parser.add_argument('target_file')
    parser.add_argument('-l', '--language', default='English', help='Recognition language (default: %(default)s)')
    parser.add_argument('-f', '--format', default='txt', help='Output format (default: %(default)s)')
    args = parser.parse_args()

    process_pdf(args.source_file, args.target_file, args.language, args.format)

if __name__ == "__main__":
    main()
