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
st.caption("A time slicing tool, free for everyone to use")

st.markdown("---")

st.sidebar.title("Settings :wrench:")
inputStr = st.sidebar.text_input("Enter input folder", value="../input/")
outputStr = st.sidebar.text_input("Enter output folder", value="../output/")
vid = st.sidebar.checkbox("Video Output")

if st.sidebar.button("Quit"):
    st.stop()

result_container = st.empty()

button = st.button("Run me")


if not runed:
    place_holder = st.empty()
    img= Image.open("../output/3_bandes.png")
    place_holder.image(img)

if button:

    s = Slicing(3)
    if vid:
        st.text("video enabled")
    with st.spinner("Please wait.."):
        place_holder.empty()
        runed = True
        img = s.slice(3, inputStr, outputStr)
    st.image(img, caption="Output image")
    st.balloons()

st.markdown("---")

st.write(
    "Share on social media !"
)
st.markdown(
    "More infos and :star: at [github.com/cmauget/timelapse-slicer](https://github.com/cmauget/timelapse-slicer)"
)
