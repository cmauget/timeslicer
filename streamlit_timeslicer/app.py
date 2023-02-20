import streamlit as st#type: ignore
from PIL import Image

import sys
import os

folder = os.path.dirname(__file__)
sys.path.append(folder+"/..")

from slicer.Slicing import Slicing

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
inputStr = st.sidebar.text_input("Enter input folder", value="input/")
outputStr = st.sidebar.text_input("Enter output folder", value="output/")
vid = st.sidebar.checkbox("Video Output")

if vid:
    funcoption = [ "linear", "easeInSine", "easeInOutCubic"]
    funclist=[ s.linear, s.easeInSine, s.easeInOutCubic]
    frame_rate = st.sidebar.number_input("Enter wanted fps", min_value=0, max_value=60, value=25)
    duration = st.sidebar.slider("Choose wanted duration ", min_value=1, max_value=30, value=5, step=1)
    cycle = st.sidebar.number_input("Choose wanted number of cycle ", min_value=1, max_value=30, value=1)
    height = st.sidebar.number_input("Enter height resolution", min_value=1,  max_value=4092, value = 1920)
    width = st.sidebar.number_input("Enter width resolution", min_value=1, max_value=2160, value = 1080)
    funcname = st.sidebar.selectbox("Choose the easing option", options = funcoption)

if st.sidebar.button("Stop"):
    st.stop()

result_container = st.empty()

button = st.button("Run me")


if not runed:
    place_holder = st.empty()
    if vid:
        video_file = open('video.mp4', 'rb')
        video_bytes = video_file.read()
        place_holder.video(video_bytes)
    else:
        img= Image.open("output/3_bandes.png")
        place_holder.image(img)

if button:

    if vid:
        func = funclist[funcoption.index(funcname)]
        print(func)
        with st.spinner("Generating video, please wait..."):
            place_holder.empty()
            s.silce_vid( frame_rate, inputStr, outputStr, func=func, duration=duration, cycle=cycle, height=height, width=width)
        video_file = open(f'{outputStr}/video.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

    else:
        with st.spinner("Please wait.."):
            place_holder.empty()
            runed = True
            img, _ = s.slice( inputStr, outputStr)
        st.image(img, caption="Output image")
    st.balloons()

st.markdown("---")

st.write(
    "Feel free to share on social media !"
)
st.markdown(
    "More infos and :star: at [github.com/cmauget/timelapse-slicer](https://github.com/cmauget/timelapse-slicer)"
)
