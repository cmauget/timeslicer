from slicer.Slicing import Slicing
from PIL import Image #type: ignore
import sys, getopt

def loard_arg(argv):
   
    inputStr = 'input/'
    outputStr = 'output/'
    disp = True
    opts, args = getopt.getopt(argv,"hi:o:vd",["ifile=","ofile=", "video" ,"display"])
    vid = False

    for opt, arg in opts:
        if opt == '-h':
            print ('main.py -d show the image at the end -i <inputfolder> -o <outputfolder>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputStr = arg
        elif opt in ("-o", "--ofile"):
            outputStr = arg
        elif opt in ("-v", "--video"):
            vid = True
        elif opt in ("-d", "--display"):
            disp=False

    return inputStr, outputStr, vid, disp

if __name__=='__main__':

    inputStr, outputStr, vid, disp = loard_arg(sys.argv[1:])

    s = Slicing()
    
    if not vid:
        image, _ = s.slice(inputStr, outputStr)
        if disp:
            image.show()
    else:
        s.silce_vid_cl( 25, inputStr, outputStr)