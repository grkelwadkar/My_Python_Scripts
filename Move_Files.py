
import os
import shutil


path = r'C:\Users\grkel\Downloads'
destination_path_zip = r'C:\Users\grkel\Downloads\Zip_Files'  # or just '/path/to/destination/'
destination_path_pdf = r'C:\Users\grkel\Downloads\PDFs'  # or just '/path/to/destination/'
destination_path_images = r'C:\Users\grkel\Downloads\Images'  # or just '/path/to/destination/'
destination_path_docs = r'C:\Users\grkel\Downloads\Docs'  # or just '/path/to/destination/'
destination_path_videos = r'C:\Users\grkel\Downloads\Videos'  # or just '/path/to/destination/'
destination_path_excel = r'C:\Users\grkel\Downloads\Sheets'  # or just '/path/to/destination/'
destination_path_web = r'C:\Users\grkel\Downloads\Web Files'  # or just '/path/to/destination/'
destination_path_exe = r'C:\Users\grkel\Downloads\Executables'  # or just '/path/to/destination/'
destination_path_text = r'C:\Users\grkel\Downloads\Text Files'  # or just '/path/to/destination/'
#print(os.getcwd())


for f in os.listdir(path):
    full_path = os.path.join(path,f)

    if os.path.isdir(full_path):
        continue
    else:
        if f.lower().endswith('.zip'):
            shutil.move(full_path,os.path.join(destination_path_zip,f))
        if f.lower().endswith('.pdf'):
            shutil.move(full_path,os.path.join(destination_path_pdf,f))
        if f.lower().endswith('.jpg') or f.lower().endswith('.png'):
            shutil.move(full_path,os.path.join(destination_path_images,f))
        if f.lower().endswith('.doc') or f.lower().endswith('.docx'):
            shutil.move(full_path,os.path.join(destination_path_docs,f))
        if f.lower().endswith('.mp4'):
            shutil.move(full_path,os.path.join(destination_path_videos,f))
        if f.lower().endswith('.xls') or f.lower().endswith('.xlsx') or f.lower().endswith('.csv'):
            shutil.move(full_path,os.path.join(destination_path_excel,f))
        if f.lower().endswith('.json') or f.lower().endswith('.htm') or f.lower().endswith('.html'):
            shutil.move(full_path,os.path.join(destination_path_web,f))
        if f.lower().endswith('.exe') or f.lower().endswith('.msi'):
            shutil.move(full_path,os.path.join(destination_path_exe,f))
        if f.lower().endswith('.txt') :
            shutil.move(full_path,os.path.join(destination_path_text,f))















