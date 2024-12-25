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

4. 會生成Cape.psd，跑完後再打開來檢查是否有對齊完成

### GIF生成
1. 根據執行方法可以選擇以下兩種，python程式執行或是執行檔

1.1 執行 python main.py 並選擇選項二

1.2 執行 Autoalign.exe 選擇選項二

2. 輸入需要轉換成gif的PSD檔案名稱(PSD檔案建議先把圖層合好，會節省時間)
3. 即會生成PREVIEW資料夾

### 製作大椅子
參考影片:https://youtu.be/0pxWmT5UbOw
1. 根據執行方法可以選擇以下兩種，python程式執行或是執行檔

1.1 執行 python main.py 並選擇選項三

1.2 執行 Autoalign.exe 選擇選項三

2. 輸入要作為基礎的PSD檔案名稱
3. 輸入要置入的椅子圖片的名稱(444*250與479*250 試過皆可)

## 注意事項
1. 因為對齊圖片是使用open cv的matchTemplate 去做對齊，所以如果腳色過於複雜 PSD檔案中的位置會有誤，請自行調整
   
2.1 EXE FILE 下載路徑:[Google Drive](https://drive.google.com/file/d/1h1rTRnMHGyzBWclMnHIEhjp5hiuCaLf-/view?usp=sharing)

2.2 下載後放到與main.py相同的資料夾之後如上述使用方法執行

3. 歡迎提出想法與一起解BUG

## 參考使用方法
https://youtube.com/live/c2HatnjVlcE

如果沒有photoshop，我是用https://krita.org/zh-tw/

## 更新Note:
20241216
1. 支援psd to gif
2. 支援大椅子(兩件裝備)的製作
20241215:
1. 支援maplesalon自動判斷檔名

