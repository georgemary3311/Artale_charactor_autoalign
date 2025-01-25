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

class psd_utils:

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
            'stabTF':{'x':7,'y':4,'block':1, 'delay':[100,200,200,200], 'offsetx':[149], 'offsety':[135]},
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

    def load_psd(self,path="",visible = False):
        if path=="":
            return 1
        self.psd = PSDImage.new(mode="RGBA",size=(2750,3500))
        # self.psd = PSDImage.open(path,mode="RGBA")
        print("load template")
        tmp=PSDImage.open(path)
        if visible:
            for t in tmp:
                if "guide_grid" in t.name or "guide_background" in t.name:
                    t.visible = False
        self.orgcanvas = tmp.composite(layer_filter=lambda layer: layer.is_visible() and layer.kind != 'type')
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
    
    def load_png(self,path,name="",pics=[]):
        errcnt=0
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
                    print("prefix:{}".format(prefix))
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
                        print(filename)
                        x = self.cape[key]['offsetx'][i] - self.js[key][i]['x']
                        y = self.cape[key]['offsety'][i] - self.js[key][i]['y']
                        print("json x:{}, y:{}".format( self.js[key][i]['x'], self.js[key][i]['y']))
                        png_image = Image.open("{}/{}".format(path,filename)).convert("RGBA")
                    else:
                        print("Load png : {}".format(p))
                        png_image = Image.open(p).convert("RGBA")
                        #因為有些output的圖片更大 比預計的格子還大 所以動態調整
                        if png_image.width >=250:
                            offset0 = png_image.width - 250
                        if png_image.height >=250:
                            offset1 = png_image.height - 250
                        print("offset {},{}".format(offset0,offset1))
                        img = self.orgcanvas.crop(((cape_x+i)*250,(cape_y*250),(cape_x+i+1)*250+offset0,(cape_y+1)*250+offset1))
                        x,y = self.get_offset(img,png_image)

                    png_layer = pxl.frompil(png_image,psd_file=self.psd,layer_name="{}_{}".format(key,i),left=(cape_x+i)*250+x,top=(cape_y)*250+y)
                    self.layers[key]=png_layer
                    # self.psd.append(png_layer)
                    group.append(png_layer)
                    #Move to group
                except Exception as e:
                    errcnt+=1
                    print("load failed")
                    print(e)
        print("total failed count:{}".format(errcnt))

    def load_png2(self,path,tmp_path,name="",simu=False):
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
                    print("Load png : {}/{}_{}.png".format(path,key,i))
                    png_image = Image.open(png_path.format(path,key,i)).convert("RGBA")
                    print("Load png : {}/{}_{}.png".format(tmp_path,key,i))
                    tmp_img = Image.open(png_path.format(tmp_path,key,i)).convert("RGBA")
                    #因為有些output的圖片更大 比預計的格子還大 所以動態調整
                    offset0 = 0
                    offset1 = 0
                    if png_image.width >=250:
                        offset0 = png_image.width - 250
                    if png_image.height >=250:
                        offset1 = png_image.height - 250
                    print("offset {},{}".format(offset0,offset1))
                    
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

    def load_png_bak(self,path,bx=0,by=0,name=""):
        png_image = Image.open(path).convert("RGBA")
        img = self.orgcanvas.crop((bx*250,by*250,250,250))
        x,y = self.get_offset(img,png_image)
        png_layer = pxl.frompil(png_image,psd_file=self.psd,layer_name=name,top=by*250+y,left=bx*250+x)
        self.layers[name]=png_layer
        self.psd.append(png_layer)        

    def update_canvas(self):
        self.orgcanvas = self.psd.composite()

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

    def preview(self,root):
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
                    print("load failed")
                    print(e)
            folder_path = "{}/preview/".format(root)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            images[0].save('{}/{}.gif'.format(folder_path,key), save_all=True, append_images=images[1:], duration=delay, loop=0)    

    def set_redpoint_left(self):
        #原本的位置 x = 142 , y = 136
        x = 142
        y = 136
        offset_x = 20
        offset_y = 23
        for layer in self.psd:
            if layer.is_group():
                print(layer)
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
                        #取代原本的圖層
                        result_img = Image.fromarray(pixels)
                        png_layer = pxl.frompil(result_img,psd_file=self.psd,layer_name=child.name,left=0,top=0)
                        self.psd.append(png_layer)
                        png_layer.move_to_group(layer)
                        layer.remove(child)
                        
    def set_redpoint_right(self,x,psd):
        #原本的位置 x = 142 , y = 136
        offset_x = 21
        offset_y = 23
        for layer in psd:
            if layer.is_group():
                print(layer)
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
                        print("紅點位置:{},{}".format(x-offset_x-sit_x,249-offset_y))
                        #取代原本的圖層
                        result_img = Image.fromarray(pixels)
                        png_layer = pxl.frompil(result_img,psd_file=psd,layer_name=child.name,left=0,top=0)
                        psd.append(png_layer)
                        png_layer.move_to_group(layer)
                        layer.remove(child)

    def make_bigchair(self,pic_path,psd_right):
        img = Image.open(pic_path).convert("RGBA")
        limited_x=479
        limited_y=250
        #check char size:
        y=img.height
        x=img.width
        if img.width>limited_x:
            x=479
        if img.height > limited_y:
            y=250
        img = img.crop((0,0,x,y)).convert("RGBA")
        # split image
        if x > 250:
            img_left=img.crop((0,0,250,y)).convert('RGBA')
            img_right=img.crop((251,0,x,y)).convert('RGBA')
        else:
            img_left=img.crop((0,0,250,y)).convert('RGBA')
        #put pic to cape 
        png_layer_left = pxl.frompil(img_left,psd_file=self.psd,layer_name="chair_left",left=self.cape['sit']['x']*250,top=self.cape['sit']['y']*250+250-y)
        self.psd.append(png_layer_left)
        self.set_redpoint_left()

        if x > 250:
            print("Relpace second psd file")
            #put cap to coat
            png_layer_right = pxl.frompil(img_right,psd_file=psd_right,layer_name="chair_right",left=self.cape['sit']['x']*250+(500-x),top=self.cape['sit']['y']*250+250-y)
            psd_right.append(png_layer_right)
            self.set_redpoint_right(self.cape['sit']['x']*250+(500-x),psd_right)

    def classify(self,path,name):
        lists = os.listdir(path)
        tmp = []
        for l in lists:
            if name in l and "png" in l and "json" not in l:
                tmp.append(l)
        if len(tmp) == self.cape[name]['block']:
            print("No multiple pic exists, no need to classify")
            return 0
        print(tmp)
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
                print(f"資料夾 {folder_path} 已存在，正在刪除...")
                shutil.rmtree(folder_path)
            os.makedirs(folder_path)
            print("load gesture templete")
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

    def calculate_similarity(self, image1, image2):
        """計算兩張圖片的相似度（SSIM）"""
        score, _ = ssim(np.squeeze(np.array(image1)), np.squeeze(np.array(image2)),win_size=3, full=True)
        return score
    
    def load_json(self,path):
        print("Load Json file {}".format(path))
        with open(path, 'r') as file:
            data = json.load(file)
        return data

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
                print("Init {} failed, no such key in PSD, errmesg:{}".format(l,e))
        # print(images.keys())
        #選擇是要使用哪些圖片
        print("\n\n")
        for key in images.keys():
            print("Choose {}".format(key))
            js = self.load_json("{}/{}".format(path,images[key]['json']))
            self.js[key] = []
            block = self.cape[key]['block']
            delays = self.cape[key]['delay']
            pic_lists = images[key]['gesture']
            #重整排續
            pic_lists = sorted(pic_lists, key=lambda x: int(x.split('-')[-1].split('.')[0]))
            print(pic_lists)
            delay = 0
            pic_index = 0
            pics = []
            for b in range(block):
                #choose block's pic
                print("--------- Choise {}_{}".format(key,b))
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
            print(pics)
            print("\n")
            pic_arr[key]=pics
        return pic_arr
              


    
