from PIL import Image

import os
import numpy as np

import streamlit as st#type: ignore

from slicer.Data_process import Data_process
from slicer.Align_cv import Align_cv
from slicer.Img_list import Img_list

import ffmpeg #type: ignore


class Slicing:

    def __init__(self):

        self.imgList = Img_list()
        self.background = None


    def create_bg(self): 

        width, height = self.imgList.get_Max_Size()
        print(width)
        print(height)
        bg = Image.new(mode="RGB", size=(width, height))
        self.background = bg
        
        

    def pre_slice(self):
        nb_bandes =self.get_Nb_Bandes()
        largeur, _ = self.imgList.get_Max_Size()
        largeur_bande = largeur//nb_bandes 
        nb_img = self.imgList.get_Nb_Img()    
        #print("nb photo : ", nb_img)                                        
        espace_residuel=int((largeur%(nb_bandes))/2)                                
        return largeur_bande, espace_residuel


    def get_Iter_Img(self,n_iteration):

        img = self.imgList[n_iteration]
    
        return img  

    def get_Nb_Bandes(self):
        return self.imgList.get_Nb_Img()

      
    def overlay_cropNpaste(self, espace_residuel, largeur_bande, iter, debug=False, decalage=0):

        largeur, hauteur = self.imgList.get_Max_Size()
        borneagauche = (espace_residuel+largeur_bande*iter+decalage)
        remise = (borneagauche//largeur)       
        
        if debug:
            print(remise)
            print(type(self.background)) 

        borneagauche = borneagauche - remise*largeur
        borneadroite = (espace_residuel+largeur_bande*(iter+1)+decalage) - remise*largeur

        if debug:
            print(largeur)
            print("b1 "+str(borneagauche))
            print("d1 "+str(borneadroite))
        
        if ((decalage != 0) and (borneadroite > largeur) and (borneagauche <= largeur)):
            self.imgList.get_I(iter).set_Border(borneagauche, 0, largeur, hauteur)
            overlaycrop1 = self.imgList.get_I(iter).crop_Img()
            corner1=(borneagauche,0)

            nv_borneadroite = borneadroite - largeur
            self.imgList.get_I(iter).set_Border(0, 0, nv_borneadroite, hauteur)
            overlaycrop2 = self.imgList.get_I(iter).crop_Img()
            corner2=(0,0)

            self.background.paste(overlaycrop1,corner1)
            self.background.paste(overlaycrop2,corner2)
 
        elif ((decalage != 0) and (borneadroite > largeur) and (borneagauche > largeur)):

            nv_borneagauche = borneagauche - largeur
            nv_borneadroite = borneadroite - largeur

            self.imgList.get_I(iter).set_Border(nv_borneagauche, 0, nv_borneadroite, hauteur)
            overlaycrop = self.imgList.get_I(iter).crop()
            corner=(nv_borneagauche,0)

            self.background.paste(overlaycrop, corner)
            
            
        else :

            self.imgList.get_I(iter).set_Border(borneagauche, 0, borneadroite, hauteur)
            overlaycrop = self.imgList.get_I(iter).crop_Img()
            corner=(borneagauche,0)

            self.background.paste(overlaycrop,corner)

        
        if debug:
            print("b2 ",borneagauche)
            print("d2 ",borneadroite)



    def rognage_residus(self,image,residu):
        largeur, hauteur = self.imgList.get_Max_Size()
        image=image.crop((residu//2,0,largeur-residu//2,hauteur))
        return image

    def easeInSine(self, x):
        return (1 - np.cos((x*np.pi)/2))

    def linear(self, x):
        return x

    def easeInOutCubic(self, x):
        if x < 0.5:
            x = 4 * x * x * x 
        else :
            x = 1 - pow(-2 * x + 2, 3) / 2
        return x

    def decal_Img(self, iter, frames: int, cycle: int,  func , mode = 1):

        largeur, _ = self.imgList.get_Max_Size()
        ratio =  cycle * largeur
        x = iter/frames
        decalage = int(func(x)*ratio)
        return decalage


    def decal_Frames(self, duration, fps):

        frames = int(duration*fps)
        return frames



    def slice(self,  inputStr, outputStr, func= linear, iter = 0, duration=0, cycle=0, frames=0, align=False,  rognage=True, vid=False, debug = False):
        
        if not vid:
            self.imgList.load_Img(inputStr)

        d=Data_process()
        

        if align : 
            a=Align_cv()
            imRef = a.loadRef(inputStr+"/"+os.listdir(inputStr)[0])
            a.saveIm(imRef, "aligned/"+os.listdir(inputStr)[0])

            for i in range(self.imgList.get_Nb_Img()-1):
                im = a.loadIm(inputStr+"/"+os.listdir(inputStr)[i+1])
                imReg, h = a.alignImages(im, imRef)
                a.saveIm(imReg, "aligned/"+os.listdir(inputStr)[i+1])
                print("Estimated homography : \n",  h)
    
            inputStr = 'aligned'
        
        self.create_bg()  

        largeur_bande, espace_residuel = self.pre_slice()

        if vid:
            decalage = self.decal_Img(iter, frames, cycle, func)
        else:
            decalage=0

        for i in range(self.imgList.get_Nb_Img()):  
            photo_utilisee=i
            print("photo utilisée : ",photo_utilisee)
            print(inputStr+os.listdir(inputStr)[photo_utilisee])
            self.overlay_cropNpaste(espace_residuel,largeur_bande,i, decalage=decalage)
            print(str(round(100*(i)/self.imgList.get_Nb_Img()))+" %")  #avancement du traitement de la photo
        print("100 %")

        if rognage:
            fond = self.rognage_residus(self.background,espace_residuel)
        
        print("Slicing terminé !")
        outputImgAddr = outputStr

        if vid:
            outputImgAddr=outputImgAddr+".vid/"
            outputImg = d.folder_to_vid(iter, outputImgAddr)

        else : 
            d.folder(outputImgAddr,rm=0)
            outputImg = outputImgAddr+str(self.get_Nb_Bandes())+"_bandes.png"
        
        d.save_pic(outputImg, fond)
        return fond, outputImgAddr


    def silce_vid(self, fps, inputStr, outputStr, func=linear, duration = 2, cycle= 1, align=False,  rognage=True, debug = False, height = 4092, width = 2160):

        d = Data_process()

        self.imgList.load_Img(inputStr)
        self.imgList.resize_Img_list(height=height, width=width)

        frames = self.decal_Frames(duration, fps)

        
        mybar = st.progress(0)
        for i in range (frames):
            p = ((i/frames)*100)+1
            mybar.progress(int(p))
            _ , inputStr_vid = self.slice( inputStr, outputStr, func=func, iter = i, duration= duration, frames= frames, cycle=cycle, align=align, vid = True)

        d.save_to_vid(inputStr_vid, outputStr, fps)
        d.folder(inputStr_vid, rm=True)
  