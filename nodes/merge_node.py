import os
import cv2
from config import get_patient_paths


def merge_node(state):
    print("\n==============================")
    print("🚀 NODE: MERGE (STRICT MATCH)")
    print("==============================")

    patient_id = state.get("patient_id")
    high_df = state.get("high_df")

    if high_df is None or len(high_df) == 0:
        print("[WARNING] No high confidence frames to merge")
        return state

    paths = get_patient_paths(patient_id)

    detection_dir = paths["detections"]
    gradcam_dir = paths["gradcam"]
    merged_dir = paths["merged"]

    os.makedirs(merged_dir, exist_ok=True)

    print(f"[Merge] Saving outputs → {merged_dir}")

    # 🔥 sort best frames first
    high_df_sorted = high_df.sort_values("max_conf", ascending=False)

    success_count = 0
    skipped_count = 0

    for _, row in high_df_sorted.iterrows():

        study = row["study"]          # e.g. v3.dcm
        frame = row["frame"]          # e.g. frame_00017.png

        # ==============================
        # EXACT PATHS (NO MODIFICATION)
        # ==============================
        det_path = os.path.join(detection_dir, study, frame)
        grad_path = os.path.join(gradcam_dir, f"{study}_{frame}")

        # ==============================
        # STRICT VALIDATION
        # ==============================
        if not os.path.exists(det_path):
            print(f"[ERROR] Detection missing → {study}/{frame}")
            skipped_count += 1
            continue

        if not os.path.exists(grad_path):
            print(f"[ERROR] GradCAM missing for SAME frame → {study}_{frame}")
            skipped_count += 1
            continue

        # ==============================
        # LOAD IMAGES
        # ==============================
        det_img = cv2.imread(det_path)
        grad_img = cv2.imread(grad_path)

        if det_img is None or grad_img is None:
            print(f"[ERROR] Failed loading images → {study}_{frame}")
            skipped_count += 1
            continue

        # ==============================
        # RESIZE GRADCAM
        # ==============================
        h = det_img.shape[0]

        grad_img = cv2.resize(
            grad_img,
            (int(grad_img.shape[1] * h / grad_img.shape[0]), h)
        )

        # ==============================
        # MERGE SIDE-BY-SIDE
        # ==============================
        merged = cv2.hconcat([det_img, grad_img])

        save_path = os.path.join(merged_dir, f"{study}_{frame}")
        cv2.imwrite(save_path, merged)

        print(f"[OK] Merged → {study}_{frame}")
        success_count += 1

    print("\n📊 MERGE SUMMARY")
    print(f"✔ Success: {success_count}")
    print(f"❌ Skipped: {skipped_count}")

    print("\n✅ NODE COMPLETE: MERGE")
    print("==============================\n")

    return {"merged_dir": merged_dir}