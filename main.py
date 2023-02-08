from slicer.Slicing import Slicing
from PIL import Image
import os

if __name__=='__main__':

    inputStr = "input/"
    outputStr = "output/"
    nb_bandes = 3

    s = Slicing(nb_bandes)
    
    image, _ = s.slice(nb_bandes, inputStr, outputStr)
    image.show()

    s.silce_vid(nb_bandes, 25, inputStr, outputStr)

    '''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    s.save_to_vid(dir_path+"/"+outputStr+"/de_gauche_à_droite/vid/", "output/")'''