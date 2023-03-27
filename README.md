# Timelapse Slicer

A simple python script to create "timeslices" 

<h3 align="center">
<a href="url"><img src="https://github.com/cmauget/timeslicer/blob/master/output/ex.png" height="250" width="500"></a>
</h3>  

---
<h3 align="center">
    🎈 Try it out here: <a href="https://timeslicer.streamlit.app/">timeslicer on streamlit 🎈 </a>
</h3>

---

## Local Setup

First, you will need to download the zip, extract it, and move to the root of this repo using the _cd_ command. It is recommended to use it in a venv (using conda for example)

### On ubuntu 

To install everything:

    make setup  
    
### On windows

You will need to install all the dependencies by launching the command (td add ffmpeg-python):  

    pip install -r requirements.txt
  
In order to create animated video, you will also need to install ffmepg. It is a bit more complicated, and I recommend this [guide](https://phoenixnap.com/kb/ffmpeg-windows)

# How to use it  

It is recommended to put your pictures in the input folder as below :

```
📂 timelapse-slicer/ # this is root
├── 📂 input/
|       ├── 📜 image1.jpg
|       |...
│...
```  
You can also use the absolute path in the enter input file here later  

_Note : the files have to be in alphabetical order relatively to the time they were taken in order to produce coherent results_

and then launch the web app using (on ubuntu) :

    make run  
    
and on windows :
    
    streamlit run streamlit_timeslicer/app.py
    
A new window will open in your browser, if not use the "localhost" link given in the terminal.  
In order to create a video check the video output box and complete the informations.
Click the run me button and enjoy ! 
