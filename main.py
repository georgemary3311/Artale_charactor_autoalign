import os
import json
from lib.psd_utils import psd_utils as psdutil
from lib.globalstuff import globalstuff, Color, File_type, Equipment
import threading
gs = globalstuff()

root = os.getcwd()
parse_folder = ""
default_folder = {"CharacterSpriteSheet": "{}/CharacterSpriteSheet/default/0/".format(root), "character-action-split-frame": "{}/character-action-split-frame/".format(root)}

lang = ""

def check_folder():
    global parse_folder
    lists = os.listdir(root)
    gs.send_log("Current folder list", level="info", color=Color.YELLOW)
    gs.send_log("{}".format(lists), level="info", color=Color.GREEN)
    for item in lists:
        if ".zip" in item:
            continue
        if "CharacterSpriteSheet" in item:
            if parse_folder == "":
                parse_folder = "CharacterSpriteSheet"
        if "character-action-split-frame" in item:
            if parse_folder == "":
                parse_folder = "character-action-split-frame"
    if parse_folder == "":
        gs.send_log("No data from MapleSalon2 or Maple simulator", level="error", color=Color.RED)
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
        #maplesalon2
        gs.send_log("Maplesalon json exists", level="info", color=Color.GREEN)
        load_maplesalon()
    else:
        #maplesimulator1
        psd = psdutil()
        equit = gs.choose_equipment()
        psd.load_psd("{}/src/Avatar_{}.psd".format(root,equit))
        psd.load_png(default_folder[parse_folder])
        psd.save_psd("{}/Avatar_{}_Done.psd".format(root,equit))

def preview(name):
    if check_folder():
        os._exit()
    psd = psdutil()
    if ".psd" not in name:
        name += ".psd"
    
    lists = os.listdir(root)
    if name not in lists:
        print(lang["error_file_not_found"].format(name, root))
        return 1
    psd.load_psd("{}/{}".format(root, name))
    psd.preview(root)

def maples_im_align(url,filename):
    import subprocess
    import zipfile
    
    #download file
    t1 = threading.Thread(target=gs.download, args=(f"{url}&renderMode=1", f"{root}/tmp.zip"))
    t2 = threading.Thread(target=gs.download, args=(f"{url}&renderMode=2", f"{root}/CharacterSpriteSheet.zip"))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # unzip file
    gs.unzip_file(root,"tmp.zip")
    gs.unzip_file(root,"CharacterSpriteSheet.zip")
    psd = psdutil()
    psd.load_psd("{}/src/{}.psd".format(root,filename))
    psd.load_png2("{}/CharacterSpriteSheet/default/0/".format(root),"{}/tmp/default/0/".format(root))
    psd.save_psd("{}/{}_Done.psd".format(root,filename))


def make_chair_2pic(pic_name,filename,filename2="{}/src/Avatar_Longcoat.psd"):
    psd = psdutil()
    psd.load_psd("{}/{}".format(root, filename))  # left
    psd_right = psdutil()
    # psd_right.load_psd("{}/src/Avatar_Longcoat.psd".format(root))
    psd_right.load_psd("{}/src/{}".format(root, filename2))  # right
    psd.make_bigchair("{}/{}".format(root, pic_name), psd_right.psd)
    psd.save_psd("{}/{}".format(root,filename.replace(".psd","_left.psd")))
    psd_right.save_psd("{}/{}".format(root,filename2.replace(".psd","_right.psd")))

def make_chair_4pic(pic_name,filename):
    filename2="Avatar_Coat.psd"
    filename3="Avatar_Gloves.psd"
    filename4="Avatar_Pants.psd"
    gs.send_log("Processing TOP right/left picture", level="info", color=Color.YELLOW)
    psd_lefttop = psdutil()
    #check if it's about to split pic to two images, sould be chair_btn.png
    if psd_lefttop.save_horizontal_pic("{}/{}".format(root, pic_name)):
        gs.send_log("Error: save_horizontal_pic failed", level="error", color=Color.RED)
        return 1
    psd_lefttop.load_psd("{}/{}".format(root, filename))  # LEFT TOP
    psd_righttop = psdutil()
    # psd_right.load_psd("{}/src/Avatar_Longcoat.psd".format(root))
    
    psd_righttop.load_psd("{}/src/{}".format(root, filename2))  # RIGHT TOP
    psd_lefttop.make_bigchair("{}/{}".format(root, pic_name), psd_righttop.psd, "up")
    psd_lefttop.save_psd("{}/{}".format(root,filename.replace(".psd","_LEFT_TOP.psd")))
    psd_righttop.save_psd("{}/{}".format(root,filename2.replace(".psd","_RIGHT_TOP.psd")))
    gs.send_log("Processing TOP right/left picture Finished", level="info", color=Color.YELLOW)


    gs.send_log("Processing BTN right/left picture", level="info", color=Color.YELLOW)
    psd_leftbottom = psdutil()
    psd_leftbottom.load_psd("{}/src/{}".format(root, filename3))  # LEFT BOTTOM
    psd_rightbottom = psdutil()
    # psd_right.load_psd("{}/src/Avatar_Longcoat.psd".format(root))
    psd_rightbottom.load_psd("{}/src/{}".format(root, filename4))  # RIGHT BOTTOM
    psd_leftbottom.make_bigchair("{}/{}".format(root, "chair_btn.png"), psd_rightbottom.psd, "down")
    psd_leftbottom.save_psd("{}/{}".format(root,filename3.replace(".psd","_LEFT_BOTTOM.psd")))
    psd_rightbottom.save_psd("{}/{}".format(root,filename4.replace(".psd","_RIGHT_BOTTOM.psd")))
    gs.send_log("Processing BTN right/left picture Finished", level="info", color=Color.YELLOW)

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
    equit = gs.choose_equipment()
    psd.load_psd("{}/src/Avatar_{}.psd".format(root,equit))
    pics = psd.load_mapleson_png_with_json(default_folder[parse_folder])
    psd.load_png(default_folder[parse_folder],pics=pics)
    psd.save_psd("{}/Avatar_{}_Done.psd".format(root,equit))


