import os
import yaml

# Path dataset
dataset_path = os.path.abspath("dataset")  # Ganti "dataset" sesuai lokasi dataset Anda
images_train_path = os.path.join(dataset_path, "images/train")
images_val_path = os.path.join(dataset_path, "images/val")
labels_train_path = os.path.join(dataset_path, "labels/train")
labels_val_path = os.path.join(dataset_path, "labels/val")

# Pastikan direktori ada
if not os.path.exists(images_train_path):
    raise FileNotFoundError(f"Train images path not found: {images_train_path}")
if not os.path.exists(images_val_path):
    raise FileNotFoundError(f"Validation images path not found: {images_val_path}")

# Nama kelas
class_names = ["plate_number"]

# Membuat data.yaml
data_yaml = {
    'train': images_train_path.replace("\\", "/"),
    'val': images_val_path.replace("\\", "/"),
    'nc': len(class_names),
    'names': class_names
}

# Menyimpan file data.yaml
data_yaml_path = os.path.join(dataset_path, "data.yaml")
with open(data_yaml_path, 'w') as yaml_file:
    yaml.dump(data_yaml, yaml_file, default_flow_style=False)

print(f"File data.yaml telah dibuat di {data_yaml_path}")
