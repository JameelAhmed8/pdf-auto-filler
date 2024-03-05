import PyPDF2

def get_pdf_form_fields(pdf_path):
    pdf_fields = {}
    with open(pdf_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        fields = pdf.get_fields()
        for field_name in fields:
            field = fields[field_name]
            field_type = field.get('/FT', '')
            if field_type == '/Tx':  # Text field
                field_value = field.get('/V', '')
            elif field_type == '/Btn':  # Button (checkbox/radio)
                field_value = field.get('/V', '')
                if isinstance(field_value, PyPDF2.generic.ArrayObject):
                    field_value = [v.getObject()['/AS'] for v in field_value]
            else:
                field_value = None
            pdf_fields[field_name] = field_value
    return pdf_fields

pdf_path = 'sample1.pdf'
form_fields = get_pdf_form_fields(pdf_path)

for field_name, field_value in form_fields.items():
    print(f"Field Name: {field_name}, Field Value: {field_value}")
