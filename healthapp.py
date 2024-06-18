import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image 
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_respsonse(input_prompt,image):
    model=genai.GenerativeModel('gemini-pro-vision')
    response =model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }

        ] 
        return image_parts
    else:
            raise FileNotFoundError("No file uploaded")

import streamlit as st
from PIL import Image

# Set page config
st.set_page_config(page_title="Your Dietitian", layout="wide")

# Use columns for layout
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Your Personal Dietitian")
    st.write("Check whether the food is healthy or not - Get Calorie and Nutrition count from an Image. Please upload your meal image below.")

with col2:
    uploaded_file = st.file_uploader("Choose an food image...", type=["jpg", "jpeg", "png"], help="Upload an image of your meal.")

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", width=300)

# Highlight the button with markdown
st.markdown("""
---
#### :arrow_down: Click Below to Analyze Your Meal :arrow_down:
---
""", unsafe_allow_html=True)

# Custom button with emoji
submit = st.button("🔍 Analyze Image", help="Click to analyze the uploaded meal image.")

# Optional: Add an expander for additional information or instructions
with st.expander("How does it work?"):
    st.write("""
        This application uses advanced image processing and nutritional analysis to evaluate your meal. 
        Just upload an image of your meal, and let us do the rest. You'll get information on calories, 
        nutritional content, and whether it fits into a healthy diet.
    """)

# Add some space after the button if needed
st.markdown("---")

  



# Optional: Use custom CSS to further customize (this is just an example, adjust as needed)
st.markdown("""
<style>
.stButton>button {
    color: white;
    background-color: #4CAF50;
    border-radius: 20px;
    border: 2px solid #4CAF50;
    font-size: 20px;
    font-weight: bold;
    padding: 10px 24px;
    margin: 10px 1px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)    

input_prompt="""
You are an expert in nutritionist where you need to see the food  items from image and calculate the total calories , also provide the details of every food items with calories intake  and quantity in below formate
1. Item-1.-----no of calories , (quantity)
2. Item-2.-----no of calories , (quantity)
---
----
finally you can also mention whether the food is healthy or not , if food is not detected then say food is not detected also count quantity of every food."""
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_respsonse(input_prompt, image_data)
    st.header("The Response is")
    st.write(response)
