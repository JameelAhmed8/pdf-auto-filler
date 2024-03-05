import PyPDF2

def fill_pdf(input_pdf_path, output_pdf_path, field_map):
    with open(input_pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            if "/Annots" in page:
                for annot_ref in page['/Annots']:
                    annot = annot_ref.get_object()
                    if annot.get("/Subtype") == "/Widget" and annot.get("/T") in field_map:
                        field_name = annot["/T"][1:-1]
                        if field_name in field_map:
                            field_value = field_map[field_name]
                            annot.update({
                                PyPDF2.generic.NameObject("/V"): PyPDF2.generic.createStringObject(field_value)
                            })
                            annot.update({
                                PyPDF2.generic.NameObject("/DV"): PyPDF2.generic.createStringObject(field_value)
                            })
                            annot.update({
                                PyPDF2.generic.NameObject("/AS"): PyPDF2.generic.createStringObject(field_value)
                            })
            pdf_writer.add_page(page)

        with open(output_pdf_path, "wb") as output_pdf_file:
            pdf_writer.write(output_pdf_file)

# Example usage
input_pdf_path = "pdf-conversion-services.pdf"
output_pdf_path = "filled-out.pdf"
field_map = {
    "Address": "John Doe",
    # Add more field names and values as needed
}
fill_pdf(input_pdf_path, output_pdf_path, field_map)
