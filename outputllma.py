import replicate
import os

# Define the raw text variable
raw_text = """
DocuSign Envelope ID: EAC9BFCD-7E77-4A08-9A17-D6FAFF4BE437

Bundle ID
Client Data Sheet (for Independent RIA) aap
78210 Scott Summerlin PFG Advisors
Investment Advisor Rep Number _Investment Advisor Rep Name Investment Advisory Firm Name
Account Title
...
"""

# Set the Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "r8_8betJvhokQjMch86dLopatR91XA0Q0D2euZzf"

# Define the input parameters for the replication stream
input_params = {
    "debug": False,
    "prompt": (
        "Given a list of fields with empty values in the format 'Field Name: ', followed by raw text containing client information, your task is to extract and match field names mentioned in the raw text with the provided list of fields. If a field name or a potentially similar piece of information exists in the raw text, extract the corresponding value and output the final structure in the format 'Field Name: Value'.\n\n"
        "List of Fields:\n"
        "SVP Name\n"
        "Primary Insured\n"
        "Primary DOB Month\n"
        "Primary DOB Date\n"
        "Primary DOB Year\n"
        "Gender 1\n"
        "Primary Phone\n"
        "Second Insured\n"
        "Secondary DOB Month\n"
        "Secondary DOB Date\n"
        "Secondary DOB Year\n"
        "Gender 2\n"
        "Secondary Phone\n"
        "Address\n"
        "City\n"
        "State\n"
        "Email Address\n"
        "Notes Travel Hobbies Language etc\n"
        "Indicate Hour AM or PM 15 minute time frames please\n"
        "Other\n"
        "Special Instructions\n"
        "Carrier\n"
        "Face Amount\n"
        "Product\n"
        "Proposed Premium\n"
        "Will new insurance replace any inforce insurance\n"
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
    ).format(raw_text),
    "temperature": 0.5,
    "system_prompt": "Given a list of fields with empty values in the format 'Field Name: ', followed by raw text containing client information, your task is to extract and match field names mentioned in the raw text with the provided list of fields. If a field name or a potentially similar piece of information exists in the raw text, extract the corresponding value and output the final structure in the format 'Field Name: Value'.",
    "max_new_tokens": 500,
    "min_new_tokens": -1
}

# Stream the output of the llama-2-70b-chat model
output_events = []
for event in replicate.stream("meta/llama-2-70b-chat", input=input_params):
    output_events.append(event)

# Convert the list of output events to a single string
output_text = ''.join(map(str, output_events))

# Print or manipulate the output text as needed
print(output_text)
