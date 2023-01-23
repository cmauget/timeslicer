from PIL import Image
import os

class Pre_process:

    def __init__(self,inputStr) -> None:
        self.inputStr = inputStr
        pass

    def ajustement_nb_photos(self,mode,nb_bandes,num_derniere_photo,num_premiere_photo): 
        if mode<=1: #centré
            if nb_bandes%2==0:
                nb_bandes+=1  #permet une symétrie
            nb_photos=int((nb_bandes-1)/2+1)
        else:  #linéaire
            nb_photos=nb_bandes  
        num_derniere_photo_opti = num_derniere_photo-(num_derniere_photo-num_premiere_photo)%(nb_photos-1)            #numéro dernière photo #here

        return nb_photos,num_derniere_photo_opti,nb_bandes

    def choix_fond(self,mode,num_derniere_photo_opti,num_premiere_photo): 

        if mode== 0:
            num_fond=num_derniere_photo_opti
        else:
            num_fond=num_premiere_photo
        fond = Image.open(self.inputStr+"/"+os.listdir(self.inputStr)[num_fond])
        largeur, hauteur = fond.size
        
        if mode ==2: # gd
            overlay = Image.open(self.inputStr+"/"+os.listdir(self.inputStr)[num_derniere_photo_opti])  
            overlaycrop = overlay.crop((largeur//2,0,largeur,hauteur))
            corner=(largeur//2,0)
            fond.paste(overlaycrop,corner)
        elif mode ==3: # dg
            overlay = Image.open(self.inputStr+"/"+os.listdir(self.inputStr)[num_derniere_photo_opti])  
            overlaycrop = overlay.crop((0,0,largeur//2,hauteur))
            corner=(0,0)
            fond.paste(overlaycrop,corner)
        
        return fond, largeur, hauteur

    def preparation_decoupage(self,largeur, nb_bandes, num_derniere_photo_opti,nb_photos,num_premiere_photo):

        largeur_bande = largeur//nb_bandes     
        print("nb photo : ", nb_photos)                                        
        pas_photos=(num_derniere_photo_opti-num_premiere_photo)//(nb_photos-1)
        espace_residuel=int((largeur%(nb_bandes))/2)                                
        return largeur_bande,pas_photos,espace_residuel

    def choix_photo_iteration(self,mode,nb_photos,pas_photos,n_iteration,num_premiere_photo):
        
        if mode ==0 or mode== 3:
            return num_premiere_photo+pas_photos*(nb_photos-n_iteration-1)  #commence par la fin
        else :
            return num_premiere_photo+pas_photos*(n_iteration)  #commence par le debut
