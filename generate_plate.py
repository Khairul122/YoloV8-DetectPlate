import os
from PIL import Image, ImageDraw, ImageFont
import random

# Daftar plat nomor
plate_numbers = [
    'BA 1010 AC',
    'BK 6527 JU',
    'BL 2020 FE',
    'BK 7276 RS',
    'BA 3201 YT'
]

# Warna background
background_colors = ['white', 'red', 'green', 'blue']

def create_plate_image(text, bg_color, count, folder_path):
    # Ukuran gambar
    width = 400
    height = 150
    
    # Membuat gambar baru
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    try:
        # Menggunakan font Arial
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        # Fallback ke default font jika Arial tidak tersedia
        font = ImageFont.load_default()
    
    # Mendapatkan ukuran text untuk penempatan tengah
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Menghitung posisi text agar berada di tengah
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Menggambar text
    draw.text((x, y), text, fill='black', font=font)
    
    return image

def main():
    # Membuat folder utama 'plat' jika belum ada
    if not os.path.exists('plat'):
        os.makedirs('plat')
    
    # Untuk setiap plat nomor
    for plate in plate_numbers:
        # Membuat subfolder untuk setiap plat
        subfolder = os.path.join('plat', plate.replace(' ', '_'))
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)
        
        # Generate 50 gambar untuk setiap plat
        for i in range(50):
            # Pilih warna background secara acak
            bg_color = random.choice(background_colors)
            
            # Buat gambar
            img = create_plate_image(plate, bg_color, i+1, subfolder)
            
            # Simpan gambar
            filename = f"{plate.replace(' ', '_')}_{bg_color}_{i+1}.png"
            img.save(os.path.join(subfolder, filename))

if __name__ == "__main__":
    main()
    print("Pembuatan gambar selesai!")