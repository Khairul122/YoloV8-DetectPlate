from ultralytics import YOLO

# Path ke file YAML dan model pre-trained
data_yaml_path = "dataset/data.yaml"
model_pretrained = "yolov8n.pt"  # Gunakan yolov8n.pt untuk model YOLO versi terbaru

# Konfigurasi pelatihan
epochs = 50
imgsz = 640

# Membuat dan melatih model
model = YOLO(model_pretrained)  # Memuat model YOLO pre-trained
model.train(data=data_yaml_path, epochs=epochs, imgsz=imgsz)

print("Pelatihan model selesai!")
