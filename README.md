# 🛑 最新版撲滅君 / Saishinban Bokumetsu-kun

## 🇯🇵 日本語説明

このアプリは、**「最新版」や「新最新版」など、紛らわしいファイル名**を付けたときに通知してくれるアプリです。  
ファイル管理の混乱を防ぎ、わかりやすい命名をサポートします。

> 📝 **検出例:**  
> 📄 〇〇最新版  
> 📄 〇〇新最新版  
> 📄 〇〇新最新版改  
> 📄 〇〇最終最新版  
> 📄 〇〇完成版最新版  

---

**Boothで販売もしているので、気になった方や支援したい方はぜひご購入ください。**  
**※GitHubリポジトリとアプリ版のアップデート適用には、1日～1週間程度のズレが生じる場合があります。**

**Boothリンク**  
[最新版撲滅君 - Booth](https://nsan.booth.pm/items/6678312)

---

### ✨ 主な機能

- 📂 指定フォルダ内のファイル名を監視  
- 🔔 特定キーワードを含むファイル名を検知すると通知  
- 🖥️ タスクトレイ常駐  
- 🗂️ キーワードやディレクトリの履歴保存・選択  
- ⏯️ 監視の開始・停止が可能  

---

### 🛠️ 必要ライブラリ

- 🐍 Python 標準ライブラリ  
- 🖱️ pystray  
- 🔔 win10toast  
- 🪟 tkinter  
- 🖼️ PIL (Pillow)  
- 📱 plyer（一部バージョンで使用）  
- その他  

---

## 🇬🇧 English Description

This app notifies you when you create files with **misleading or redundant names** such as “latest version” in a specified folder.  
It helps keep your file naming clear and organized.

---

**This app is also available for purchase on Booth. If you are interested or would like to support the development, please consider buying it.**  
**Please note that updates between the GitHub repository and the app version may have a delay of about 1 day to 1 week.**

**Booth Link**  
[最新版撲滅君 - Booth](https://nsan.booth.pm/items/6678312)

---

> 📝 **Examples detected:**  
> 📄 xxx_latest  
> 📄 xxx_new_latest  
> 📄 xxx_new_latest_rev  
> 📄 xxx_final_latest  
> 📄 xxx_completed_latest  

---

### ✨ Main Features

- 📂 Monitor file names in a specified folder  
- 🔔 Notify when a file name contains a specific keyword  
- 🖥️ Run in the system tray  
- 🗂️ Save and select keyword/directory history  
- ⏯️ Start and stop monitoring  

---

### 🛠️ Required Libraries

- 🐍 Python standard library  
- 🖱️ pystray  
- 🔔 win10toast  
- 🪟 tkinter  
- 🖼️ PIL (Pillow)  
- 📱 plyer (used in some versions)  
- others  

---

## 🚀 使い方 / Usage

### 🇯🇵 日本語

1. Python 3.x がインストールされていることを確認してください。  
2. 以下の必要ライブラリをインストールします：  
   ```bash
   pip install pystray win10toast pillow plyer
※ tkinter は多くの環境で標準搭載されています。

3. Dev.py または nodebugvar.py を実行します。
4. タスクトレイのアイコンから監視ディレクトリやキーワードを設定できます。

### 🇬🇧 English

1. Make sure Python 3.x is installed.

2. Install the required libraries:

   ```bash
   pip install pystray win10toast pillow plyer
※ tkinter is included by default in many environments.

3. Run Dev.py or nodebugvar.py.

4. Set the monitoring directory and keywords from the system tray icon.
