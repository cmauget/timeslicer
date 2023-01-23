from PIL import Image
import os
from scripts.Pre_process import Pre_process
from scripts.Data_process import Data_process
from matplotlib import pyplot as plt
from matplotlib import image as mpimg

class Slicing:

    def __init__(self):
        pass

            
    def overlay_cropNpaste(self,fond,overlay,mode,espace_residuel,largeur,largeur_bande,n_iteration,hauteur):

        if mode<=1:
            overlaycrop1 = overlay.crop((espace_residuel+largeur_bande*n_iteration,0,espace_residuel+largeur_bande*(n_iteration+1),hauteur))
            overlaycrop2 = overlay.crop((largeur-espace_residuel-(n_iteration+1)*largeur_bande,0,largeur-espace_residuel-n_iteration*largeur_bande,hauteur))
            corner1=(espace_residuel+largeur_bande*n_iteration,0)
            corner2=(largeur-espace_residuel-(n_iteration+1)*largeur_bande,0)
            fond.paste(overlaycrop1,corner1)
            fond.paste(overlaycrop2,corner2)
        
        else:
            overlaycrop = overlay.crop((espace_residuel+largeur_bande*n_iteration,0,espace_residuel+largeur_bande*(n_iteration+1),hauteur))
            corner=(espace_residuel+largeur_bande*n_iteration,0)
            fond.paste(overlaycrop,corner)
        return fond


    def rognage_residus(self,image,residu,largeur,hauteur):
        image=image.crop((residu//2,0,largeur-residu//2,hauteur))
        return image



    def slice(self, nb_bandes, num_derniere_photo, num_premiere_photo, inputStr, outputStr, itere=False ,mode=0,premiere_iteration=0,rognage=0, disp = True, affichage_progressif=False):
        p=Pre_process(inputStr)
        d=Data_process()
        if nb_bandes==1:            #on se passe des différentes opérations s'il n'y a qu'une bande (évite des divisions par 0)
            if mode==1:
                numfond = num_premiere_photo         
            else:
                numfond=num_derniere_photo
            fond = Image.open(inputStr+"/"+os.listdir(inputStr)[numfond])
            print("nb photo", 1)
            print("num photo", numfond)
            if affichage_progressif:
                    fond.show()
        else:  #plusieurs bandes
            nb_photos,num_derniere_photo_opti,nb_bandes = p.ajustement_nb_photos(mode,nb_bandes,num_derniere_photo,num_premiere_photo)
            fond,largeur,hauteur = p.choix_fond(mode,num_derniere_photo_opti,num_premiere_photo)                                 
            
            print("num opti",num_derniere_photo_opti)
            print("num premiere photo ", num_premiere_photo)

            largeur_bande,pas_photos,espace_residuel=p.preparation_decoupage(largeur, nb_bandes, num_derniere_photo_opti,nb_photos,num_premiere_photo)
            print("pas photo :", pas_photos)
            for i in range(1,nb_photos):  #on itère sur toutes les photos à couper/coller
                photo_utilisee=p.choix_photo_iteration(mode,nb_photos,pas_photos,i,num_premiere_photo)
                print("photo utilisée",photo_utilisee)
                overlay = Image.open(inputStr+"/"+os.listdir(inputStr)[photo_utilisee])
                fond=self.overlay_cropNpaste(fond,overlay,mode,espace_residuel,largeur,largeur_bande,i,hauteur)
                if affichage_progressif:
                    fond.show()
                print(str(round(100*(i)/nb_photos))+" %")  #avancement du traitement de la photo
            print("100 %")
        if rognage:
            fond = self.rognage_residus(fond,espace_residuel,largeur,hauteur)
        noms_modes=["centré_sur_le_début","centré_sur_la_fin","de_gauche_à_droite","de_droite_à_gauche"]
        if itere:
            outputImgAddr = outputStr+"/itéré/"+noms_modes[mode]
            if premiere_iteration:
                d.folder(outputImgAddr,rm=1) #préparation du dossier
        else:
            print("Slicing terminé !")
            outputImgAddr = outputStr+"/"+noms_modes[mode]
            d.folder(outputImgAddr,rm=0)
        outputImg = outputImgAddr+"/"+str(nb_bandes)+"_bandes.png"
        
        print("Enregistrement...")
        print(outputImg)
        metadata=d.pngInfoWriter(num_premiere_photo, num_derniere_photo)
        fond.save(outputImg, pnginfo=metadata)   #sauvegarde de la composition
        print("Enregistrement fini !")
        if  disp:
            image = mpimg.imread(outputImg)
            plt.imshow(image)
            plt.show()