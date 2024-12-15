import os
import psd_tools
from PIL import Image
from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer as pxl

class psd_utils:

    def __init__(self) -> None:
        self.psd=None
        self.orgcanvas = None
        self.src_path=""
        self.type = ""
        self.layers = {}
        self.cape = {'walk1':{'x':0,'y':0,'block':4},
            'walk2':{'x':0,'y':1,'block':4},
            'stand1':{'x':0,'y':2,'block':3},
            'stand2':{'x':0,'y':3,'block':3},
            'alert':{'x':0,'y':4,'block':3},
            'swingO1':{'x':0,'y':5,'block':3},
            'swingO2':{'x':0,'y':6,'block':3},
            'swingO3':{'x':0,'y':7,'block':3},
            'swingOF':{'x':0,'y':8,'block':4},
            'swingT1':{'x':0,'y':9,'block':3},
            'swingT2':{'x':0,'y':10,'block':3},
            'swingT3':{'x':0,'y':11,'block':3},
            'swingTF':{'x':0,'y':12,'block':4},
            'ladder':{'x':0,'y':13,'block':2},
            
            'stabO1':{'x':5,'y': 0,'block':2},
            'stabT1':{'x':5,'y':1,'block':3},
            'stabT2':{'x':5,'y':2,'block':3},
            'proneStab':{'x':5,'y':3,'block':2},
            'stabTF':{'x':7,'y':4,'block':1},
            'fly':{'x':5,'y':5,'block':2},
            'shoot1':{'x':5,'y':6,'block':3},
            'shoot2':{'x':5,'y':7,'block':5},
            'swingP1':{'x':5,'y':9,'block':3},
            'swingP2':{'x':5,'y':10,'block':3},
            'swingPF':{'x':5,'y':11,'block':4},
            'stabOF':{'x':5,'y':12,'block':3},
            'rope':{'x':5,'y':13,'block':2},
            
            'stabO2':{'x':8,'y': 0,'block':2},
            'jump':{'x':8,'y':5,'block':1},
            'shootF':{'x':9,'y':6,'block':2},
            'sit':{'x':10,'y':11,'block':1}}

    def load_psd(self,path=""):
        if path=="":
            return 1
        self.psd = PSDImage.new(mode="RGBA",size=(2750,3500))
        # self.psd = PSDImage.open(path,mode="RGBA")
        print("load template")
        tmp=PSDImage.open(path)
        self.orgcanvas = tmp.composite()
        for layer in tmp:
            self.psd.append(layer)
        print("load template finished")
        if "CAPE" in path.upper():
            self.type="CAPE"
        self.load_layers()

    def save_psd(self,path):
        if path =="":
            return 1
        if ".psd" not in path:
            path+=".psd"
        self.psd.save(path)

    def show_psd(self):
        #self.set_layers()
        self.psd.composite(layer_filter=lambda layer: layer.is_visible() and layer.kind != 'type').show()
    
    def load_layers(self):
        self.layers={}
        for layer in self.psd:
            print("set layer{}".format(layer))
            self.layers[layer.name]=layer

    def set_layers(self):
        for layer in self.psd:
            if layer.name in self.layers.keys():
                layer = self.layers[layer.name]
                print(layer.name)
                print(layer.visible)
                print("---")
            else:
                pass
    
    def load_png(self,path,name=""):
        errcnt=0
        png_path=""
        if "character-action-split-frame" in path:
            png_path = "{}/default-{}-{}.png"
        elif "CharacterSpriteSheet" in path:
            png_path = "{}/{}_{}.png"
        for key in self.cape.keys():
            cape_x = self.cape[key]['x']
            cape_y = self.cape[key]['y']
            blocks = self.cape[key]['block']
            # load correspond pic and put to psd
            for i in range(blocks):
                try:
                    print("Load png : {}/{}_{}.png".format(path,key,i))
                    png_image = Image.open(png_path.format(path,key,i)).convert("RGBA")
                    img = self.orgcanvas.crop(((cape_x+i)*250,(cape_y*250),(cape_x+i+1)*250,(cape_y+1)*250))
                    x,y = self.get_offset(img,png_image)
                    png_layer = pxl.frompil(png_image,psd_file=self.psd,layer_name="{}_{}".format(key,i),left=(cape_x+i)*250+x,top=(cape_y)*250+y)
                    self.layers[key]=png_layer
                    self.psd.append(png_layer)
                except Exception as e:
                    errcnt+=1
                    print("load failed")
        print("total failed count:{}".format(errcnt))

    def load_png_bak(self,path,bx=0,by=0,name=""):
        png_image = Image.open(path).convert("RGBA")
        img = self.orgcanvas.crop((bx*250,by*250,250,250))
        x,y = self.get_offset(img,png_image)
        png_layer = pxl.frompil(png_image,psd_file=self.psd,layer_name=name,top=by*250+y,left=bx*250+x)
        self.layers[name]=png_layer
        self.psd.append(png_layer)        

    def get_offset(self,canvas, target):
        import cv2
        import numpy as np
        large_image_pil = canvas  # 大圖 (Pillow 格式)
        small_image_pil = target  # 小圖 (Pillow 格式)

        # 將 PIL 圖像轉為 NumPy 陣列
        large_image_np = np.array(large_image_pil.convert('L'))  # 轉為灰階並轉為陣列
        small_image_np = np.array(small_image_pil.convert('L'))  # 轉為灰階並轉為陣列

        # 進行模板匹配
        result = cv2.matchTemplate(large_image_np, small_image_np, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 找到最佳匹配的位置
        top_left = max_loc
        h, w = small_image_np.shape
        print("{}".format(top_left))
        return top_left
        # # 在擷取範圍內繪製框線
        # matched_image = cv2.cvtColor(large_image_np, cv2.COLOR_GRAY2BGR)
        # cv2.rectangle(matched_image, top_left, (top_left[0] + w, top_left[1] + h), (0, 255, 0), 3)

        # # 繪製結果
        # fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # axes[0].imshow(np.array(large_image_pil), cmap='gray')
        # axes[0].set_title("Original Larger Image")
        # axes[0].axis('off')

        # axes[1].imshow(large_image_np, cmap='gray')
        # axes[1].set_title("Cropped Image")
        # axes[1].axis('off')  

        # axes[2].imshow(matched_image)
        # axes[2].set_title("Matched Result in Cropped Image")
        # axes[2].axis('off')

        # plt.tight_layout()
        # plt.show()




