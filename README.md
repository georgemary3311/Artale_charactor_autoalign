# Artale_charactor_autoalign

## Environment
1. psd-tools          1.10.4
2. opencv-python      4.10.0.84

## 使用方法
1. 於https://maples.im/# 捏好自己的角色並下載行走圖
2. 把程式碼下載下來 把行走圖解壓縮放到與程式同個資料夾
3. 執行 python main.py
4. 會生成cape.psd，跑完後再打開來檢查是否有對齊完成


## 注意事項
1. 因為對齊圖片是使用open cv的matchTemplate 去做對齊，所以如果腳色過於複雜 PSD檔案中的位置會有誤，請自行調整

## 參考使用方法
https://youtube.com/live/c2HatnjVlcE
如果沒有photoshop，我是用https://krita.org/zh-tw/
