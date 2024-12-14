import os
from lib.psd_utils import psd_utils as psdutil

root=os.getcwd()



if __name__ == "__main__":
    psd = psdutil()
    psd.load_psd("{}/src/Avatar_Cape.psd".format(root))
    psd.load_png("{}/CharacterSpriteSheet/default/0/".format(root))
    # psd.layers['edithere:cape_capeBelowBody_83'].visible = False 
    # psd.show_psd()

    psd.save_psd("{}/Cape.psd".format(root))