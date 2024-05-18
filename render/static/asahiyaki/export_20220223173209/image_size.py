import os
from PIL import Image

# 画像ファイルの拡張子リスト
image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

def get_image_files(directory):
    # ディレクトリ内のファイルを取得
    for root, dirs, files in os.walk(directory):
        for file in files:
            # 画像ファイルかどうかをチェック
            if any(file.lower().endswith(ext) for ext in image_extensions):
                yield os.path.join(root, file)

def get_image_size(file_path):
    with Image.open(file_path) as img:
        return img.size

def main():
    current_directory = os.getcwd()
    for image_file in get_image_files(current_directory):
        try:
            size = get_image_size(image_file)
            print(f"{image_file}: {size}")
        except Exception as e:
            print(f"Error processing {image_file}: {e}")

if __name__ == "__main__":
    main()
