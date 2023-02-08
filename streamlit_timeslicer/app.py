import streamlit as st#type: ignore
from PIL import Image

import sys
sys.path.append("../")
from slicer.Slicing import Slicing

st.set_page_config(
    page_title="Timeslicer",
    page_icon=":camera:",
)

runed =False

st.title("Timeslicer :camera:")
st.caption("A time slicing tool, free and for everyone to use")

st.markdown("---")

st.sidebar.title("Settings :wrench:")
inputStr = st.sidebar.text_input("Enter input folder", value="../input/")
outputStr = st.sidebar.text_input("Enter output folder", value="../output/")
vid = st.sidebar.checkbox("Video Output")

if vid:
    frame_rate = st.sidebar.number_input("Enter wanted fps", min_value=0, max_value=60, value=25)
    duration = st.sidebar.slider("Choose wanted duration ", min_value=1, max_value=30, value=5, step=1)
    cycle = st.sidebar.slider("Choose wanted number of cycle ", min_value=1, max_value=30, value=1, step=1)

if st.sidebar.button("Stop"):
    st.stop()

result_container = st.empty()

button = st.button("Run me")


if not runed:
    place_holder = st.empty()
    if vid:
        video_file = open('../video.mp4', 'rb')
        video_bytes = video_file.read()
        place_holder.video(video_bytes)
    else:
        img= Image.open("../output/3_bandes.png")
        place_holder.image(img)

if button:
    nb_Slice=3
    s = Slicing(nb_Slice)
    if vid:
        with st.spinner("Generating video, please wait..."):
            place_holder.empty()
            s.silce_vid(nb_Slice, frame_rate, inputStr, outputStr, duration=duration, cycle=cycle)
        video_file = open(f'{outputStr}/video.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

    else:
        with st.spinner("Please wait.."):
            place_holder.empty()
            runed = True
            img, _ = s.slice(nb_Slice, inputStr, outputStr)
        st.image(img, caption="Output image")
    st.balloons()

st.markdown("---")

st.write(
    "Share on social media !"
)
st.markdown(
    "More infos and :star: at [github.com/cmauget/timelapse-slicer](https://github.com/cmauget/timelapse-slicer)"
)