def menu():
    menu = [
        lang["menu_title"],
        lang["option_auto_align"],
        lang["option_align_by_maplesimulater"],
        lang["option_convert_psd_to_gif"],
        lang["option_make_big_chair_2"],
        lang["option_make_big_chair_4"],
        lang["option_exit"]
    ]
    while True:
        print("\n".join(menu))
        user_choice = input(lang["prompt_enter_choice"])
        gs.send_log("{} {}".format(lang['prompt_user_choise'],user_choice), level="info", color=Color.YELLOW)
        if user_choice == "1":
            gs.send_log(lang["info_auto_align_selected"], level="info", color=Color.GREEN)
            create_psd_by_png()
        elif user_choice == "2":
            equit = gs.choose_equipment()
            filename = "Avatar_{}".format(equit)
            url = gs.get_maplesimu_url()
            if url is None:
                gs.send_log(lang['Maplestory_Simulater_Link_invalid'],"error", Color.RED)
                continue
            gs.send_log(lang['processing_url'],"info",Color.GREEN)
            maples_im_align(url,filename)
            # maples_im_align("https://maplestory.io/api/character/%7B%22itemId%22%3A2000%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A12000%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A1703140%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A1032005%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A50101%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A60136%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A1103305%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A1053024%2C%22version%22%3A%22255%22%7D/download?showears=false&showLefEars=false&showHighLefEars=undefined&resize=1&name=&flipX=undefined")
            # maples_im_align("https://maplestory.io/api/character/%7B%22itemId%22%3A2000%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A12000%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A1011011%2C%22animationName%22%3A%22default%22%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A1103100%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A1054169%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A1005407%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A1703001%2C%22version%22%3A%22255%22%7D/download?showears=false&showLefEars=false&showHighLefEars=undefined&resize=1&name=&flipX=false&bgColor=222,35,35,0")
            # maples_im_align("https://maplestory.io/api/character/%7B%22itemId%22%3A2000%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A12000%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A1053441%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A54537%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A40880%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A1103684%2C%22version%22%3A%22255%22%7D%2C%7B%22itemId%22%3A1703418%2C%22version%22%3A%22255%22%7D/download?showears=false&showLefEars=false&showHighLefEars=true&resize=1&name=&flipX=undefined")
        elif user_choice == "3":
            gs.send_log(lang["info_convert_psd_to_gif_selected"], level="info", color=Color.GREEN)
            filename = input(lang["prompt_enter_filename"])
            preview(filename)
        elif user_choice == "4":
            filename = gs.choose_file(root,["psd"])
            # filename = input(lang["prompt_enter_psd_filename"])
            equit = gs.choose_equipment()
            filename2 = "Avatar_{}.psd".format(equit)
            pic_name = gs.choose_file(root, ['png', 'jpg', 'jpeg'])
            # pic_name = input(lang["prompt_enter_chair_image"])
            err_cnt = 0
            ret, filename = gs.check_file_exists(root,filename,File_type.PSD)
            err_cnt += ret
            pic_name = gs.find_picture(root,pic_name)
            if pic_name is None:
                err_cnt += ret
            if err_cnt != 0:
                gs.send_log("Error: {} file(s) not found".format(err_cnt), level="error", color=Color.RED)
                continue
            make_chair_2pic(pic_name,filename,filename2)
        elif user_choice == "5":
            # filename = input(lang["prompt_enter_psd_filename"])
            filename = gs.choose_file(root, ["psd"])
            # pic_name = input(lang["prompt_enter_chair_image"])
            pic_name = gs.choose_file(root, ['png', 'jpg', 'jpeg'])
            err_cnt = 0
            ret, filename = gs.check_file_exists(root,filename,File_type.PSD)
            err_cnt += ret
            pic_name = gs.find_picture(root,pic_name)
            if pic_name is None:
                err_cnt += ret
            if err_cnt != 0:
                gs.send_log("Error: {} file(s) not found".format(err_cnt), level="error", color=Color.RED)
                continue
            make_chair_4pic(pic_name,filename)
        
        elif user_choice == "0":
            gs.send_log(lang["info_exit_program"], level="info", color=Color.GREEN)
            break
        else:
            gs.send_log(lang["error_invalid_choice"].format(user_choice), level="error", color=Color.RED)
            continue
        gs.send_log("{} {} Finished. \n\n".format(lang['prompt_user_choise'],user_choice), level="info", color=Color.YELLOW)



if __name__ == "__main__":
    try:
        language = gs.get_local_info()
        if gs.check_support_language(language):
            lang = gs.load_language(language)
        else:
            lang = gs.load_language("EN")
        gs.show_info()
        menu()
    except Exception as e:
        gs.send_log("Error: {}".format(e), level="error", color=Color.RED)
        input(lang["prompt_press_enter_to_exit"])