import os
from config import INPUT_DIR, get_patient_paths
from utils.dicom import find_dicom_files, dicom_to_frames


def preprocess_node(state):
    print("\n📂 PREPROCESS NODE STARTED")

    patient_id = state["patient_id"]

    input_dir = os.path.join(INPUT_DIR, patient_id)
    print(f"[Preprocess] Input dir: {input_dir}")

    paths = get_patient_paths(patient_id)

    dicom_list = find_dicom_files(input_dir)
    print(f"[Preprocess] Found {len(dicom_list)} DICOM files")

    total = 0

    for dcm in dicom_list:
        print(f"[Preprocess] Processing: {dcm}")

        name = os.path.basename(dcm)
        out = os.path.join(paths["frames"], name)

        total += dicom_to_frames(dcm, out)

    print(f"[Preprocess] Total frames generated: {total}")
    print("✅ PREPROCESS NODE COMPLETED\n")

    return {
        "dicom_list": dicom_list,
        "frames_dir": paths["frames"]
    }