# Artale_charactor_autoalign

## Environment
1. psd-tools          1.10.4
2. opencv-python      4.10.0.84

## 使用方法 
* 完整demo video: https://youtu.be/qCrf0S1Wksw
### Auto Align

1. 於https://maples.im/# 捏好自己的角色並下載行走圖 或是透過maplesalon2所捏的腳色並匯出分鏡
(https://github.com/spd789562/MapleSalon2/releases/tag/app-v0.6.3)
2. 把程式碼下載下來 把行走圖解壓縮放到與程式同個資料夾
3. 根據執行方法可以選擇以下兩種，python程式執行或是執行檔

3.1 執行 python main.py 並選擇選項一

3.2 執行 Autoalign.exe 選擇選項一
4. 目前可以選擇使用的檔案，來源於src資料夾
5. 會生成XXX_DONE.psd，跑完後再打開來檢查是否有對齊完成

### GIF生成
1. 根據執行方法可以選擇以下兩種，python程式執行或是執行檔

1.1 執行 python main.py 並選擇選項二

1.2 執行 Autoalign.exe 選擇選項二

2. 輸入需要轉換成gif的PSD檔案名稱(PSD檔案建議先把圖層合好，會節省時間)
3. 即會生成PREVIEW資料夾

### 製作大椅子(兩張圖片版本)
參考影片:https://youtu.be/0pxWmT5UbOw
1. 根據執行方法可以選擇以下兩種，python程式執行或是執行檔

1.1 執行 python main.py 並選擇選項三

1.2 執行 Autoalign.exe 選擇選項三

2. 選擇要使用的PSD檔案
3. 選擇要使用的另外一個裝備種類
4. 選擇要使用的椅子圖片

### 製作大椅子(四張圖片版本)
1. 根據執行方法可以選擇以下兩種，python程式執行或是執行檔

1.1 執行 python main.py 並選擇選項四

1.2 執行 Autoalign.exe 選擇選項四

2. 選擇要使用的PSD檔案(建議使用Cape)
3. 選擇要使用的椅子圖片

* 他會把圖片分成以下順序來切割圖片放到PSD同時調整紅點(目前沒有所有size的圖片都試過)
CAPE  | COAT
一一一十一一一
GLOVES| PANTS

## 注意事項
1. 使用maple simulater對齊圖片是使用open cv的matchTemplate 去做對齊，所以如果腳色過於複雜 PSD檔案中的位置會有誤，請自行調整
2. ![image](https://github.com/user-attachments/assets/713b4d86-4ddd-4e65-9a5e-e149ef1c93ad)如果使用maplesason2，請關閉此選項，並且在匯出時選擇強制匯出特效
   
2.1 EXE FILE 下載路徑:[Google Drive](https://drive.google.com/drive/folders/1L3WprF8cyESB7CdYgiiexKBZPfNlOL9I?usp=sharing)

2.2 下載後放到與main.py相同的資料夾之後如上述使用方法執行


## 參考使用方法
https://youtube.com/live/c2HatnjVlcE

如果沒有photoshop，我是用https://krita.org/zh-tw/

## 更新Note:
20241216
1. 支援psd to gif
2. 支援大椅子(兩件裝備)的製作
   
20241215:
1. 支援maplesalon自動判斷檔名
   
20250505
1. Fix maplesalon stabtf failed issue
2. Support multiple language
3. Fix two equip chair making offset
4. Support four equips chair making
5. Change Reading file by entering option
6. Support recording log
