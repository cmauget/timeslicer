import os
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from scripts.Img_process import Img_process
import ffmpeg #type: ignore

class Data_process:

    def __init__(self) :
        pass


    def create_folder(self,addr):
        if not os.path.exists(addr):
            i=len(addr)
            while addr[i-1]!="/" and i>0:
                i-=1
            if i==0:
                print("root doesn't exists")
            else:
                parent = addr[:i-1] 
                self.create_folder(parent)
                if os.path.exists(parent):
                    os.mkdir(addr)


    def folder(self,addr,rm=1):
        if os.path.exists(addr):
            if rm==1:
                for img in os.listdir(addr):
                    os.remove(addr+"/"+img)
        else:
            self.create_folder(addr)


    def pngInfoWriter(self):
        metadata = PngInfo()
        metadata.add_text("Properties", "sliced w/ timelapse-slicer")
        return metadata


    def save_pic(self, fileName, img):
    
        print("Saving...", fileName)
        metadata=self.pngInfoWriter()
        img.save(fileName, pnginfo=metadata)   
        print("Saved !")

    
    def folder_to_vid(self, iter, outputImgAddr):

        if iter<10:
            v=f'0{iter}'
        else:
            v=iter

        outputImgAddr=outputImgAddr+"/vid/"
        self.folder(outputImgAddr,rm=0)
        fileName = outputImgAddr+"image"+str(v)+".png" 

        return fileName


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
  