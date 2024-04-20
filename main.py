import streamlit as st
import requests
import base64
from PIL import Image
from io import BytesIO

# Function to encode the image from an uploaded file or taken picture
def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Streamlit UI
st.title('EasyGains')
st.write('Upload An Image Of Your Meal For A Full Nutritional Analysis')

if 'take_pic' not in st.session_state:
    st.session_state['take_pic'] = False

if st.button('Take A Picture With Your Device Camera'):
    st.session_state['take_pic'] = True

if st.session_state['take_pic']:
    takeapic = st.camera_input('Capture your meal')
    if takeapic is not None:
        st.session_state['captured_image'] = takeapic

uploaded_file = st.file_uploader('Upload From Your Device', type=['png', 'jpg', 'jpeg', 'heic', 'heif'], label_visibility='collapsed')

if st.button('Click Here To Analyze'):
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
    elif 'captured_image' in st.session_state and st.session_state['captured_image'] is not None:
        image = Image.open(st.session_state['captured_image'])
    
    if image is None:
        st.error("Please upload a photo or take one to provide analysis.")
        st.stop()

    # Encode the uploaded or taken image
    base64_image = encode_image(image)

    apikey = st.secrets["apikey"]
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {apikey}"
    }

    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": "please describe the nutritional information of the following image, please include total calories (not in kcals) as well as how many grams of protein, carbs, and fats, the meal in the image has"
        },
        {
          "role": "system",
          "content": f"data:image/jpeg;base64,{base64_image}"
        }
      ],
      "max_tokens": 300
    }

    # Send the request to OpenAI
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()

    try:
      content = response_data['choices'][0]['message']['content']
      st.write(content)
    except (KeyError, IndexError, TypeError):
      st.error("There was an error processing the response from OpenAI.")

