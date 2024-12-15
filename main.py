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


if __name__ == "__main__":
    if check_folder():
        os._exit()
    psd = psdutil()
    psd.load_psd("{}/src/Avatar_Cape.psd".format(root))
    psd.load_png(default_folder[parse_folder])
    # psd.layers['edithere:cape_capeBelowBody_83'].visible = False 
    # psd.show_psd()

    psd.save_psd("{}/Cape.psd".format(root))