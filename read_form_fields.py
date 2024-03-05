import PyPDF2


def get_form_fields(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    fields = pdf_reader.get_form_text_fields()
    return fields


def extract_text_sections(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)

    # Dictionary to store sections and their texts
    sections = {}

    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()

        # Assuming sections are marked by titles preceded by "Section" (modify as needed)
        section_titles = [line.strip() for line in text.split('\n') if line.startswith('Section')]

        # Extracting texts under each section
        for i in range(len(section_titles)):
            section_title = section_titles[i]
            if i + 1 < len(section_titles):
                section_text = text.split(section_titles[i])[1].split(section_titles[i + 1])[0].strip()
            else:
                section_text = text.split(section_titles[i])[1].strip()

            sections[section_title] = section_text

    return sections


# Example Usage
pdf_path = './form.pdf'
fields = get_form_fields(pdf_path)
text_sections = extract_text_sections(pdf_path)

# Print form fields
print("Form Fields:")
for field in fields:
    print(f"Field Name: {field}")
    print(f"Value: {fields[field]}")
    print("-" * 20)

# Print text sections
print("\nText Sections:")
for section_title, section_text in text_sections.items():
    print(f"Section Title: {section_title}")
    print(f"Section Text: {section_text}")
    print("-" * 20)
