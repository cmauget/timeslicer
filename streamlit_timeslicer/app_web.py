import streamlit as st #type: ignore
from PIL import Image #type: ignore

import sys
import os
import io

folder = os.path.dirname(__file__)
sys.path.append(folder+"/..")

from slicer.Slicing_web import Slicing

st.set_page_config(
    page_title="Timeslicer",
    page_icon=":camera:",
)

s = Slicing()

runed =False

st.title("Timeslicer :camera:")
st.caption("A time slicing tool, free and for everyone to use")

st.markdown("---")

st.sidebar.title("Settings :wrench:")

uploaded_files = st.sidebar.file_uploader("Choose an image file", type=["png","jpg"], accept_multiple_files=True)

for img in os.listdir('input'):
        os.remove("input/"+img)

    
if uploaded_files!=[]:

    for img in os.listdir('input'):
        os.remove("input/"+img)
    
    print("saving image")
    for uploaded_file in uploaded_files:
        data = uploaded_file.read()
        image = Image.open(io.BytesIO(data))
        i=uploaded_file.name
        image.save(f"input/{i}")
        

outputStr = "output/"
inputStr = "input"
vid = st.sidebar.checkbox("Video Output")

if vid:
    with st.sidebar:
        funcoption = [ "linear", "easeInSine", "easeInOutCubic"]
        funclist=[ s.linear, s.easeInSine, s.easeInOutCubic]
        frame_rate = st.number_input("Enter wanted fps", min_value=0, max_value=60, value=25)
        duration = st.slider("Choose wanted duration (s)", min_value=1, max_value=30, value=5, step=1)
        cycle = st.number_input("Choose wanted number of cycle ", min_value=1, max_value=30, value=1)
        col1, col2 = st.columns(2)
        with col1:
            height = st.number_input("Enter height resolution", min_value=1,  max_value=4092, value = 1920)
        with col2:
            width = st.number_input("Enter width resolution", min_value=1, max_value=2160, value = 1080)
        funcname = st.selectbox("Choose the easing option", options = funcoption)

result_container = st.empty()

button = st.button("Run me")

if not runed:
    place_holder = st.empty()
    if vid:
        video_file = open('video.mp4', 'rb')
        video_bytes = video_file.read()
        place_holder.video(video_bytes)
    else:
        img= Image.open("output/ex.png")
        place_holder.image(img)


if button:

    if uploaded_files==[]:
        inputStr = "input_ex"

    if vid:
        func = funclist[funcoption.index(funcname)]
        with st.spinner("Generating video, please wait..."):
            place_holder.empty()
            s.silce_vid( frame_rate, inputStr, outputStr, func=func, duration=duration, cycle=cycle, height=height, width=width)
        video_file = open(f'{outputStr}/video.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
        st.sidebar.download_button("Download output video", video_bytes, "fixed.mp4", "video/mp4")

    else:
        with st.spinner("Please wait.."):
            place_holder.empty()
            runed = True
            img, _ = s.slice( inputStr, outputStr)
        st.image(img, caption="Output image")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        byte_im = buf.getvalue()

        st.sidebar.download_button("Download output image", byte_im, "fixed.png", "image/png")


st.markdown("---")

st.write("Feel free to share on social media !")

st.markdown(
    "More infos and :star: at [github.com/cmauget/timelapse-slicer](https://github.com/cmauget/timelapse-slicer)"
)

