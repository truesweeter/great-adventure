import os
import sys
import shutil


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_writable_path(filename, subfolder="data"):
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(".")

    target_dir = os.path.join(base_dir, subfolder)
    os.makedirs(target_dir, exist_ok=True)

    target_file = os.path.join(target_dir, os.path.basename(filename))
    if getattr(sys, 'frozen', False) and not os.path.exists(target_file):
        try:
            src_file = os.path.join(sys._MEIPASS, filename)
            shutil.copy2(src_file, target_file)
        except Exception as e:
            print(f"Не удалось скопировать {filename} из временной папки: {e}")
    return target_file
