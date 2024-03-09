import streamlit as st

def main():
    st.title('Text Editor')

    # Define field names and initial values
    field_data = {
        "FieldName1": "Value1",
        "FieldName2": "Value2",
        "FieldName3": "Value3"
    }

    # Display the table-like structure in a single text area
    st.write("## Editable Text Fields")

    # Construct the string for the single text area
    edited_values = ""
    for field_name, initial_value in field_data.items():
        edited_values += f"{field_name}: {st.text_input(label='', value=initial_value, key=field_name)}\n"

    # Display the edited values
    st.write("### Edited Values:")
    st.text_area(label='', value=edited_values, height=200, key='editable_text_area')

if __name__ == "__main__":
    main()
