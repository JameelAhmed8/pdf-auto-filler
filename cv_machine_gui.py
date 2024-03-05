# Import necessary libraries
import streamlit as st

# Title of the web app
st.title("My Streamlit Web App")

# Subheader
st.subheader("A simple example")

# Add a text input
user_input = st.text_input("Enter your name:", "John Doe")

# Add a button
button_clicked = st.button("Click me!")

# Check if the button is clicked
if button_clicked:
    st.write(f"Hello, {user_input}!")

# Add a slider for a numerical input
number_input = st.slider("Choose a number", 1, 10, 5)
st.write(f"You selected: {number_input}")

# Add a checkbox
checkbox_option = st.checkbox("Show additional information")

# Conditional rendering based on checkbox state
if checkbox_option:
    st.write("Here is some additional information.")

# Add a selectbox
options = ["Option 1", "Option 2", "Option 3"]
selected_option = st.selectbox("Choose an option", options)
st.write(f"You selected: {selected_option}")

# Add a file uploader
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "pdf"])
if uploaded_file is not None:
    st.write("File uploaded successfully!")

# Add a date input
selected_date = st.date_input("Select a date", min_value="2022-01-01", max_value="2024-12-31")
st.write(f"You selected: {selected_date}")
