import os
from PIL import Image

# 画像ファイルの拡張子リスト
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

# リサイズ後の画像サイズ
new_size = (1080, 1080)

def get_image_files(directory):
    # ディレクトリ内のファイルを取得
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 画像ファイルかどうかをチェック
            if any(file.lower().endswith(ext) for ext in image_extensions):
                yield os.path.join(root, file)

def resize_image(file_path, size):
    try:
        with Image.open(file_path) as img:
            # 画像をリサイズして保存
            img_resized = img.resize(size, Image.Resampling.LANCZOS)
            img_resized.save(file_path)
            print(f"Resized {file_path} to {size}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    # 現在の作業ディレクトリを取得
    current_directory = os.getcwd()
    for image_file in get_image_files(current_directory):
        resize_image(image_file, new_size)

if __name__ == "__main__":
    main()
