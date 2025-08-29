import zipfile
import os

def zip_conf_folder(source_folder, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder, topdown=False):
            # 先处理子目录和文件，再处理父目录
            for name in files + dirs:
                path = os.path.join(root, name)
                arcname = os.path.relpath(path, source_folder)
                if os.path.isdir(path):
                    arcname += '/'  # 标记为目录
                zipf.write(path, arcname)

zip_conf_folder("conf", "6_area_conf.zip")  