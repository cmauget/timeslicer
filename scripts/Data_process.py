import os
from PIL.PngImagePlugin import PngInfo
import ffmpeg

class Data_process:

    def __init__(self) -> None:
        pass

    def compteur_de_photos(self,inputStr):
        num_derniere_photo = 0
        inputStr=inputStr.replace('\\', "/")
        for file in os.listdir(inputStr):
            num_derniere_photo += 1
        return num_derniere_photo

    def creerDossiers(self,addr):
        if not os.path.exists(addr):
            i=len(addr)
            while addr[i-1]!="/" and i>0:  #conditons limites
                i-=1
            if i==0:
                print("la racine n'existe pas")
            else:
                parent = addr[:i-1]  #on teste le dossier parent dans l'adresse
                self.creerDossiers(parent)
                if os.path.exists(parent):
                    os.mkdir(addr)


    def folder(self,addr,rm=1):
        if os.path.exists(addr):
            if rm==1:
                for pic in os.listdir(addr):
                    os.remove(addr+"/"+pic)
        else:
            self.creerDossiers(addr)

    def pngInfoWriter(self, num_premiere_photo, num_derniere_photo):
        texte = "num_premiere_photo = "+str(num_premiere_photo)
        texte+= ", num_derniere_photo = "+str(num_derniere_photo)
        #texte+= ", bandes = "+str(bandes)
        metadata = PngInfo()
        metadata.add_text("Propriétés",texte)
        return metadata

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
  