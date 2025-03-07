import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def is_empty_dir(dirpath):
    try:
        # ディレクトリ名が #recycle を含む場合はスキップ
        if "#recycle" in dirpath.lower():
            return None
        # ディレクトリ内のファイルとサブディレクトリを取得
        if not os.listdir(dirpath):
            return dirpath
    except PermissionError:
        pass
    return None

def find_empty_dirs(root_dir):
    empty_dirs = []
    with ThreadPoolExecutor(max_workers=4) as executor:  # i3-12100Fは4コアなので4スレッドを指定
        futures = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            if not filenames and not dirnames:
                futures.append(executor.submit(is_empty_dir, dirpath))
        
        for future in futures:
            result = future.result()
            if result:
                empty_dirs.append(result)
    
    return empty_dirs

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Tkinterのウィンドウを非表示にする
    root_dir = filedialog.askdirectory(title="検索するディレクトリを選択してください")
    
    if not root_dir:
        print("ディレクトリが選択されませんでした。")
    elif not os.path.exists(root_dir):
        print("指定されたディレクトリが存在しません。")
    else:
        empty_dirs = find_empty_dirs(root_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = f"result_{timestamp}.txt"
        
        with open(result_file, "w", encoding="utf-8") as file:
            if empty_dirs:
                file.write("ファイルが存在しないディレクトリ一覧:\n")
                for d in empty_dirs:
                    file.write(f"{d}\n")
                print(f"結果が {result_file} に書き出されました。")
            else:
                file.write("空のディレクトリは存在しません。\n")
                print("空のディレクトリは存在しません。")
