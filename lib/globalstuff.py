import json
import os
import logging
import sys
import tkinter as tk
from enum import Enum
from PIL import Image, ImageTk, ImageSequence
from colorama import init 
import threading
init()

working_dir = os.getcwd()
lang = ""
logger = None


class Color(Enum):
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"

class File_type(Enum):
    PSD = ".psd"
    PNG = ".png"
    JSON = ".json"
    ZIP = ".zip"
    TXT = ".txt"
    JPG = ".jpg"
    GIF = ".gif"

class Equipment(Enum):
    CAPE = "Cape"
    COAT = "Coat"
    PANTS = "Pants"
    GLOVES = "Gloves"
    SHOES = "Shoes"
    LONGCOAT = "Longcoat"


class globalstuff:
    def __init__(self):
        global logger
        logger = self.init_logger()

    # Load language file
    '''
    Function Name:  load_language
    Description:    Loading language json file from language folder
    Auther:         George Chang
    '''
    def load_language(self,language="EN"):
        global lang
        self.send_log(f"Loading language file: {language}", level="info", color=Color.YELLOW)
        lang_EN = None
        # prevent language setting missing.
        if language != "EN":
            with open(f"{working_dir}/language/EN.json", "r", encoding="utf-8") as file:
                lang_EN = json.load(file)
        with open(f"{working_dir}/language/{language}.json", "r", encoding="utf-8") as file:
            lang = json.load(file)
        if lang_EN != None:
            for key in lang.keys():
                if key in lang_EN:
                    lang_EN[key]= lang[key]
            return lang_EN
        return lang 
        
    '''
    Function Name:  check_support_language
    Description:    Check if a specific language is supported by verifying its existence in the language folder
    Author:         George Chang
    '''
    def check_support_language(self,language):
        l = os.listdir(f"{working_dir}/language")
        for lang in l:
            if language in lang:
                return True
        return False

    '''
    Function Name:  get_local_info
    Description:    Retrieve the system's default locale information, including language and encoding
    Author:         George Chang
    '''
    def get_local_info(self):
        import locale
        language, encoding = locale.getdefaultlocale()
        self.send_log(f"System Language: {language}", level="info", color=Color.YELLOW)
        return language
    
    '''
    Function Name:  show_info
    Description:    Display basic information about the tool, including its name, version, and author
    Author:         George Chang
    '''
    def show_info(self):
        infos = ['Artile Little Tool', 'Version: 1.0.6', 'Author: George.Chang', 'Release Date: 2025/05/10']
        for info in infos:
            self.send_log(info, level="info", color=Color.YELLOW)

    '''
    Function Name:  init_logger
    Description:    Initialize a logger to handle logging for the application, including creating log files
    Author:         George Chang
    '''
    def init_logger(self):
        import os
        import logging

        logger = logging.getLogger("Artile Little Tool")
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:  # ✅ 防止重複加 handler
            os.makedirs(f"{working_dir}/log", exist_ok=True)

            handler = logging.FileHandler(f"{working_dir}/log/artile_little_tool.log", encoding='utf-8')
            handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            logger.addHandler(handler)

        return logger

    '''
    Function Name:  send_log
    Description:    Log messages to both the console and the log file with optional color formatting
    Parameters:     message (str): The message to log
                    level (str): The log level (e.g., info, debug, warning, error, critical)
                    color (Color): The color to use for console output
    Author:         George Chang
    '''
    def send_log(self, message, level="info", color=Color.RESET):
        print(color.value + message + Color.RESET.value)
        global logger
        if level.lower() == "info":
            logger.info(message)
        elif level.lower() == "debug":
            logger.debug(message)
        elif level.lower() == "warning":
            logger.warning(message)
        elif level.lower() == "error":
            logger.error(message)
        elif level.lower() == "critical":
            logger.critical(message)
        else:
            raise ValueError("Invalid log level specified.")
        

    def download(self,url,file):
        import requests
        file_name = file
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.send_log(f"{lang['prompt_download_file']}:{url}", level="info", color = Color.GREEN)
        for i in range(5):
            response = requests.get(url, headers=headers)
            # 檢查 HTTP 回應狀態碼
            if response.status_code == 200:
                # 儲存檔案
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                self.send_log(f"Download file successfully :{file_name}", level="info", color=Color.GREEN)
                return 0
            else:
                self.send_log(f"Failed to download file: {file_name}", level="error", color=Color.RED)
                self.send_log(f"HTTP Status Code: {response.status_code}", level="error", color=Color.RED)
        return 1
            

    def unzip_file(self,path,name):
        import zipfile
        zip_filename = '{}/{}'.format(path,name)
        if ".zip" not in zip_filename:
            zip_filename += ".zip"
        if not os.path.exists(zip_filename):
            self.send_log(f"File not found: {zip_filename}", level="error", color=Color.RED)
            return 1
        extract_to_directory = '{}/{}/'.format(path,name.replace('.zip',''))
        # 解壓縮文件
        self.send_log(f"{lang['prompt_unzipfile']} {zip_filename} to {extract_to_directory}", level="info", color=Color.YELLOW)
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
            zip_ref.extractall(extract_to_directory)
        return 0

    def check_file_exists(self, path, name, type):
        import os
        
        if not os.path.exists(path):
            self.send_log(f"Path not found: {path}", level="error", color=Color.RED)
            return 1, None
        self.send_log(f"Checking if file exists: {path}/{name} , Type:{type}", level="info", color=Color.YELLOW)
        lists = os.listdir(path)
        if type.value not in name:
            name += type.value
        if name in lists:
            self.send_log(f"File found: {name}", level="info", color=Color.GREEN)
            return 0, name
        else:
            self.send_log(f"File not found: {name}", level="error", color=Color.RED)
            return 1, None
        
    def find_picture(self, path, name):
        ret, name_png = self.check_file_exists(path, name, File_type.PNG)
        ret2, name_jpg = self.check_file_exists(path, name, File_type.JPG)
        if ret == 0:
            return name_png
        elif ret2 == 0:
            return name_jpg
        else:
            self.send_log(f"File not found: {name}", level="error", color=Color.RED)
            return None

    def choose_equipment(self):
        self.send_log(lang['choose_equip'], level="info", color=Color.YELLOW)
        options = [e.value for e in Equipment]
        for index, option in enumerate(options):
            self.send_log(f"{index + 1}. {lang[option]}", level="info", color=Color.YELLOW)
        choice = input("Enter the number of your choice: ")
        try:
            choice = int(choice) - 1
            if 0 <= choice < len(options):
                selected_equipment = options[choice]
                self.send_log(f"You selected: {lang[selected_equipment]}", level="info", color=Color.GREEN)
                return selected_equipment
            else:
                self.send_log(lang['choise_number_from_list'], level="error", color=Color.RED)
                return None
        except Exception as e:
            self.send_log(f"Error: {e}", level="error", color=Color.RED)
            return None
        
    def list_folder_files(self, path, target_type=[]):
        import os
        known_files = [ "README.md", "main.py"]
        if not os.path.exists(path):
            self.send_log(f"Path not found: {path}", level="error", color=Color.RED)
            return 1, None
        self.send_log(f"Listing files in folder: {path}", level="info", color=Color.YELLOW)
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        files = [f for f in files if f not in known_files]
        filelist = []
        for file in files:
            for t in target_type:
                if file.endswith(t):
                    filelist.append(file)
                    self.send_log(f"File found: {file}", level="info", color=Color.GREEN)
        return filelist
    
    def choose_file(self, path, target_type=[]):
        import os
        files = self.list_folder_files(path, target_type)
        if len(files) == 0:
            self.send_log(f"Error listing files in folder: {path}", level="error", color=Color.RED)
            return None
        self.send_log(lang['prompt_choose_file'].format(','.join(target_type)), level="info", color=Color.YELLOW)
        for index, file in enumerate(files):
            self.send_log(f"{index + 1}. {file}", level="info", color=Color.GREEN)
        choice = input(lang['prompt_enter_file_choice'])
        try:
            choice = int(choice) - 1
            if 0 <= choice < len(files):
                selected_file = files[choice]
                self.send_log(f"You selected: {selected_file}", level="info", color=Color.GREEN)
                return selected_file
            else:
                self.send_log("Invalid choice. Please enter a number from the list.", level="error", color=Color.RED)
                return None
        except Exception as e:
            self.send_log(f"Error: {e}", level="error", color=Color.RED)
            return None
        
    def get_maplesimu_url(self):
        for i in range(5):
            ipt = input(lang['prompt_enter_url_link'])
            if "help" in ipt.lower():
                self.play_gif("src/maplesimulater_help.gif")
                continue
            if "exit" in ipt.lower():
                return None
            if "maplestory.io/api/character" in ipt:
                return ipt
        return None


    def play_gif(self,path):
        import cv2
        from PIL import Image, ImageSequence
        import numpy as np
        import time
        gif = Image.open(path)
        frames = [frame.copy().convert("RGB") for frame in ImageSequence.Iterator(gif)]
        duration = gif.info.get('duration', 100) / 1000.0  # 毫秒轉秒

        for frame in frames:
            frame_np = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
            cv2.imshow("GIF Viewer", frame_np)
            if cv2.waitKey(int(duration * 1000)) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()