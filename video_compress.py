import subprocess
import os
import tkinter as tk
from tkinter import filedialog

# 支持的视频格式列表
supported_formats = ['.mov', '.mp4']

def compress_video(file_paths):
    for input_path in file_paths:
        file_name = os.path.basename(input_path)
        if any(file_name.lower().endswith(ext) for ext in supported_formats):
            # 添加 'minify_' 前缀到原始文件名
            output_file_name = 'minify_' + file_name
            output_path = os.path.join(os.path.dirname(input_path), output_file_name)
            
            # 构建FFmpeg命令
            command = [
                'ffmpeg',
                '-i', input_path,           # 输入文件
                '-c:v', 'libx265',          # 视频编码器为H.265
                '-crf', '18',               # 常用CRF值
                '-c:a', 'aac',              # 音频编码器
                '-b:a', '128k',             # 音频比特率
                output_path                # 输出文件
            ]
            
            # 执行命令
            subprocess.run(command, check=True)

def select_files():
    # 创建一个Tkinter窗口并隐藏
    root = tk.Tk()
    root.withdraw()
    
    # 打开文件选择对话框，允许选择多个文件
    file_paths = filedialog.askopenfilenames(
        title='选择文件',
        filetypes=(("视频文件", "*.mov *.mp4"), ("所有文件", "*.*"))
    )
    return file_paths

# 使用GUI选择文件
file_paths = select_files()
compress_video(file_paths)
