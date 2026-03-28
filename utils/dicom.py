import os
import cv2
import numpy as np
import pydicom

def find_dicom_files(folder):
    dicom_files = []

    for root, _, files in os.walk(folder):
        for f in files:
            path = os.path.join(root, f)
            try:
                ds = pydicom.dcmread(path, force=True)
                if hasattr(ds, "PixelData"):
                    dicom_files.append(path)
            except:
                pass

    print(f"✅ Found {len(dicom_files)} DICOM files")
    return dicom_files


def dicom_to_frames(dicom_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    ds = pydicom.dcmread(dicom_path, force=True)
    arr = ds.pixel_array

    if len(arr.shape) == 3:
        arr = np.stack([arr]*3, axis=-1)

    count = arr.shape[0]

    for i in range(count):
        frame = arr[i].astype(np.float32)
        frame = (frame - frame.min()) / (frame.max() - frame.min() + 1e-8)
        frame = (frame * 255).astype(np.uint8)

        cv2.imwrite(os.path.join(out_dir, f"frame_{i:05d}.png"), frame)

    return count