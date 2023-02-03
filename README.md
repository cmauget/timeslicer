# Timelapse Slicer

A simple python script for making timeslices

## Setup

You will need to install all the dependencies by launching the command (td add ffmpeg-python):  

    pip install -r requirements.txt
  
In order to create animated video you will also need to install ffmepg using the command :

    sudo apt install ffmpeg

You will have to upload your pictures in the input folder :

```
📂 timelapse-slicer/ # this is root
├── 📂 input/
|       ├── 📜 image1.jpg
|       |...
│...
```

and then lauch the main.py script :

    python3 main.py
