import requests
import json
import streamlit as st
import google.generativeai as genai

from api_key import api_key
genai.configure(api_key=api_key)
#Configure the model generation settings
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",    
}
# Function to generate home dessign ideas using Google Generative AI API
def generate_design_idea(style,size,rooms):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )
    context = f'create a custom home design plan with the following details:\nStyle:{style}\nSize:{size}\nRooms:{rooms} '
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts":[
                    context
                ],
            },
        ]
    )
    response= chat_session.send_message(context)
    text=response.candidates[0].content if isinstance(response.candidates[0].content,str) else response.candidates[0].content.parts[0].text
    return text
# Function to fetch an image from lexica.art based on the design style
def fetch_image_from_pexels(style,):
    pexels_url = f"https://api.pexels.com/v1?q={style}"
    headers={"Authorization":api_key}
    response =requests.get(pexels_url,headers=headers)
    if response.status_code==200:
        try:
            data = response.json()
            if data['photos']:
                return data['photos'][0]['src']['medium']# OR "oroginal", "large2x", etc.
            else:
                return None
        except json. JSONDecodeError as e:
            print(f"Error decoding Json:{e}")
            return None
    else:
        print(f"Error fetching from Pexels:{response.status_code}")
        return None
# Streamlit UI for taking user inputs
st.title("Custom Home Design assistant")

# Textboxes for style,size,and number of rooms input 
style = st.text_input("Enter the home design style (e.g., Modern, rustic)")
size = st.text_input("Enter the size of the home (e.g., 2000sq ft)")
rooms = st.text_input("Enter the number of rooms")
# submit button
if st.button("Generate Design"):
    if style and size and rooms:
        design_idea = generate_design_idea(style,size,rooms)
        image_url = fetch_image_from_pexels(style)

        st.markdown("### Custom Home Design Idea ")
        st.markdown(design_idea)

        if image_url:
            st.image(image_url, caption="Design inspiration from Pexels.art")
        else:
            st.warning("no relevant images found on Pexels.art.")
    else:
        st.warning("Please fill in all the fields.")