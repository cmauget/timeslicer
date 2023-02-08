from PIL import Image
import os

from scripts.Pre_process import Pre_process
from scripts.Data_process import Data_process
from scripts.Align_cv import Align_cv
from scripts.Img_list import Img_list

import ffmpeg #type: ignore


class Slicing:

    def __init__(self, nbBandes1, imgList1: Img_list):

        self.nbBandes = nbBandes1
        self.imgList = imgList1
        self.background = None


    def create_bg(self): 

        width, height = self.imgList.get_Max_Size()
        print(width)
        print(height)
        bg = Image.new(mode="RGB", size=(width, height))
        self.background = bg
        
        

    def pre_slice(self, nb_bandes):

        largeur, _ = self.imgList.get_Max_Size()
        largeur_bande = largeur//nb_bandes 
        nb_img = self.imgList.get_Nb_Img()    
        print("nb photo : ", nb_img)                                        
        espace_residuel=int((largeur%(nb_bandes))/2)                                
        return largeur_bande, espace_residuel


    def get_Iter_Img(self,n_iteration):

        img = self.imgList[n_iteration]
    
        return img  

      
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


    def save_to_vid(self, inputStr, outputStr, fps=25):
        '''
        for i in range(10):
            im = Image.open(inputStr+f'image{i}.png')
            w, h = im.size
            h = h - h % 2
            im = im.resize((w, h))
            im.save(inputStr+f'image{i}.png')
        

        TARGET_WIDTH = 4092
        TARGET_HEIGHT = 2160

        for i in range(70):
            if i<10:
                v=f'0{i}'
            else:
                v=i
            im = Image.open(inputStr+f'image{v}.png')
            w, h = im.size
            if w != TARGET_WIDTH or h != TARGET_HEIGHT:
                #TODO get ratio
                im = im.resize((TARGET_WIDTH, TARGET_HEIGHT))
            im.save(inputStr+f'image{v}.png')
        '''

        (
            ffmpeg
            .input(inputStr+'image%02d.png', framerate=24)
            .output('video.mp4', pix_fmt='yuv420p', vcodec='libx264')
            .run()
        )


    def slice(self, nb_bandes,  inputStr, outputStr, iter = 0, align=False,  premiere_iteration=0, rognage=True, vid=False, debug = False):
        
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

        largeur_bande, espace_residuel = self.pre_slice(nb_bandes)

        for i in range(self.imgList.get_Nb_Img()):  
            photo_utilisee=i
            print("photo utilisée : ",photo_utilisee)
            #overlay = self.imgList.get_Img(i)
            print(inputStr+os.listdir(inputStr)[photo_utilisee])
            decalage = iter*10
            self.overlay_cropNpaste(espace_residuel,largeur_bande,i, decalage=decalage)
            print(str(round(100*(i)/self.imgList.get_Nb_Img()))+" %")  #avancement du traitement de la photo
        print("100 %")

        if rognage:
            fond = self.rognage_residus(self.background,espace_residuel)

        #noms_modes=["c_b","c_e","l_r","r_l"]
        
        print("Slicing terminé !")
        outputImgAddr = outputStr

        if vid:
            outputImg = d.folder_to_vid(iter, outputImgAddr)

        else : 
            d.folder(outputImgAddr,rm=0)
            outputImg = outputImgAddr+str(nb_bandes)+"_bandes.png"
        
        d.save_pic(outputImg, fond)


    def silce_vid(self, nb_bandes, num_derniere_photo, num_premiere_photo, inputStr, outputStr, decalage = 0, align=False, itere=False , premiere_iteration=0,rognage=True, disp = False, affichage_progressif=False):

        for i in range (100):
            self.slice(nb_bandes, num_derniere_photo, num_premiere_photo, inputStr, outputStr, iter = i, align=False, itere=False, vid = True)
  