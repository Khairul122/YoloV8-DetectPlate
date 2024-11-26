import os
import shutil
import random
from PIL import Image
import easyocr

# Path awal gambar
source_path = "plat"

# Path target dataset
dataset_path = "dataset"
images_train_path = os.path.join(dataset_path, "images/train")
images_val_path = os.path.join(dataset_path, "images/val")
labels_train_path = os.path.join(dataset_path, "labels/train")
labels_val_path = os.path.join(dataset_path, "labels/val")

# Membuat struktur folder
os.makedirs(images_train_path, exist_ok=True)
os.makedirs(images_val_path, exist_ok=True)
os.makedirs(labels_train_path, exist_ok=True)
os.makedirs(labels_val_path, exist_ok=True)

# Persentase data untuk train dan val
train_ratio = 0.8
val_ratio = 0.2

# Inisialisasi EasyOCR
reader = easyocr.Reader(['en'])  # Menggunakan bahasa Inggris untuk OCR

# Fungsi untuk membuat label dari gambar menggunakan EasyOCR
def create_label_from_image(image_path):
    try:
        # Baca gambar menggunakan EasyOCR
        results = reader.readtext(image_path, detail=1)
        
        # Jika tidak ada teks terdeteksi, lewati
        if not results:
            raise ValueError("Tidak ada teks yang terdeteksi dalam gambar.")
        
        # Ambil bounding box untuk teks yang terdeteksi
        for bbox, text, confidence in results:
            # EasyOCR memberikan koordinat bounding box: [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
            x1, y1 = bbox[0]
            x3, y3 = bbox[2]
            
            # Dapatkan dimensi gambar
            image = Image.open(image_path)
            image_width, image_height = image.size
            
            # Konversi ke format YOLO
            center_x = ((x1 + x3) / 2) / image_width
            center_y = ((y1 + y3) / 2) / image_height
            width = abs(x3 - x1) / image_width
            height = abs(y3 - y1) / image_height
            
            # Hanya buat label untuk teks dengan kepercayaan tinggi (threshold 0.5)
            if confidence > 0.5:
                return f"0 {center_x} {center_y} {width} {height}\n"
        
        raise ValueError("Tidak ada teks dengan confidence tinggi yang terdeteksi.")
    
    except Exception as e:
        print(f"Error memproses gambar {image_path}: {e}")
        return None

# Memproses setiap subfolder dalam source_path
for plate_folder in os.listdir(source_path):
    plate_path = os.path.join(source_path, plate_folder)
    if os.path.isdir(plate_path):
        # Dapatkan semua file gambar di folder plat
        files = [f for f in os.listdir(plate_path) if f.endswith('.png')]
        random.shuffle(files)  # Acak file
        
        # Hitung jumlah data train dan val
        train_count = int(len(files) * train_ratio)
        val_count = len(files) - train_count
        
        # Memproses file untuk train
        for file in files[:train_count]:
            src_image_path = os.path.join(plate_path, file)
            dst_image_path = os.path.join(images_train_path, file)
            shutil.copy(src_image_path, dst_image_path)
            
            # Buat label dari gambar
            label = create_label_from_image(src_image_path)
            if label:  # Jika label berhasil dibuat
                dst_label_path = os.path.join(labels_train_path, file.replace('.png', '.txt'))
                with open(dst_label_path, 'w') as label_file:
                    label_file.write(label)
        
        # Memproses file untuk val
        for file in files[train_count:]:
            src_image_path = os.path.join(plate_path, file)
            dst_image_path = os.path.join(images_val_path, file)
            shutil.copy(src_image_path, dst_image_path)
            
            # Buat label dari gambar
            label = create_label_from_image(src_image_path)
            if label:  # Jika label berhasil dibuat
                dst_label_path = os.path.join(labels_val_path, file.replace('.png', '.txt'))
                with open(dst_label_path, 'w') as label_file:
                    label_file.write(label)

print("Dataset berhasil diproses dan dipisahkan!")
