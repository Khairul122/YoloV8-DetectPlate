from ultralytics import YOLO
import cv2
import easyocr
import torch

# Gunakan GPU jika tersedia
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Fungsi untuk menghitung IoU (Intersection Over Union)
def iou(box1, box2):
    x1, y1, x2, y2 = box1[:4]
    x1_, y1_, x2_, y2_ = box2[:4]

    inter_x1 = max(x1, x1_)
    inter_y1 = max(y1, y1_)
    inter_x2 = min(x2, x2_)
    inter_y2 = min(y2, y2_)

    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x2_ - x1_) * (y2_ - y1_)

    union_area = box1_area + box2_area - inter_area
    return inter_area / union_area if union_area > 0 else 0

# Load model YOLO
model = YOLO('runs/detect/train2/weights/best.pt')

# Inisialisasi EasyOCR
reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())

# Buka kamera (0 adalah kamera default)
cap = cv2.VideoCapture(0)

# Optimasi kamera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set lebar frame
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set tinggi frame
cap.set(cv2.CAP_PROP_FPS, 30)            # Set frame rate

if not cap.isOpened():
    print("Error: Tidak dapat membuka kamera.")
    exit()

while True:
    # Baca frame dari kamera
    ret, frame = cap.read()
    if not ret:
        print("Error: Tidak dapat membaca frame dari kamera.")
        break

    # Deteksi pelat nomor menggunakan YOLO dengan GPU
    results = model.predict(source=frame, imgsz=640, conf=0.5, device=device)
    boxes = []

    # Kumpulkan semua bounding box dan confidence
    for r in results[0].boxes.data:
        x1, y1, x2, y2, conf, cls = r
        if conf > 0.6:  # Abaikan box dengan confidence rendah
            boxes.append((int(x1), int(y1), int(x2), int(y2), float(conf)))

    print(f"Detections before NMS: {len(boxes)}")  # Debug jumlah box sebelum NMS

    # Terapkan Non-Max Suppression (NMS) untuk single bounding box
    selected_boxes = []
    if boxes:
        # Sorting boxes berdasarkan confidence
        boxes = sorted(boxes, key=lambda x: x[4], reverse=True)

        for i, box1 in enumerate(boxes):
            keep = True
            for j, box2 in enumerate(boxes):
                if i != j:
                    iou_val = iou(box1, box2)
                    # Hapus box dengan IoU tinggi
                    if iou_val > 0.4:
                        keep = False
                        break
            if keep:
                selected_boxes.append(box1)

    print(f"Detections after NMS: {len(selected_boxes)}")  # Debug jumlah box setelah NMS

    # Proses hanya bounding box yang telah dipilih
    for x1, y1, x2, y2, conf in selected_boxes:
        # Gambar bounding box dengan warna hijau
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Potong area pelat nomor dari frame
        plate_image = frame[y1:y2, x1:x2]

        # OCR untuk membaca teks dari pelat nomor
        result = reader.readtext(plate_image)
        for detection in result:
            text = detection[1]
            print("Detected Plate:", text)

            # Tambahkan teks hasil OCR ke gambar di atas bounding box
            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Tampilkan frame dalam mode layar penuh
    cv2.namedWindow('License Plate Detection', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('License Plate Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('License Plate Detection', frame)

    # Tekan 'q' untuk keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Lepas kamera dan tutup semua jendela
cap.release()
cv2.destroyAllWindows()
