# EDIDREADER

EDID 解析器

## 解析能力

* Standard `00 FF FF FF FF FF FF FF 00`
* CTA Extension `02 03`
* Display ID `70`
* Block Map `F0`(分析後，跳過該區塊)

## 使用後你將可以得到

* 基本顯示器資訊(Header Info)
* 詳細時序描述區塊(DTDs or Display Descriptors)
* 視訊格式(VDB)
* 音訊格式(ADB)
* 聲道配置(SADB)
* 供應商_視訊格式(VSDB)

## 介面

應用程式圖示
<!-- markdownlint-disable MD033 -->

<img src="https://raw.githubusercontent.com/Ken-Huang-PX/edid_parser_image/main/image.png" alt="alt text" width="120">

執行介面(日間模式)

<img src="https://raw.githubusercontent.com/Ken-Huang-PX/edid_parser_image/main/image_1.png" alt="alt text" width="600">

執行介面(夜間模式)

<img src="https://raw.githubusercontent.com/Ken-Huang-PX/edid_parser_image/main/image_2.png" alt="alt text" width="600">

## How to use

1. 先打開應用程式，他會先顯示你現在的螢幕資訊

    <img src="https://raw.githubusercontent.com/Ken-Huang-PX/edid_parser_image/main/image_4.png" alt="alt text" width="600">

2. 將顯示器插入電腦的HDMI或DP介面

3. 按下`重新整理顯示器資訊`按鈕

    你會看到內容更新，順序應該是依照註冊表的排序

    <img src="https://raw.githubusercontent.com/Ken-Huang-PX/edid_parser_image/main/image_5.png" alt="alt text" width="600">

4. 右上方會顯示目前的顯示器數量

    <img src="https://raw.githubusercontent.com/Ken-Huang-PX/edid_parser_image/main/image_6.png" alt="alt text" width="300">

5. 按下`匯出資訊`按鈕

    你將可以匯出目前所有顯示器資訊
    * txt 主要拿來編輯，html 是提供給其他人檢視
    <img src="https://raw.githubusercontent.com/Ken-Huang-PX/edid_parser_image/main/image_7.png" alt="alt text" width="600">

    * 匯出樣式(*.txt)
    <img src="https://raw.githubusercontent.com/Ken-Huang-PX/edid_parser_image/main/image_8.png" alt="alt text" width="600">

    * 匯出樣式(*.html)
    <img src="https://raw.githubusercontent.com/Ken-Huang-PX/edid_parser_image/main/image_9.png" alt="alt text" width="600">

## EDID 簡介(不熟悉EDID的請看這)

每個區塊有對應的開頭描述

* 標準區塊

  * 開頭`00 FF FF FF FF FF FF 00`
  * 必須為首個block
  * 最高的解析規格放在DTD，包括`首選時序解析度`、`最大時序解析度`、`最大垂直更新率`，已經過計算取得

* CTA擴充區塊

  * 開頭`02 03`
  * 通常為第二個
  * 遇到F0會往後推移
  * 所有的解析度都放在VDB，以vic描述，每個VIC有自己對應的解析度參數，詳細參閱目錄 /hdmi_spec/vic表格
  * 音訊格式(LPCM、AC3...)
  * 聲道配置(FL/FR、LFE...)
  * VSDB，主要是看CEA Physical Address(PA)，有時候CEC錯誤是因為這裡分配錯誤
  * 最高解析度規格放在DTD，以`時序解析度`描述，已經過計算取得

* DisplayID區塊
  * 開頭`70`
  * 通常為第三個
  * 遇到F0會往後推移
  * 容易在出現在hdmi 2.1
  * 整區塊都以`時序解析度`描述，已經過計算取得

* BlockMap區塊

  * 開頭`F0`
  * 通常為第二個
  * 雖然早就有定義在規格書，但似乎是hdmi 2.0->2.1過渡期
  * 容易在出現在hdmi 2.1
  * 描述著此block之後的區塊類型，比如`F0 02 70`代表下一個是cta，再下一個是DP

容易產生解析度錯誤的EDID

* 擴充數錯誤

        倒數第二位元組，也就是checksum旁邊的那個數字，如果錯誤通常會在影音串流盒發現解析度錯誤

* Checksum 錯誤

        每個block的最後一個位元組都是checksum，如果錯誤容易被判定為無效EDID，通常是更改擴充數導致

* VIC 填寫缺漏

        在cta block中，有關於video data block(VDB)的描述，vic是填寫關於解析度與更新率的資料卡，容易發生在splitter分配EDID給sink端的時候，如果填寫缺漏，會導致選取不到該解析度
        
* CEA PA 錯誤

        全名是CEA Physical Address (CEA物理位置)
        如果錯誤的分配這項，可能會讓CEC功能喪失或誤觸，在switcher容易發生
