import os
import pandas as pd
from ultralytics import YOLO

from config import MODEL_PATH, get_patient_paths
import cv2


# 🔥 INIT MODEL ONCE (module-level)
print("[Detection] Loading YOLO model...")
try:
    model = YOLO(MODEL_PATH)
    print("[Detection] Model loaded")
except Exception as e:
    print(f"[ERROR] Failed to load YOLO model: {e}")
    model = None


def detection_node(state):
    print("\n==============================")
    print("🚀 NODE: DETECTION")
    print("Incoming state keys:", list(state.keys()))
    print("==============================")

    # 🔒 Safe access
    frames_dir = state.get("frames_dir")
    patient_id = state.get("patient_id")

    if not frames_dir:
        print("[ERROR] 'frames_dir' missing in state")
        return {"df": pd.DataFrame(), "high_df": pd.DataFrame()}

    if not os.path.exists(frames_dir):
        print(f"[ERROR] frames_dir does not exist: {frames_dir}")
        return {"df": pd.DataFrame(), "high_df": pd.DataFrame()}

    if model is None:
        print("[ERROR] YOLO model not loaded")
        return {"df": pd.DataFrame(), "high_df": pd.DataFrame()}

    print(f"[Detection] Frames directory: {frames_dir}")

    paths = get_patient_paths(patient_id)

    rows = []

    studies = [
        d for d in os.listdir(frames_dir)
        if os.path.isdir(os.path.join(frames_dir, d))
    ]

    print(f"[Detection] Found studies: {studies}")

    if len(studies) == 0:
        print("[WARNING] No studies found")
        return {"df": pd.DataFrame(), "high_df": pd.DataFrame()}

    for study in studies:
        study_dir = os.path.join(frames_dir, study)

        print(f"[Detection] Processing study: {study}")

        files = sorted(os.listdir(study_dir))[:30]

        if len(files) == 0:
            print(f"[WARNING] No files in study: {study}")
            continue

        for fname in files:
            if not fname.endswith(".png"):
                continue

            path = os.path.join(study_dir, fname)

            try:
                results = model(path, verbose=False)[0]
                # 🔥 SAVE DETECTION IMAGE (WITH BOUNDING BOX)
                study_out_dir = os.path.join(paths["detections"], study)
                os.makedirs(study_out_dir, exist_ok=True)

                annotated_img = results.plot()  # YOLO draws boxes

                save_path = os.path.join(study_out_dir, fname)
                cv2.imwrite(save_path, annotated_img)

            except Exception as e:
                print(f"[ERROR] YOLO failed on {path}: {e}")
                continue

            max_conf = 0.0

            try:
                if results.boxes is not None and len(results.boxes) > 0:
                    max_conf = float(results.boxes.conf.cpu().numpy().max())
            except Exception as e:
                print(f"[WARNING] Failed to extract confidence for {fname}: {e}")

            print(f"[Detection] {fname} → conf: {max_conf:.2f}")

            rows.append([study, fname, max_conf])

    print(f"[Detection] Total frames processed: {len(rows)}")

    df = pd.DataFrame(rows, columns=["study", "frame", "max_conf"])

    if len(df) == 0:
        print("[WARNING] No detection results generated")
        return {"df": df, "high_df": df}

    high_df = df[df.max_conf >= 0.5]

    print(f"[Detection] High confidence frames: {len(high_df)}")

    final_dir = os.path.join(paths["detections"], "final_selection")
    os.makedirs(final_dir, exist_ok=True)

    sorted_df = df.sort_values("max_conf", ascending=False).head(10)

    for _, row in sorted_df.iterrows():
        src = os.path.join(frames_dir, row["study"], row["frame"])
        dst = os.path.join(final_dir, f"{row['study']}_{row['frame']}")

        try:
            img = cv2.imread(src)
            if img is not None:
                cv2.imwrite(dst, img)
        except:
            pass

    print(f"[Detection] Final selected frames saved at: {final_dir}")

    print("✅ NODE COMPLETE: DETECTION")
    print("Output keys:", ["df", "high_df"])
    print("==============================\n")

    return {
        "df": df,
        "high_df": high_df
    }