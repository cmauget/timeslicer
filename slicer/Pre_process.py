from PIL import Image, ImageDraw
from slicer.Img_list import Img_list
import os

class Pre_process:

    def __init__(self, imgList1: Img_list):
        self.imgList = imgList1

    def create_bg(self): 
   
        width, height = self.imglist.get_Max_Size()
        background = Image.new(mode="RGB", size=(width, height))
        
        return background


    def pre_slice(self, nb_bandes):

        largeur, _ = self.imgList.get_Max_Size()
        largeur_bande = largeur//nb_bandes 
        nb_img = self.imgList.get_Nb_Img()    
        #print("nb photo : ", nb_img)                                        
        espace_residuel=int((largeur%(nb_bandes))/2)                                
        return largeur_bande, espace_residuel


    def get_Iter_Img(self,n_iteration):

        img = self.imgList[n_iteration]
    
        return img  
