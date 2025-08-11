import os
import time
import threading
import tkinter as tk
from tkinter import filedialog
from pystray import Icon, Menu, MenuItem
from PIL import Image
from win10toast import ToastNotifier
import logging
import json

# ログ設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 設定値や状態管理用のクラス
class MonitorConfig:
    def __init__(self):
        self.target_keyword = ""      # 監視対象のキーワード
        self.target_directory = ""    # 監視するフォルダのパス
        self.notified_files = set()   # 通知済みのファイルを保持するセット
        self.save = False             # ディレクトリ保存フラグ

config = MonitorConfig()

# 通知オブジェクトの作成
toaster = ToastNotifier()

# 停止用イベント
monitoring_stop_event = threading.Event()

def quit_app():
    """タスクトレイアプリを終了"""
    try:
        # print("アプリケーションを終了します")
        stop_monitoring_thread()
        icon.stop()
    except Exception as e:
        # print(f"アプリケーション終了エラー: {e}")
        pass

def open_condition_setting_window():
    """監視するファイル名の条件を設定するGUI"""
    try:
        # print("キーワード設定ウィンドウを開きます")
        window = tk.Tk()
        window.geometry("350x300")
        window.title("監視キーワード設定")

        # 保存済みキーワードを読み込む
        try:
            if os.path.exists('saved_keywords.json'):
                with open('saved_keywords.json', 'r') as file:
                    try:
                        saved_keywords = json.load(file)
                        # print(f"保存済みキーワード読み込み: {saved_keywords}")
                    except json.JSONDecodeError:
                        saved_keywords = []
                        # print("キーワードJSONデコードエラー")
            else:
                saved_keywords = []
                # print("キーワード保存ファイルなし")
        except Exception as e:
            saved_keywords = []
            # print(f"キーワードファイル読み込みエラー: {e}")

        entry_keyword = tk.Entry(window)
        entry_keyword.place(x=20, y=30)

        # キーワードリスト表示
        keyword_listbox = tk.Listbox(window)
        for kw in saved_keywords:
            keyword_listbox.insert(tk.END, kw)
        keyword_listbox.place(x=20, y=70, width=200, height=120)

        # キーワード保存
        def save_keyword():
            try:
                keyword = entry_keyword.get()
                # print(f"キーワード保存ボタン押下: '{keyword}'")
                if keyword and keyword.strip():
                    config.target_keyword = keyword
                    if keyword not in saved_keywords:
                        saved_keywords.append(keyword)
                        try:
                            with open('saved_keywords.json', 'w') as file:
                                json.dump(saved_keywords, file, indent=4)
                            keyword_listbox.insert(tk.END, keyword)
                            # print(f"キーワード保存: {keyword}")
                        except Exception as e:
                            # print(f"キーワード保存エラー: {e}")
                            pass
                    entry_keyword.delete(0, tk.END)
                    label_message.config(text=f"'{config.target_keyword}' を監視対象に追加しました")
                else:
                    label_message.config(text="空のキーワードは保存できません")
                    # print("空のキーワードは保存できません")
            except Exception as e:
                # print(f"キーワード保存処理エラー: {e}")
                pass

        # キーワード選択
        def select_keyword():
            try:
                selection = keyword_listbox.curselection()
                # print(f"キーワード選択: {selection}")
                if selection:
                    config.target_keyword = keyword_listbox.get(selection[0])
                    label_message.config(text=f"'{config.target_keyword}' を選択しました")
                    # print(f"キーワード選択: {config.target_keyword}")
                else:
                    label_message.config(text="キーワードを選択してください")
                    # print("キーワードを選択してください")
            except Exception as e:
                # print(f"キーワード選択エラー: {e}")
                pass

        # キーワード選択解除
        def clear_keyword_selection():
            try:
                keyword_listbox.selection_clear(0, tk.END)
                label_message.config(text="キーワードの選択を解除しました")
                # print("キーワード選択解除")
            except Exception as e:
                # print(f"キーワード選択解除エラー: {e}")
                pass

        button_ok = tk.Button(window, text="保存", command=save_keyword)
        button_ok.place(x=230, y=26)
        button_select = tk.Button(window, text="選択", command=select_keyword)
        button_select.place(x=230, y=70)
        button_clear = tk.Button(window, text="選択解除", command=clear_keyword_selection)
        button_clear.place(x=230, y=110)

        label_message = tk.Label(window, text="")
        label_message.place(x=20, y=200)

        def close_window():
            try:
                # print("キーワードウィンドウを閉じます")
                window.destroy()
            except Exception as e:
                # print(f"キーワードウィンドウ終了エラー: {e}")
                pass

        button_quit = tk.Button(window, text="Quit", command=close_window)
        button_quit.pack(side=tk.BOTTOM)

        window.mainloop()
        # print("キーワード設定ウィンドウを閉じました")
    except Exception as e:
        # print(f"キーワード設定ウィンドウエラー: {e}")
        pass

