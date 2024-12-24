import os
from lib.psd_utils import psd_utils as psdutil

root=os.getcwd()
parse_folder=""
default_folder = {"CharacterSpriteSheet":"{}/CharacterSpriteSheet/default/0/".format(root),"character-action-split-frame":"{}/character-action-split-frame/".format(root)}
def check_folder():
    global parse_folder
    lists = os.listdir(root)
    print("Current folder list")
    print(lists)
    for item in lists:
        if ".zip" in item:
            continue
        if "CharacterSpriteSheet" in item:
            if parse_folder=="":
                parse_folder = "CharacterSpriteSheet"
            
        if "character-action-split-frame" in item:
            if parse_folder=="":
                parse_folder = "character-action-split-frame"

    if parse_folder=="":
        print("No data from MapleSalon2 or Maple simulator")
        return 1
    return 0

def check_ismaplesalon_with_json():
    global parse_folder
    if parse_folder == "character-action-split-frame":
        lists2 = os.listdir("{}".format(default_folder[parse_folder]))
        for l in lists2:
            if "walk1.json" in l:
                return 1
    return 0

        

def create_psd_by_png():
    if check_folder():
        os._exit()
    if check_ismaplesalon_with_json():
        print("Maplesalon json exists")
        load_maplesalon()
    else:
        psd = psdutil()
        psd.load_psd("{}/src/Avatar_Cape.psd".format(root))
        psd.load_png(default_folder[parse_folder])
        # psd.layers['edithere:cape_capeBelowBody_83'].visible = False 
        # psd.show_psd()
        psd.save_psd("{}/Cape.psd".format(root))

def preview(name):
    if check_folder():
        os._exit()
    psd = psdutil()
    if ".psd" not in name:
        name += ".psd"
    
    lists = os.listdir(root)
    if name not in lists:
        print("File {} not found in {}".format(name,root))
        return 1
    psd.load_psd("{}/{}".format(root,name))
    psd.preview(root)

def maples_im_align(url):
    import subprocess
    import zipfile
    
    #download file
    download("{}&renderMode=1".format(url),"{}/tmp.zip".format(root))
    download("{}&renderMode=2".format(url),"{}/CharacterSpriteSheet.zip".format(root))
    # unzip file
    unzip_file(root,"tmp.zip")
    unzip_file(root,"CharacterSpriteSheet.zip")
    psd = psdutil()
    psd.load_psd("{}/src/Avatar_Cape.psd".format(root))
    # psd.load_png("{}/tmp/default/0/".format(root))
    psd.load_png2("{}/CharacterSpriteSheet/default/0/".format(root),"{}/tmp/default/0/".format(root))
    psd.save_psd("{}/Cape.psd".format(root))

def download(url,file):
    import requests
    # 儲存的檔案名稱
    file_name = file
    # 模擬瀏覽器的 User-Agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # 發送 GET 請求，附帶 headers
    response = requests.get(url, headers=headers)

    # 檢查 HTTP 回應狀態碼
    if response.status_code == 200:
        # 儲存檔案
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"檔案已經成功下載並儲存為 {file_name}")
    else:
        print(f"下載失敗，HTTP 錯誤碼：{response.status_code}")

def unzip_file(path,name):
    import zipfile
    zip_filename = '{}/{}'.format(path,name)
    if ".zip" not in zip_filename:
        zip_filename += ".zip"
    extract_to_directory = '{}/{}/'.format(path,name.replace('.zip',''))
    # 解壓縮文件
    print("Unzip file {}".format(name))
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to_directory)

def make_chair(filename,pic_name):
    psd = psdutil()
    psd.load_psd("{}/{}".format(root,filename))# left

    psd_right = psdutil()
    psd_right.load_psd("{}/src/Avatar_Longcoat.psd".format(root))
    psd.make_bigchair("{}/{}".format(root,pic_name),psd_right.psd)
    psd.save_psd("{}/Cape.psd".format(root))
    psd_right.save_psd("{}/Longcoat.psd".format(root))

def pic_classify():
    if check_folder():
        os._exit()
    psd = psdutil()
    psd.load_psd("{}/src/Avatar_Cape.psd".format(root))
    for key in psd.cape.keys():
        psd.classify(default_folder[parse_folder],key)

def load_maplesalon():
    if check_folder():
        os._exit()
    psd = psdutil()
    psd.load_psd("{}/src/Avatar_Cape.psd".format(root))
    pics = psd.load_mapleson_png_with_json(default_folder[parse_folder])
    psd.load_png(default_folder[parse_folder],pics=pics)
    psd.save_psd("{}/Cape.psd".format(root))


def menu():
    menu = [
            "目前功能",
            "1. Auto Align",
            "2. Convert PSD to GIF",
            "3. Make Big Chair",
            # "4. Maplesalon 特效分類(不是很準 +-玩玩)",
            # "5. load config with json",
            #"3. 透過https://maples.im/# 的下載網址來auto align",
            "0. 退出"
        ]
    
    while True:
        print("\n".join(menu))
        
        user_choice = input("請輸入選擇的功能編號: ")
        
        if user_choice == "1":
            print("你選擇了 Auto Align 功能")
            # 在這裡加入 Auto Align 功能的代碼
            create_psd_by_png()
        elif user_choice == "2":
            print("你選擇了 Convert PSD to GIF 功能(建議先把製作好的圖層們合併，加速載入時間，同時請注意PSD內的檔案圖層應該對齊完畢)")
            # 在這裡加入 預覽 from psd 功能的代碼
            filename = input("檔案名稱: ")
            preview(filename)
        elif user_choice =="3":
            filename = input("請輸入作為基底的psd的檔案名稱(另外一個檔案會使用src底下的另外一個檔案會使用src底下的Avatar_Longcoat.psd): ")
            pic_name = input("請輸入椅子圖片名稱(椅子寬度請超過250pixel): ")
            lists = os.listdir(root)
            if ".psd" not in filename:
                filename+=".psd"
            if ".jpg" not in pic_name and ".png" not in pic_name:
                if "{}.jpg".format(pic_name) in lists:
                    pic_name+=".jpg"
                elif "{}.png".format(pic_name) in lists:
                    pic_name+=".png"
                else:
                    print("no {} found in {} folder".format(pic_name,root))
                    return 1
            if filename not in lists :
                print("file {} not found in {}".format(filename,root))
                return 1
            if pic_name not in lists :
                print("file {} not found in {}".format(pic_name,root))
                return 1
            make_chair(filename,pic_name)
        # elif user_choice == "4":
        #     pic_classify()
        # elif user_choice == "5":
        #     load_maplesalon()
        elif user_choice == "0":
            print("退出程式")
            break
        else:
            print("無效的選擇，請重新輸入。")
    
def show_info():
    infos=['Artile Little Tool',
           'Version: 1.0.4',
           'Author: George.Chang']
    print("\n".join(infos))
    print("\n\n")
    

if __name__ == "__main__":
    show_info()
    menu()
