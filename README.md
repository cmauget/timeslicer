# Timelapse Slicer

A simple python script for creating timeslices 

<a href="url"><img src="https://github.com/cmauget/timeslicer/blob/master/output/ex.png" height="250" width="500"></a>

## Setup

### The easy way 

To install everything:

    make setup  
    

### The hard way

You will need to install all the dependencies by launching the command (td add ffmpeg-python):  

    pip install -r requirements.txt
  
In order to create animated video you will also need to install ffmepg using the command :

    sudo apt install ffmpeg


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

and then lauch the web app using :

    make run  
    
A new window will open in your browser, if not use the "localhost" link given in the terminal.  
In order to create a video check the video output box and complte the informations.
The click run me