#################################################################################################
# ディレクトリ選択・保存関連
#################################################################################################

def open_directory_saved():
    global saved_directory
    try:
        # print("ディレクトリ選択ウィンドウを開きます")
        config.save = False    
        window = tk.Tk()
        window.geometry("300x400")
        window.title("監視ディレクトリを選択")
        
        label = tk.Label(window, text="監視するディレクトリを選択してください")

        try:
            if os.path.exists('saved_directories.json'):
                with open('saved_directories.json', 'r') as file:
                    try:
                        saved_directories = json.load(file)
                        # print(f"保存済みディレクトリ読み込み: {saved_directories}")
                    except json.JSONDecodeError:
                        saved_directories = []
                        # print("ディレクトリJSONデコードエラー")
            else:
                saved_directories = []
                # print("ディレクトリ保存ファイルなし")
        except Exception as e:
            saved_directories = []
            # print(f"ディレクトリファイル読み込みエラー: {e}")

        option = [
            *saved_directories
        ]

        def saved_directoryTrue():
            try:
                if not config.save:
                    config.save = True
                    # print("保存チェック: True")
                else:
                    config.save = False
                    # print("保存チェック: False")
            except Exception as e:
                # print(f"保存チェックエラー: {e}")
                pass
            return

        check_button = tk.Checkbutton(window, text="保存する", command=saved_directoryTrue)
        save_directory_list = tk.Listbox(window)
        for item in option:
            save_directory_list.insert(tk.END, item)

        def clear_selection():
            try:
                save_directory_list.selection_clear(0, tk.END)
                # print("ディレクトリ選択解除")
            except Exception as e:
                # print(f"ディレクトリ選択解除エラー: {e}")
                pass

        def close_window():
            try:
                selection = save_directory_list.curselection()
                # print(f"ディレクトリ決定ボタン押下: {selection}")
                if selection:
                    selected_dir = save_directory_list.get(selection[0])
                    config.target_directory = selected_dir
                    # print(f"ディレクトリ選択: {config.target_directory}")
                if config.save:
                    try:
                        save_directory()
                        # print("保存が選択されました")
                    except Exception as e:
                        # print(f"ディレクトリ保存エラー: {e}")
                        pass
                    config.save = False
                else:
                    # print("保存は選択されませんでした")
                    pass
                # print("ディレクトリウィンドウを閉じます")
                window.destroy()
            except Exception as e:
                # print(f"ディレクトリウィンドウ終了エラー: {e}")
                pass

        directory_select_button = tk.Button(window, text="ディレクトリ選択", command=open_directory_selection)
        directory_set_button = tk.Button(window, text="決定", command=close_window)
        clear_selection_button = tk.Button(window, text="選択解除", command=clear_selection)

        directory_select_button.pack()
        label.pack()
        check_button.pack()
        save_directory_list.pack()
        clear_selection_button.pack()
        directory_set_button.pack()
        window.mainloop()
        # print("ディレクトリ選択ウィンドウを閉じました")
    except Exception as e:
        # print(f"ディレクトリ選択ウィンドウエラー: {e}")
        pass

def save_directory():
    try:
        # print(f"ディレクトリ保存処理開始: {config.target_directory}")
        if config.target_directory:
            try:
                if not os.path.exists('saved_directories.json'):
                    with open('saved_directories.json', 'w') as file:
                        json.dump([], file)
                    # print("ディレクトリ保存ファイル新規作成")
                with open('saved_directories.json', 'r+') as file:
                    try:
                        saved_directories = json.load(file)
                    except json.JSONDecodeError:
                        saved_directories = []
                        # print("ディレクトリ保存ファイルJSONデコードエラー")
                    if config.target_directory not in saved_directories:
                        saved_directories.append(config.target_directory)
                        file.seek(0)
                        json.dump(saved_directories, file, indent=4)
                        file.truncate()
                        # print(f"ディレクトリ保存: {config.target_directory}")
                    logging.debug(f"保存されたディレクトリ: {saved_directories}")
            except Exception as e:
                # print(f"ディレクトリ保存処理エラー: {e}")
                pass
        else:
            logging.debug("保存するディレクトリが設定されていません")
            # print("保存するディレクトリが設定されていません")
    except Exception as e:
        # print(f"save_directory関数エラー: {e}")
        pass

