import os
import psd_tools
import json
import numpy as np
import shutil
import cv2
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from psd_tools import PSDImage
from psd_tools.api.layers import PixelLayer as pxl
from psd_tools.api.layers import Group as gp
from lib.globalstuff import globalstuff
from lib.globalstuff import Color

class psd_utils(globalstuff):
    '''
    Function Name:  __init__
    Description:    Initialize the psd_utils class with default attributes, including PSD file, canvas, gesture configurations, and other metadata.
    Author:         George Chang
    '''
    def __init__(self) -> None:
        self.psd=None
        self.orgcanvas = None
        self.js={}
        self.src_path=""
        self.type = ""
        self.layers = {}
        self.cape = {'walk1':{'x':0,'y':0,'block':4, 'delay':[180,180,180,180], 'offsetx':[134,134,134,134], 'offsety':[150,150,150,150]},
            'walk2':{'x':0,'y':1,'block':4, 'delay':[180,180,180,180], 'offsetx':[134,134,134,134], 'offsety':[150,150,150,150]},
            'stand1':{'x':0,'y':2,'block':3, 'delay':[500,500,500], 'offsetx':[134,134,134], 'offsety':[150,150,150]},
            'stand2':{'x':0,'y':3,'block':3, 'delay':[500,500,500], 'offsetx':[134,134,134], 'offsety':[150,150,150]},
            'alert':{'x':0,'y':4,'block':3, 'delay':[500,500,500], 'offsetx':[142,142,142], 'offsety':[150,150,150]},
            'swingO1':{'x':0,'y':5,'block':3, 'delay':[300,150,350], 'offsetx':[133,141,150], 'offsety':[150,150,150]},
            'swingO2':{'x':0,'y':6,'block':3, 'delay':[300,150,350], 'offsetx':[144,143,144], 'offsety':[150,150,150]},
            'swingO3':{'x':0,'y':7,'block':3, 'delay':[300,150,350], 'offsetx':[139,158,158], 'offsety':[150,150,150]},
            'swingOF':{'x':0,'y':8,'block':4, 'delay':[200,100,100,300], 'offsetx':[142,147,165,169], 'offsety':[150,156,154,150]},
            'swingT1':{'x':0,'y':9,'block':3, 'delay':[300,150,350], 'offsetx':[134,147,146], 'offsety':[150,150,150]},
            'swingT2':{'x':0,'y':10,'block':3, 'delay':[300,150,350], 'offsetx':[145,145,145], 'offsety':[150,150,150]},
            'swingT3':{'x':0,'y':11,'block':3, 'delay':[300,150,350], 'offsetx':[135,140,137], 'offsety':[150,150,150]},
            'swingTF':{'x':0,'y':12,'block':4, 'delay':[200,150,150,200], 'offsetx':[147,147,148,149], 'offsety':[150,150,150,150]},
            'ladder':{'x':0,'y':13,'block':2, 'delay':[250,250], 'offsetx':[130,127], 'offsety':[150,148]},
            
            'stabO1':{'x':5,'y': 0,'block':2, 'delay':[350,450], 'offsetx':[141,153], 'offsety':[150,150]},
            'stabT1':{'x':5,'y':1,'block':3, 'delay':[300,100,350], 'offsetx':[148,150,165], 'offsety':[150,150,150]},
            'stabT2':{'x':5,'y':2,'block':3, 'delay':[300,100,350], 'offsetx':[139,140,158], 'offsety':[150,150,150]},
            'proneStab':{'x':5,'y':3,'block':2, 'delay':[300,400], 'offsetx':[153,153], 'offsety':[150,150]},
            'stabTF':{'x':5,'y':4,'block':3, 'delay':[100,200,200,200], 'offsetx':[ 149,149,159], 'offsety':[150,150,166]},
            'fly':{'x':5,'y':5,'block':2, 'delay':[300,300], 'offsetx':[138,142], 'offsety':[150,150 ]},
            'shoot1':{'x':5,'y':6,'block':3, 'delay':[300,150,350], 'offsetx':[144,144,144], 'offsety':[150,150,150]},
            'shoot2':{'x':5,'y':7,'block':5, 'delay':[160,160,250,100,150], 'offsetx':[143,143,143,143,143], 'offsety':[150,150,150,150,150]},
            'swingP1':{'x':5,'y':9,'block':3, 'delay':[300,150,350], 'offsetx':[134,147,146,], 'offsety':[150,150,150]},
            'swingP2':{'x':5,'y':10,'block':3, 'delay':[300,150,350], 'offsetx':[143,143,141], 'offsety':[150,150,150]},
            'swingPF':{'x':5,'y':11,'block':4, 'delay':[100,200,200,200], 'offsetx':[135,137,151,178], 'offsety':[150,150,166,150]},
            'stabOF':{'x':5,'y':12,'block':3, 'delay':[250,150,300], 'offsetx':[139,151,162], 'offsety':[150,152,150]},
            'rope':{'x':5,'y':13,'block':2, 'delay':[250,250], 'offsetx':[128,128], 'offsety':[150,150]},
            
            'stabO2':{'x':8,'y': 0,'block':2, 'delay':[350,450], 'offsetx':[142,156], 'offsety':[150,150]},
            'jump':{'x':8,'y':5,'block':1, 'delay':[500], 'offsetx':[137], 'offsety':[150]},
            'shootF':{'x':9,'y':6,'block':2, 'delay':[300,150,250], 'offsetx':[144,141], 'offsety':[150,150]},
            'sit':{'x':10,'y':11,'block':1, 'delay':[500], 'offsetx':[144], 'offsety':[153]}}

    '''
    Function Name:  load_psd
    Description:    Load a PSD file, initialize its layers, and set visibility for specific layers if required.
    Parameters:     path (str): The file path of the PSD file to load.
                    visible (bool): Whether to hide specific layers (default: False).
    Author:         George Chang
    '''
    def load_psd(self, path="", visible=False):
        if path=="":
            return 1
        self.psd = PSDImage.new(mode="RGBA",size=(2750,3500))
        # self.psd = PSDImage.open(path,mode="RGBA")
        self.send_log("Load psd file {}".format(path),"info",color=Color.YELLOW)
        tmp=PSDImage.open(path)
        if visible:
            for t in tmp:
                if "guide_grid" in t.name or "guide_background" in t.name:
                    t.visible = False
        self.orgcanvas = tmp.composite(layer_filter=lambda layer: layer.is_visible() and layer.kind != 'type')
        for layer in tmp:
            self.psd.append(layer)
        self.send_log("Load psd file finished", "info",color=Color.YELLOW)
        if "CAPE" in path.upper():
            self.type="CAPE"
        self.load_layers()

    '''
    Function Name:  save_psd
    Description:    Save the current PSD file to the specified path.
    Parameters:     path (str): The file path to save the PSD file.
    Author:         George Chang
    '''
    def save_psd(self, path):
        if path =="":
            return 1
        if ".psd" not in path:
            path+=".psd"
        self.send_log("Save psd file {}".format(path),"info",color=Color.YELLOW)
        self.psd.save(path)

    '''
    Function Name:  show_psd
    Description:    Display the composite image of the current PSD file.
    Author:         George Chang
    '''
    def show_psd(self):
        self.send_log("Show psd file {}".format(self.psd.name),"info",color=Color.YELLOW)
        self.psd.composite(layer_filter=lambda layer: layer.is_visible() and layer.kind != 'type').show()
    
    '''
    Function Name:  load_layers
    Description:    Load all layers from the current PSD file and store them in a dictionary for easy access.
    Author:         George Chang
    '''
    def load_layers(self):
        self.layers={}
        for layer in self.psd:
            self.send_log("Loading Layer name: {}".format(layer.name),"info",color=Color.GREEN)
            self.layers[layer.name]=layer

    '''
    Function Name:  set_layers
    Description:    Update the layers of the PSD file based on the stored layer dictionary.
    Author:         George Chang
    '''
    def set_layers(self):
        for layer in self.psd:
            if layer.name in self.layers.keys():
                layer = self.layers[layer.name]
                self.send_log("Set Layer name: {}".format(layer.name),"info",color=Color.YELLOW)
            else:
                pass
    
    '''
    Function Name:  load_png
    Description:    Load PNG images from a directory and add them as layers to the PSD file.
    Parameters:     path (str): The directory path containing PNG files.
                    name (str): The name of the group to which the PNG layers will be added.
                    pics (list): A list of PNG file names to load (optional).
    Author:         George Chang
    '''
    def load_png(self, path, name="", pics=[]):
        errcnt=0
        fail_items=[]
        png_path=""
        lists = os.listdir(path)
        prefix=""
        withprefix_maplesalon=False
        group = gp.new(name="Group_Artale")
        self.psd.append(group)
        if "character-action-split-frame" in path:
            png_path = "{}/{}-{}.png"
            for l in lists:
                if "-walk1-0.png" in l:
                    prefix=lists[0].split('-')[0]
                    self.send_log("Prefix: {}".format(prefix),"info",color=Color.YELLOW)
                    png_path = "{}/{}-{}-{}.png"
                    withprefix_maplesalon = True

        elif "CharacterSpriteSheet" in path or "tmp" in path:
            png_path = "{}/{}_{}.png"

        
        for key in self.cape.keys():
            cape_x = self.cape[key]['x']
            cape_y = self.cape[key]['y']
            blocks = self.cape[key]['block']
            # load correspond pic and put to psd
            for i in range(blocks):
                if key == "stabTF" and i <2 :
                    self.send_log("Stab TF don't conatin action {}".format(i),"info",color=Color.YELLOW)
                    continue
                try:
                    if withprefix_maplesalon:
                        p = png_path.format(path,prefix,key,i)
                    else:
                        p = png_path.format(path,key,i)
                    
                    offset0 = 0
                    offset1 = 0
                
                    if len(pics)!=0:
                        #透過json來尋找位置
                        filename = pics[key][i]
                        x = self.cape[key]['offsetx'][i] - self.js[key][i]['x']
                        y = self.cape[key]['offsety'][i] - self.js[key][i]['y']
                        self.send_log("Loading Filename {}, json x:{}, y:{}".format(filename, self.js[key][i]['x'], self.js[key][i]['y']),"info",color=Color.GREEN)
                        png_image = Image.open("{}/{}".format(path,filename)).convert("RGBA")
                    else:
                        png_image = Image.open(p).convert("RGBA")
                        #因為有些output的圖片更大 比預計的格子還大 所以動態調整
                        if png_image.width >=250:
                            offset0 = png_image.width - 250
                        if png_image.height >=250:
                            offset1 = png_image.height - 250
                        self.send_log("Load PNG {}, offset {},{}".format(p,offset0,offset1),"info",color=Color.YELLOW)
                        img = self.orgcanvas.crop(((cape_x+i)*250,(cape_y*250),(cape_x+i+1)*250+offset0,(cape_y+1)*250+offset1))
                        x,y = self.get_offset(img,png_image)

                    png_layer = pxl.frompil(png_image,psd_file=self.psd,layer_name="{}_{}".format(key,i),left=(cape_x+i)*250+x,top=(cape_y)*250+y)
                    self.layers[key]=png_layer

                    group.append(png_layer)
                    #Move to group
                except Exception as e:
                    errcnt+=1
                    fail_items.append(p)
                    self.send_log("Load failed {}, ERR msg:{}".format(p, e),"error",color=Color.RED)
        self.send_log("Load png file finished, failed count:{}".format(errcnt), "info",color=Color.YELLOW)
        self.send_log("Failed items: {}".format(fail_items), "info",color=Color.YELLOW)

    '''
    Function Name:  load_png2
    Description:    Load PNG images from two directories, process them, and add them as layers to the PSD file.
    Parameters:     path (str): The directory path containing the first set of PNG files.
                    tmp_path (str): The directory path containing the second set of PNG files.
                    name (str): The name of the group to which the PNG layers will be added.
                    simu (bool): Whether to simulate the process (default: False).
    Author:         George Chang
    '''
    def load_png2(self, path, tmp_path, name="", simu=False):
        errcnt=0
        png_path=""
        png_path = "{}/{}_{}.png"
        for key in self.cape.keys():
            cape_x = self.cape[key]['x']
            cape_y = self.cape[key]['y']
            blocks = self.cape[key]['block']
            # load correspond pic and put to psd
            for i in range(blocks):
                try:
                    self.send_log("Load png : {}/{}_{}.png".format(path,key,i),"info",color=Color.YELLOW)
                    png_image = Image.open(png_path.format(path,key,i)).convert("RGBA")
                    self.send_log("Load png : {}/{}_{}.png".format(tmp_path,key,i),"info",color=Color.YELLOW)
                    tmp_img = Image.open(png_path.format(tmp_path,key,i)).convert("RGBA")
                    #因為有些output的圖片更大 比預計的格子還大 所以動態調整
                    offset0 = 0
                    offset1 = 0
                    if png_image.width >=250:
                        offset0 = png_image.width - 250
                    if png_image.height >=250:
                        offset1 = png_image.height - 250
                    self.send_log("Load PNG {}, offset {},{}".format(png_path.format(path,key,i),offset0,offset1),"info",color=Color.YELLOW)
                    
                    img = self.orgcanvas.crop(((cape_x+i)*250,(cape_y*250),(cape_x+i+1)*250+offset0,(cape_y+1)*250+offset1)).convert("RGBA")
                    img.paste(tmp_img,(77,61))
                    img.save('{}/0_{}_{}.png'.format(tmp_path,key,i))
                    x,y = self.get_offset(img,png_image)
                    png_layer = pxl.frompil(png_image,psd_file=self.psd,layer_name="{}_{}".format(key,i),left=(cape_x+i)*250+x,top=(cape_y)*250+y)
                    self.layers[key]=png_layer
                    self.psd.append(png_layer)
                except Exception as e:
                    errcnt+=1
                    print("load failed")
                    print(e)
        print("total failed count:{}".format(errcnt))

    '''
    Function Name:  update_canvas
    Description:    Update the composite canvas of the current PSD file.
    Author:         George Chang
    '''
    def update_canvas(self):
        self.orgcanvas = self.psd.composite()

    '''
    Function Name:  get_offset
    Description:    Calculate the offset between a canvas and a target image using template matching.
    Parameters:     canvas (Image): The larger image (canvas).
                    target (Image): The smaller image (target).
    Returns:        tuple: The (x, y) offset of the target image within the canvas.
    Author:         George Chang
    '''
    def get_offset(self, canvas, target):
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
        self.send_log("Top left: {}, w: {}, h: {}".format(top_left, w, h), "info", color=Color.YELLOW)
        return top_left

    '''
    Function Name:  preview
    Description:    Generate preview GIFs for each gesture based on the PSD file and save them to a directory.
    Parameters:     root (str): The root directory where the preview GIFs will be saved.
    Author:         George Chang
    '''
    def preview(self, root):
        tmp = self.psd.composite(layer_filter=lambda layer: layer.is_visible() and layer.kind != 'type')
        revert = ['walk1','walk2','stand1','stand2','alert']
        for key in self.cape.keys():
            cape_x = self.cape[key]['x']
            cape_y = self.cape[key]['y']
            blocks = self.cape[key]['block']
            delay = self.cape[key]['delay']
            # load correspond pic and put to psd
            images = []
            sequence=[]
            for i in range(blocks):
                sequence.append(i)
            if key in revert:
                for i in range(blocks):
                    if i == 0 or i == blocks-1:
                        continue
                    sequence.append(i)
                    delay.append(self.cape[key]['delay'][i])
            for i in sequence:
                try:
                    img = tmp.crop(((cape_x+i)*250,(cape_y*250),(cape_x+i+1)*250,(cape_y+1)*250))
                    images.append(img)
                except Exception as e:
                    errcnt+=1
                    self.send_log("Load failed {}, ERR msg:{}".format(p, e),"error",color=Color.RED)
            folder_path = "{}/preview/".format(root)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            images[0].save('{}/{}.gif'.format(folder_path,key), save_all=True, append_images=images[1:], duration=delay, loop=0)   
            self.send_log("Save gif file to {}/{}.gif".format(folder_path,key),"info",color=Color.YELLOW) 

    '''
    Function Name:  set_redpoint_left
    Description:    Set a red point on the left side of the PSD file for alignment purposes.
    Author:         George Chang
    '''
    def set_redpoint_left(self,position="normal"):
        #原本的位置 x = 142 , y = 136
        x = 142
        y = 136
        offset_x = 20
        offset_y = 23
        if position == "up":   
            offset_y = 0
        elif position == "down":
            offset_y = 249
        for layer in self.psd:
            if layer.is_group():
                self.send_log("Layer infos: {}".format(layer),"info",color=Color.YELLOW)
                if "data" in layer.name:
                    for child in layer:
                        if "origin" not in child.name:
                            continue

                        sit_x = self.cape['sit']['x']*250
                        sit_y = self.cape['sit']['y']*250
                        # 直接把layer sit那邊的紅點點取代掉
                        #layer.composite().crop((sit_x,sit_y,sit_x+250,sit_y+250))
                        tmp = child.composite().convert("RGBA")
                        img = Image.new(mode="RGBA",size=(2750,3500))
                        img.paste(tmp, child.offset, tmp)
                        pixels=np.array(img)
                        #將椅子的地方設定成透明
                        pixels[sit_y:sit_y+249,sit_x:sit_x+249] = [0, 0, 0, 0]
                        #設定紅點
                        pixels[sit_y+249-offset_y,sit_x+249-offset_x] = [255, 0, 0, 255]
                        self.send_log("RED point position:{},{}".format(sit_x+249-offset_x,sit_y+249-offset_y),"info",color=Color.YELLOW)
                        #取代原本的圖層
                        result_img = Image.fromarray(pixels)
                        png_layer = pxl.frompil(result_img,psd_file=self.psd,layer_name=child.name,left=0,top=0)
                        self.psd.append(png_layer)
                        png_layer.move_to_group(layer)
                        layer.remove(child)

    '''
    Function Name:  set_redpoint_right
    Description:    Set a red point on the right side of the PSD file for alignment purposes.
    Parameters:     x (int): The x-coordinate for the red point.
                    psd (PSDImage): The PSD file to modify.
    Author:         George Chang
    '''
    def set_redpoint_right(self, x, psd,position="normal"):
        #原本的位置 x = 142 , y = 136
        offset_x = 21
        offset_y = 23
        if position == "up":   
            offset_y = 0
        elif position == "down":
            offset_y = 249
        for layer in psd:
            if layer.is_group():
                self.send_log("Layer infos: {}".format(layer),"info",color=Color.YELLOW)
                if "data" in layer.name:
                    layer.visible=True
                    for child in layer:
                        if "origin" not in child.name:
                            continue
                        sit_x = self.cape['sit']['x']*250
                        sit_y = self.cape['sit']['y']*250
                        # 直接把layer sit那邊的紅點點取代掉
                        #layer.composite().crop((sit_x,sit_y,sit_x+250,sit_y+250))
                        tmp = child.composite().convert("RGBA")
                        img = Image.new(mode="RGBA",size=(2750,3500))
                        img.paste(tmp, child.offset, tmp)
                        pixels=np.array(img)
                        #將椅子的地方設定成透明
                        pixels[sit_y:sit_y+249,sit_x:sit_x+249] = [0, 0, 0, 0]
                        #設定紅點
                        pixels[sit_y+249-offset_y,x-offset_x] = [255, 0, 0, 255]
                        self.send_log("RED point position:{},{}".format(x-offset_x-sit_x,249-offset_y),"info",color=Color.YELLOW)
                        #取代原本的圖層
                        result_img = Image.fromarray(pixels)
                        png_layer = pxl.frompil(result_img,psd_file=psd,layer_name=child.name,left=0,top=0)
                        psd.append(png_layer)
                        png_layer.move_to_group(layer)
                        layer.remove(child)

    '''
    Function Name:  make_bigchair
    Description:    Create a "big chair" by splitting an image into left and right parts and adding them to two PSD files.
    Parameters:     pic_path (str): The file path of the image to process.
                    psd_right (PSDImage): The PSD file for the right part of the chair.
    Author:         George Chang
    '''
    def make_bigchair(self, pic_path, psd_right, position="normal"):
        img = Image.open(pic_path).convert("RGBA")
        limited_x=479
        limited_y=250
        #check char size:
        y=img.height
        x=img.width
        if y > limited_y:
            y = limited_y
        img = img.crop((0,0,x,y)).convert("RGBA")
        # split image
        if x > 250:
            img_left=img.crop((0,0,250,y)).convert('RGBA')
            img_right=img.crop((250,0,x+1,y)).convert('RGBA')
        else:
            img_left=img.crop((0,0,250,y)).convert('RGBA')
        #put pic to cape 
        png_layer_left = pxl.frompil(img_left,psd_file=self.psd,layer_name="chair_left",left=self.cape['sit']['x']*250,top=self.cape['sit']['y']*250+250-y)
        self.psd.append(png_layer_left)
        self.set_redpoint_left(position)

        if x > 250:
            self.send_log("Relpace second psd file","info",color=Color.YELLOW)
            #put cap to coat
            png_layer_right = pxl.frompil(img_right,psd_file=psd_right,layer_name="chair_right",left=self.cape['sit']['x']*250+(500-x),top=self.cape['sit']['y']*250+250-y)
            psd_right.append(png_layer_right)
            self.set_redpoint_right(self.cape['sit']['x']*250+(500-x),psd_right,position)

    def save_horizontal_pic(self, pic_path):
        self.send_log("Changing horizontal pic".format(pic_path),"info",color=Color.YELLOW)
        img = Image.open(pic_path).convert("RGBA")
        #check char size:
        y=img.height
        x=img.width
        if y <250:
            self.send_log("Image height is too small, please check the image","error",color=Color.RED)
            return 1

        img = img.crop((0,249,x,y)).convert("RGBA")
        img.save('chair_btn.png')
        self.send_log("Save chair_btn.png","info",color=Color.YELLOW)
        return 0
        # split image
        

    '''
    Function Name:  classify
    Description:    Classify images into different gesture categories based on similarity to predefined templates.
    Parameters:     path (str): The directory path containing images to classify.
                    name (str): The name of the gesture to classify.
    Author:         George Chang
    '''
    def classify(self, path, name):
        lists = os.listdir(path)
        tmp = []
        for l in lists:
            if name in l and "png" in l and "json" not in l:
                tmp.append(l)
        if len(tmp) == self.cape[name]['block']:
            self.send_log("All pic exists, no need to classify","info",color=Color.YELLOW)
            return 0
        # 取得各動作有哪些圖片作為templete 並且使用skimage 來分類，分類的資料到相應資料夾後取出隨機一張作為那個動作的代表動作
        #取出模板圖片
        cape_x = self.cape[name]['x']
        cape_y = self.cape[name]['y']
        blocks = self.cape[name]['block']
        templete = {}
        for i in range(blocks):
            # 建立分類資料夾
            folder_path = "{}/{}_{}".format(path,name,i)
            if os.path.exists(folder_path):
                self.send_log("Remove folder {}".format(folder_path),"info",color=Color.YELLOW)
                shutil.rmtree(folder_path)
            os.makedirs(folder_path)
            # 建立每個動作的templete
            img = self.orgcanvas.crop(((cape_x+i)*250,(cape_y*250),(cape_x+i+1)*250,(cape_y+1)*250))
            templete[i]=img
        templete[0].show()

        for element in tmp:
            try:
                print("Classify {}".format(element))
                base_image = Image.open("{}/{}".format(path,element)).convert("RGBA")
                highest_similarity = -1
                most_similar_image = None
                for key in templete.keys():
                    compare_image = templete[key]
                    img = Image.new(mode="RGBA",size=(250,250))
                    
                    img.paste(base_image, (125-int(base_image.width/2),125-int(base_image.height/2)))
                    # img.show()
                    similarity = self.calculate_similarity(img, compare_image)
                    if similarity > highest_similarity:
                        highest_similarity = similarity
                        most_similar_image = key
                print("Similar to {}_{}".format(name,most_similar_image))
                shutil.copy("{}/{}".format(path,element), "{}/{}_{}".format(path,name,most_similar_image))
            except Exception as e:
                print("process {} failed, {}".format(element,e))

    '''
    Function Name:  calculate_similarity
    Description:    Calculate the structural similarity (SSIM) between two images.
    Parameters:     image1 (Image): The first image.
                    image2 (Image): The second image.
    Returns:        float: The SSIM score between the two images.
    Author:         George Chang
    '''
    def calculate_similarity(self, image1, image2):
        score, _ = ssim(np.squeeze(np.array(image1)), np.squeeze(np.array(image2)),win_size=3, full=True)
        return score
    
    '''
    Function Name:  load_json
    Description:    Load a JSON file from the specified path and return its content as a Python dictionary.
    Parameters:     path (str): The file path of the JSON file to load.
    Returns:        dict: The loaded JSON data.
    Author:         George Chang
    '''
    def load_json(self, path):
        self.send_log("Load Json file {}".format(path),"info",color=Color.GREEN)
        with open(path, 'r') as file:
            data = json.load(file)
        return data

    '''
    Function Name:  load_mapleson_png_with_json
    Description:    Load PNG and JSON files from a directory, organize them by gesture, and process them based on predefined configurations.
    Parameters:     path (str): The directory path containing PNG and JSON files.
    Returns:        dict: A dictionary mapping gestures to their corresponding PNG files.
    Author:         George Chang
    '''
    def load_mapleson_png_with_json(self, path):
        lists = os.listdir(path)
        images = {}
        pic_arr = {}
        # 初始化所有資料
        for i in self.cape.keys():
            images[i] = {'json' : "" , 'gesture' : []}

        for l in lists:
            
            try:
                sign_count= l.count('-')
                if "json" in l:
                    images[l.split('.')[0].split('-')[-1]]['json'] = l
                if ".png" in l:
                    images[l.split('-')[sign_count-1]]['gesture'].append(l)
            except Exception as e:
                self.send_log("[SKIP]Not json or png file: {}".format(l),"warning",color=Color.MAGENTA)
        # print(images.keys())
        #選擇是要使用哪些圖片
        for key in images.keys():
            self.send_log("Choose {}".format(key),"info",color=Color.GREEN)
            try:
                js = self.load_json("{}/{}".format(path,images[key]['json']))
            except Exception as e:
                self.send_log("Unable to load {}, skip to next gesture".format(key),"warning",color=Color.MAGENTA)
                continue
            self.js[key] = []
            block = self.cape[key]['block']
            delays = self.cape[key]['delay']
            pic_lists = images[key]['gesture']
            #重整排續
            pic_lists = sorted(pic_lists, key=lambda x: int(x.split('-')[-1].split('.')[0]))
            delay = 0
            pic_index = 0
            pics = []
            for b in range(block):
                #choose block's pic
                self.send_log("-------- {}_{}".format(key,b),"info",color=Color.BLUE)
                for i in range(pic_index,len(pic_lists)):
                    if len(pics) == 0:
                        delay += js[i]['delay']
                        pics.append(pic_lists[i])
                        tmp = {'x':js[i]['x'],'y':js[i]['y']}
                        self.js[key].append(tmp)
                        pic_index+=1
                        break
                    else:
                        #透過delay 來尋找下一張圖
                        if delay >= delays[b-1]:
                            delay = js[i]['delay']
                            pics.append(pic_lists[i])
                            tmp = {'x':js[i]['x'],'y':js[i]['y']}
                            self.js[key].append(tmp)
                            pic_index+=1
                            break
                        else:
                            delay += js[i]['delay']
                        pic_index+=1
                        
            pics = sorted(pics, key=lambda x: int(x.split('-')[-1].split('.')[0]))
            pic_arr[key]=pics
        return pic_arr




