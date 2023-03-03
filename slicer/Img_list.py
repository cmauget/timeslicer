from slicer.Img_process import Img_process
import os

class Img_list:

    def __init__(self):
        self.imgList = []


    def load_Img(self, inputStr:str):

        self.imgList = []
        cwd = os.getcwd()
        #print(cwd)
        os.chdir(inputStr)

        for file in sorted(os.listdir()):
            self.imgList.append(Img_process(file))

        #print("Load complete")
        os.chdir(cwd)

    def get_Max_Size(self):

        max_width = 0
        max_height = 0

        for img in self.imgList:

            max_width = max(max_width, img.get_Img_width())
            max_height = max(max_height, img.get_Img_height())
        
        return max_width, max_height


    def get_Nb_Img(self):

        return len(self.imgList)

    def get_Img(self, i: int):

        return self.imgList[i].get_Img()

    def get_I(self, i: int):

        return self.imgList[i]


    def resize_Img_list(self, height=4092, width=2160 ):

        for img in self.imgList:
            img = img.resize_Img(width, height)
        #print("Resize complete")


    