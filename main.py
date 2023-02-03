from scripts.Slicing import Slicing
import os

if __name__=='__main__':

    s = Slicing()

    num_premiere_photo = 0
    num_derniere_photo = 2
    inputStr = "input"
    outputStr = "output"
    nb_bandes = (num_derniere_photo-num_premiere_photo)+1
    m=2


#    for i in range(100):
#       s.slice(nb_bandes, num_derniere_photo, num_premiere_photo, inputStr, outputStr, mode=m, iter=i, vid=True)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    s.save_to_vid(dir_path+"/"+outputStr+"/de_gauche_à_droite/vid/", "output/")