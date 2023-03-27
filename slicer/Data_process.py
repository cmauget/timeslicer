import os
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from slicer.Img_process import Img_process
import ffmpeg #type: ignore

class Data_process:

    def __init__(self) :
        pass


    def create_folder(self,addr):
        os.mkdir(addr)
        '''
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
        '''

    def folder(self,addr,rm=True):
        if os.path.exists(addr):
            if rm:
                for img in os.listdir(addr):
                    os.remove(addr+"/"+img)
        else:
            self.create_folder(addr)


    def pngInfoWriter(self):
        metadata = PngInfo()
        metadata.add_text("Properties", "sliced w/ timelapse-slicer")
        return metadata


    def save_pic(self, fileName, img):
    
        #print("Saving...", fileName)
        metadata=self.pngInfoWriter()
        img.save(fileName, pnginfo=metadata)   
        #print("Saved !")
    

    
    def folder_to_vid(self, iter, outputImgAddr):

        if iter<10:
            v=f'0{iter}'
        else:
            v=iter

        self.folder(outputImgAddr,rm=0)
        fileName = outputImgAddr+f"image{v}.png" 

        return fileName


    def save_to_vid(self, inputStr, outputStr, fps=25):

        (
            ffmpeg
            .input(inputStr+'image%02d.png', framerate=fps)
            .output(outputStr+'video.mp4', pix_fmt='yuv420p', vcodec='libx264')
            .run(overwrite_output=True)
        )
  