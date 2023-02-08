from scripts.Slicing import Slicing
from scripts.Img_list import Img_list
import os

if __name__=='__main__':

    inputStr = "input/"
    outputStr = "output/"
    nb_bandes = 3

    imgList = Img_list()

    s = Slicing(nb_bandes, imgList)
    
    s.slice(nb_bandes, inputStr, outputStr)

    '''
    dir_path = os.path.dirname(os.path.realpath(__file__))
    s.save_to_vid(dir_path+"/"+outputStr+"/de_gauche_à_droite/vid/", "output/")'''