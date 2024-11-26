from ultralytics import YOLO
import cv2
import easyocr

# Load model YOLO
model = YOLO('runs/detect/train2/weights/best.pt')

# Inisialisasi EasyOCR
reader = easyocr.Reader(['en'])

# Baca gambar
image = cv2.imread('BA_1010_AC_blue_3.png')

# Deteksi pelat nomor menggunakan YOLO
results = model.predict(source=image, imgsz=640, conf=0.5)

# Iterasi setiap hasil deteksi
for r in results[0].boxes.data:
    x1, y1, x2, y2, conf, cls = r
    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])

    # Gambar bounding box dengan warna hijau
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Potong area pelat nomor dari gambar
    plate_image = image[y1:y2, x1:x2]

    # OCR untuk membaca teks dari pelat nomor
    result = reader.readtext(plate_image)
    for detection in result:
        text = detection[1]
        print("Detected Plate:", text)

        # Tambahkan teks hasil OCR ke gambar di atas bounding box
        cv2.putText(image, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Tampilkan gambar hasil deteksi
cv2.imshow('Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
