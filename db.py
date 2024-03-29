import base64
import os

import streamlit as st
from PIL import ImageEnhance, ImageFilter
from fpdf import FPDF
from pdf2image import convert_from_path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pytesseract
import replicate
from fillpdf import fillpdfs
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Set the Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "r8_XVYY2HcLZ3ICYEDpidB0UF04htcRikg4QTvhZ"


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

    return text_content


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
    x_cursor, y_cursor = 72, 800
    canvas_obj.setFont("Helvetica", 12)
    line_height = 14

    for line in text.split('\n'):
        if y_cursor < 0:
            canvas_obj.showPage()
            y_cursor = 800
        canvas_obj.drawString(x_cursor, y_cursor, line)
        y_cursor -= line_height


# Streamlit app
st.title("Fintech-AI MVP")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.success("File successfully uploaded!")

    # Save the uploaded file to a temporary location
    pdf_path = os.path.join('./temp', 'uploaded_pdf.pdf')
    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(uploaded_file.read())


    text_content = convert_pdf_to_images_and_create_pdf(
        pdf_path=pdf_path,
        output_folder='./temp',
        output_pdf_path='./temp/output_searchable.pdf'
    )

    # Display editable text
    st.subheader("Extracted Raw Text:")
    edited_text = st.text_area("Edit the extracted text", "\n".join(map(str, text_content)))

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


    # Define the input parameters for the replication stream
    input_params = {
        "debug": False,
        "prompt": (
           "You are given a list of fields below, followed by raw text."
           "Raw text data is containing information related to insurance policies, clients, and advisors. Your task is to parse this raw text and extract the relevant information that could be filled into the fields provided above. "
           "The extracted information should be presented in the format: FieldName: Value"
           "Your model should be able to understand the context of the raw text and identify the information that corresponds to each field accurately. Make sure the output follows the exact structure of the provided field list, "
           "maintaining the same field names and formatting conventions."
           "In accordance with the provided structure, if the field name is 'Ci ty,' the model should ensure that it adheres to this exact naming convention, even if it encounters 'City' in the raw text. Follow this for entire given Fields' list"
            "Please proceed with parsing the raw text and generating the required output."
            "SVP Name\n"
            "Primary Insured\n"
            "Primary DOB Month\n"
            "Primary DOB Date\n"
            "Primary DOB Year\n"
            "Primary Phone\n"
            "Second Insured\n"
            "Secondary DOB Month\n"
            "Secondary DOB Date\n"
            "Secondary DOB Year\n"
            "Secondary Phone\n"
            "Address\n"
            "Cit y\n"
            "State\n"
            "Email Address\n"
            "NotesT ravel Hobbies Language etc\n"
            "T ime\n"
            "T ime_2\n"
            "Date_2\n"
            "Date\n"
            "Other\n"
            "S pecial Instructions\n"
            "Carrier\n"
            "Face Amount\n"
            "Product\n"
            "Prop osed Premium\n"
            "Financial Advisor Name\n"
            "Stat e of Issue\n"
            "ROP\n"
            "Rate Class quot ed\n"
            "Universal Life\n"
            "Whole Life\n"
            "Index UL\n"
            "Variable Life\n"
            "LTC Rider\n"
            "Last Survivor\n"
            "Will new insurance replace any inforce i nsurance\n"
            "Financial Advisor Name\n"
            "Firm\n"
            "Email\n"
            "Branch City\n"
            "Business Phone 123\n"
            "Business Phone 456\n"
            "Business Phone 78910\n"
            "Licensed in\n"
            "Licensed in State of Insured\n"
            "Advisor Appointed with Carrier & PSF\n"
            "Date_3\n"
            "Zip Code\n"
            "Trust to be established\n"
            "Text Field0\n"
            "Ownership\n"
            "\nRaw Text:\n"
            "{}"  # Placeholder for the raw text
        ).format(edited_text),
        "temperature": 0.5,
        "system_prompt":"Please keep in mind that I have given you the list below and there are some field names like Gender 1,  or T ime or T ime_2 or C ity. "
                        "Now if you find City then dont give me City but keep in mind the given strcture and keep it as C ity etc. Also Give me full list as given by me. "
                        "In case you are unable to extract anything like given list then leave the value empty as ''.\n"
,
        "max_new_tokens": 500,
        "min_new_tokens": -1
    }

    if "form_extracted" not in st.session_state:
        st.session_state.form_extracted = None

    if st.button("Confirm Selection"):
        with st.spinner("Extracting relevant data..."):
            # Stream the output of the llama-2-70b-chat model
            output_events = []
            for event in replicate.stream("meta/llama-2-70b-chat", input=input_params):
                output_events.append(event)

            # Convert the list of output events to a single string
            output_text = ''.join(map(str, output_events))
            print(output_text)

            # Display the edited text
            st.subheader("Edited Text:")
            edited_text1 = st.text_area("Edit the extracted text", output_text)
            st.session_state.form_extracted = edited_text1
            print('Edited: ', edited_text1)

    if st.session_state.form_extracted is not None and st.button("Confirm Fill"):
        with st.spinner("Filling PDF..."):
            # Split the input text into lines
            lines = st.session_state.form_extracted.split("\n")
            data_dict = {}

            # Iterate over the lines and add the key-value pairs to the dictionary
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    data_dict[key.strip()] = value.strip()
            print('dict to fill:', data_dict)
            # Save edited text to a new PDF
            fillpdfs.write_fillable_pdf('form.pdf', 'new.pdf', data_dict)
            print('fill pdf')

            # Provide download link for the generated PDF
            st.subheader("Download Generated PDF:")

            # Display PDF file
            pdf_path = "new.pdf"

            # Display a download button for the PDF file
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
            st.markdown(f'<a href="data:application/pdf;base64,{pdf_b64}" download="new.pdf">Download PDF file</a>',
                        unsafe_allow_html=True)