import os

BASE_DIR = os.getcwd()

DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_DIR = os.path.join(DATA_DIR, "input")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")

MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt")

PATIENT_ID = "patient_002"


def get_patient_paths(patient_id):
    base = os.path.join(OUTPUT_DIR, patient_id)

    return {
        "base": base,  # 🔥 ADD THIS (important)

        "frames": os.path.join(base, "frames"),
        "detections": os.path.join(base, "detections"),
        "gradcam": os.path.join(base, "gradcam"),
        "merged": os.path.join(base, "merged"),
        "final": os.path.join(base, "final")
    }