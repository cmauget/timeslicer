from pathlib import Path
import PIL
import os
from PIL import Image, ImageDraw,ImageFont
from PIL.PngImagePlugin import PngInfo
from matplotlib import pyplot as plt
from matplotlib import image as mpimg


def compteur_de_photos(inputStr):
    num_derniere_photo = 0
    inputStr=inputStr.replace('\\', "/")
    for file in os.listdir(inputStr):
        num_derniere_photo += 1
    return num_derniere_photo

def folder(addr,rm=1):
    if os.path.exists(addr):
        if rm==1:
            for pic in os.listdir(addr):
                os.remove(addr+"/"+pic)
    else:
        creerDossiers(addr)
        
def creerDossiers(addr):
    if not os.path.exists(addr):
        i=len(addr)
        while addr[i-1]!="/" and i>0:  #conditons limites
            i-=1
        if i==0:
            print("la racine n'existe pas")
        else:
            parent = addr[:i-1]  #on teste le dossier parent dans l'adresse
            creerDossiers(parent)
            if os.path.exists(parent):
                os.mkdir(addr)


def ajustement_nb_photos(mode,nb_bandes,num_derniere_photo,num_premiere_photo): 
    if mode<=1: #centré
        if nb_bandes%2==0:
            nb_bandes+=1  #permet une symétrie
        nb_photos=int((nb_bandes-1)/2+1)
    else:  #linéaire
        nb_photos=nb_bandes  
    num_derniere_photo_opti = num_derniere_photo-(num_derniere_photo-num_premiere_photo)%(nb_photos-1)            #numéro dernière photo #here

    return nb_photos,num_derniere_photo_opti,nb_bandes

def choix_fond(mode,num_derniere_photo_opti,num_premiere_photo): 

    if mode== 0:
        num_fond=num_derniere_photo_opti
    else:
        num_fond=num_premiere_photo
    fond = Image.open(inputStr+"/"+os.listdir(inputStr)[num_fond])
    largeur, hauteur = fond.size
    
    if mode ==2: # gd
        overlay = Image.open(inputStr+"/"+os.listdir(inputStr)[num_derniere_photo_opti])  
        overlaycrop = overlay.crop((largeur//2,0,largeur,hauteur))
        corner=(largeur//2,0)
        fond.paste(overlaycrop,corner)
    elif mode ==3: # dg
        overlay = Image.open(inputStr+"/"+os.listdir(inputStr)[num_derniere_photo_opti])  
        overlaycrop = overlay.crop((0,0,largeur//2,hauteur))
        corner=(0,0)
        fond.paste(overlaycrop,corner)
    
    return fond, largeur, hauteur

def preparation_decoupage(largeur, nb_bandes, num_derniere_photo_opti,nb_photos,num_premiere_photo):

    largeur_bande = largeur//nb_bandes     
    print("nb photo : ", nb_photos)                                        
    pas_photos=(num_derniere_photo_opti-num_premiere_photo)//(nb_photos-1)
    espace_residuel=int((largeur%(nb_bandes))/2)                                
    return largeur_bande,pas_photos,espace_residuel

def choix_photo_iteration(mode,nb_photos,pas_photos,n_iteration,num_premiere_photo):
    if mode ==0 or mode== 3:
        return num_premiere_photo+pas_photos*(nb_photos-n_iteration-1)  #commence par la fin
    else :
        return num_premiere_photo+pas_photos*(n_iteration)  #commence par le debut


        
def overlay_cropNpaste(fond,overlay,mode,espace_residuel,largeur,largeur_bande,n_iteration,hauteur):

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


def rognage_residus(image,residu,largeur,hauteur):
    image=image.crop((residu//2,0,largeur-residu//2,hauteur))
    return image



def composition(nb_bandes,num_derniere_photo,num_premiere_photo,itere=0,mode=0,premiere_iteration=0,rognage=0):
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
        nb_photos,num_derniere_photo_opti,nb_bandes = ajustement_nb_photos(mode,nb_bandes,num_derniere_photo,num_premiere_photo)
        fond,largeur,hauteur = choix_fond(mode,num_derniere_photo_opti,num_premiere_photo)                                 
        
        print("num opti",num_derniere_photo_opti)
        print("num premiere photo ", num_premiere_photo)

        largeur_bande,pas_photos,espace_residuel=preparation_decoupage(largeur, nb_bandes, num_derniere_photo_opti,nb_photos,num_premiere_photo)
        print("pas photo :", pas_photos)
        for i in range(1,nb_photos):  #on itère sur toutes les photos à couper/coller
            photo_utilisee=choix_photo_iteration(mode,nb_photos,pas_photos,i,num_premiere_photo)
            print("photo utilisée",photo_utilisee)
            overlay = Image.open(inputStr+"/"+os.listdir(inputStr)[photo_utilisee])
            fond=overlay_cropNpaste(fond,overlay,mode,espace_residuel,largeur,largeur_bande,i,hauteur)
            if affichage_progressif:
                fond.show()
            print(str(round(100*(i)/nb_photos))+" %")  #avancement du traitement de la photo
        print("100 %")
    if rognage:
        fond = rognage_residus(fond,espace_residuel,largeur,hauteur)
    noms_modes=["centré_sur_le_début","centré_sur_la_fin","de_gauche_à_droite","de_droite_à_gauche"]
    if itere:
        outputImgAddr = outputStr+"/itéré/"+noms_modes[mode]
        if premiere_iteration:
            folder(outputImgAddr,rm=1) #préparation du dossier
    else:
        print("Slicing terminé !")
        outputImgAddr = outputStr+"/seul/"+noms_modes[mode]
        folder(outputImgAddr,rm=0)
    outputImg = outputImgAddr+"/"+str(nb_bandes)+"_bandes.png"
    
    print("Enregistrement...")
    metadata=pngInfoWriter()#type: ignore
    fond.save(outputImg, pnginfo=metadata)   #sauvegarde de la composition
    print("Enregistrement fini !")
    if affichage_final and not affichage_progressif:
        image = mpimg.imread(outputImg)
        plt.imshow(image)
        plt.show()
        #os.startfile(outputImg)
        #os.startfile(outputImgAddr)
    #return(outputImgAddr)


if __name__=='__main__':

    inputStr="input" 
    outputStr="output"

    num_premiere_photo = 0
    num_derniere_photo = 5      
    print(compteur_de_photos(inputStr))


    affichage_progressif=0
    affichage_final=1
    ouvrir_dossier_sortie=1
    facteur_iteration = 1.4          #mettre au moins une des deux valeurs !=0, facteur prioritaire au pas
    pas_itération = 0

    composition(6,num_derniere_photo,num_premiere_photo,itere=0,mode=3,premiere_iteration=0,rognage=0)