# Timelapse Slicer

A simple python script for creating timeslices 

<a href="url"><img src="https://github.com/cmauget/timeslicer/blob/master/output/ex.png" height="250" width="500"></a>

## Setup

First you will need to move to the root of this git using the _cd_ command.

### On ubuntu 

To install everything:

    make setup  
    

### On windows

You will need to install all the dependencies by launching the command (td add ffmpeg-python):  

    pip install -r requirements.txt
  
In order to create animated video you will also need to install ffmepg. It is a bit more complicated and I recommend this [guide](https://phoenixnap.com/kb/ffmpeg-windows)


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

and then lauch the web app using (on ubuntu) :

    make run  
    
and on windows :
    
    streamlit run streamlit_timeslicer/app.py
    
A new window will open in your browser, if not use the "localhost" link given in the terminal.  
In order to create a video check the video output box and complte the informations.
The click run me

