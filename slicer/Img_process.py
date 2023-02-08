from PIL import Image

class Img_process:

    def __init__(self, fileName1: str):
        self.fileName = fileName1
        self.img = Image.open(self.fileName)
        self.width, self.height = self.img.size
        self.lBorder = 0
        self.rBorder = self.width
        self.tBorder = self.height
        self.bBorder = 0

    def set_Border(self, left: int, bottom: int, right: int, top: int):
        self.lBorder = left
        self.rBorder = right
        self.tBorder = top
        self.bBorder = bottom

    def get_Img(self):

        return self.img

    def get_Img_Size(self):

        w, h = self.img.size
        return w, h

    def get_Img_width(self):

        w, _ = self.img.size
        return w

    def get_Img_height(self):

        _, h = self.img.size
        return h
        
    def crop_Img(self):
        img_crop = self.img.crop((self.lBorder, self.bBorder, self.rBorder, self.tBorder))

        return img_crop

    def disp_Img(self):

        self.img.show()

    def resize_Img(self, height=4092, width=2160):

        if self.height != height or self.width != width:
            #TODO get ratio
            self.img = self.img.resize((width, height))
        

    

    

    