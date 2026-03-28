import os
import cv2
import numpy as np
import torch
from ultralytics import YOLO
from config import MODEL_PATH, get_patient_paths

# 🔥 Load model once
print("[GradCAM] Loading YOLO model...")
model = YOLO(MODEL_PATH)
net = model.model
print("[GradCAM] Model loaded")

device = "cuda" if torch.cuda.is_available() else "cpu"
net.to(device)

GRAD_LAYER = 8


def generate_gradcam(frame_path):
    print(f"[GradCAM] Processing: {frame_path}")

    img = cv2.imread(frame_path)
    if img is None:
        print(f"[ERROR] Image not found: {frame_path}")
        return None

    img_resized = cv2.resize(img, (640, 640))
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

    x = torch.from_numpy(img_rgb).float() / 255
    x = x.permute(2, 0, 1).unsqueeze(0).to(device)
    x.requires_grad_(True)

    activations = []
    gradients = []

    def f_hook(m, i, o):
        activations.append(o.clone())

    def b_hook(m, gi, go):
        gradients.append(go[0].clone())

    layer = net.model[GRAD_LAYER]
    fh = layer.register_forward_hook(f_hook)
    bh = layer.register_full_backward_hook(b_hook)

    print("[GradCAM] Running forward pass")

    try:
        with torch.enable_grad():
            out = net(x.clone())
    except Exception as e:
        print(f"[ERROR] Forward pass failed: {e}")
        fh.remove()
        bh.remove()
        return None

    print("[GradCAM] Output received")

    # ✅ Safe scalar score
    score = out[0].sum()

    net.zero_grad()
    score.backward()

    if len(activations) == 0 or len(gradients) == 0:
        print("[ERROR] No activations/gradients captured")
        fh.remove()
        bh.remove()
        return None

    acts = activations[-1]
    grads = gradients[-1]

    weights = grads.mean(dim=(2, 3), keepdim=True)
    cam = (weights * acts).sum(dim=1)

    cam = torch.relu(cam)
    cam -= cam.min()
    cam /= cam.max() + 1e-8

    # ✅ FIXED HERE
    cam = cam.squeeze().detach().cpu().numpy()

    cam = cv2.resize(cam, (img.shape[1], img.shape[0]))

    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)

    fh.remove()
    bh.remove()

    print("[GradCAM] Completed")

    return overlay


def gradcam_node(state):
    print("\n==============================")
    print("🔥 NODE: GRADCAM")
    print("Incoming state keys:", list(state.keys()))
    print("==============================")

    patient_id = state.get("patient_id")
    paths = get_patient_paths(patient_id)

    high_df = state.get("high_df")

    if high_df is None or len(high_df) == 0:
        print("[WARNING] No high confidence detections")
        return state

    print(f"[GradCAM] Processing {len(high_df)} frames")

    os.makedirs(paths["gradcam"], exist_ok=True)

    for _, row in high_df.head(10).iterrows():
        frame_path = os.path.join(paths["frames"], row["study"], row["frame"])

        cam = generate_gradcam(frame_path)

        if cam is None:
            continue

        save_name = f"{row['study']}_{row['frame']}"
        save_path = os.path.join(paths["gradcam"], save_name)
        cv2.imwrite(save_path, cam)

        print(f"[GradCAM] Saved: {save_path}")

    print("✅ NODE COMPLETE: GRADCAM")
    print("==============================\n")

    return state