def open_directory_selection():
    """監視するフォルダを選択するダイアログを開く"""
    initial_directory = "C:\\\\"
    # print("ディレクトリ選択ダイアログを開きます")
    try:
        selected_directory = filedialog.askdirectory(initialdir=initial_directory)
        # print(f"ディレクトリ選択: {selected_directory}")
        if selected_directory:
            config.target_directory = selected_directory
            # print(f"target_directoryに設定: {config.target_directory}")
    except Exception as e:
        # print(f"ディレクトリ選択ダイアログエラー: {e}")
        pass

def monitor_directory():
    logging.debug("monitor_directory 関数が呼び出されました")
    # print("監視スレッド開始")
    try:
        toaster.show_toast(
            "最新版撲滅君",
            "監視開始しました",
            icon_path="_internal/image.ico",
            duration=10,
        )
    except Exception as e:
        # print(f"トースト通知エラー: {e}")
        pass
    while not monitoring_stop_event.is_set():
        # print(f"監視ループ: target_directory={config.target_directory}, target_keyword={config.target_keyword}")
        try:
            if not config.target_directory:
                logging.debug("フォルダが設定されていません")
                # print("監視中断: フォルダが設定されていません")
                time.sleep(5)
                continue

            if not config.target_keyword:
                logging.debug("キーワードが設定されていません")
                # print("監視中断: キーワードが設定されていません")
                time.sleep(5)
                continue

            if not os.path.exists(config.target_directory):
                logging.debug(f"指定されたフォルダが存在しません: {config.target_directory}")
                # print(f"監視中断: 指定されたフォルダが存在しません: {config.target_directory}")
                time.sleep(5)
                continue

            try:
                file_list = os.listdir(config.target_directory)
            except Exception as e:
                # print(f"ファイル一覧取得エラー: {e}")
                file_list = []
            # print(f"監視中: ファイル一覧={file_list}")
            for filename in file_list:
                try:
                    if config.target_keyword in filename and filename not in config.notified_files:
                        # print(f"通知: {filename} が条件に一致")
                        try:
                            toaster.show_toast(
                                "最新版撲滅君",
                                f"ヽ(｀Д´#)ﾉ お前、'{config.target_keyword}' なんてわかりにくい名前つけるんじゃねぇ",
                                icon_path="_internal/image.ico",
                                duration=10,
                            )
                        except Exception as e:
                            # print(f"トースト通知エラー: {e}")
                            pass
                        config.notified_files.add(filename)
                    else:
                        # print(f"スキップ: {filename}")
                        pass
                except Exception as e:
                    # print(f"ファイル監視エラー: {e}")
                    pass
            time.sleep(0.5)
        except Exception as e:
            # print(f"監視ループエラー: {e}")
            time.sleep(5)
    # print("監視スレッド停止")

def clear_notified_files():
    """一定時間ごとに通知済みのファイルリストをクリア（再通知を可能にする）"""
    try:
        while not monitoring_stop_event.is_set():
            # print("通知済みリストをクリアします")
            try:
                for _ in range(600):
                    if monitoring_stop_event.is_set():
                        # print("通知クリアスレッド停止")
                        return
                    time.sleep(1)
                config.notified_files.clear()
                logging.debug("通知済みリストをクリアしました")
            except Exception as e:
                # print(f"通知済みリストクリアエラー: {e}")
                pass
        # print("通知クリアスレッド停止")
    except Exception as e:
        # print(f"clear_notified_files関数エラー: {e}")
        pass

def start_monitoring_thread():
    """`monitor_directory()` をスレッドで実行"""
    # print("監視スレッドを起動します")
    try:
        monitoring_stop_event.clear()
        monitoring_thread = threading.Thread(target=monitor_directory, daemon=True)
        monitoring_thread.start()
        cleanup_thread = threading.Thread(target=clear_notified_files, daemon=True)
        cleanup_thread.start()
    except Exception as e:
        # print(f"スレッド起動エラー: {e}")
        pass

def stop_monitoring_thread():
    """監視スレッドを停止"""
    try:
        # print("監視スレッドを停止します")
        monitoring_stop_event.set()
    except Exception as e:
        # print(f"監視スレッド停止エラー: {e}")
        pass

# アイコン画像を読み込む
# icon_image = Image.open("_internal/image.ico")
icon_image = Image.open("image.ico")
# タスクトレイのメニュー設定
menu = Menu(
    MenuItem("Start Monitoring", start_monitoring_thread),
    MenuItem("Stop Monitoring", stop_monitoring_thread),
    MenuItem("Set Directory", open_directory_saved),
    MenuItem("Set Keyword", open_condition_setting_window),
    MenuItem("Quit", quit_app),
)

# タスクトレイアイコンの作成
icon = Icon(name="monitoring_tool", icon=icon_image, title="最新版撲滅君", menu=menu)
icon.run()