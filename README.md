# AI4CAD — AI-Powered Coronary Artery Disease Detection & Clinical Decision Support

AI4CAD is an end-to-end agentic AI system designed to assist in the detection and clinical interpretation of coronary artery disease (CAD) using angiography data.

The system integrates **deep learning, explainability, and medical reasoning** into a unified pipeline to support faster and more accessible diagnosis.

---

# Project Structure

```
project/
│
├── data/
│   ├── input/
│   │   └── dicom/                  # Place DICOM files here
│   │
│   └── output/
│       └── patient_x/
│           ├── frames/             # Extracted frames
│           ├── detections/         # YOLO detections (with boxes)
│           ├── gradcam/            # Explainability heatmaps
│           ├── merged/             # Side-by-side detection + GradCAM
│           ├── final/              # Final reports
│
├── models/
│   └── best.pt                    # Trained YOLO model
│
├── graph/
│   ├── builder.py                # LangGraph pipeline
│   ├── state.py                  # State definition
│
├── nodes/
│   ├── preprocess.py             # DICOM → frames
│   ├── detection.py              # YOLO inference
│   ├── gradcam.py                # Explainability
│   ├── merge_node.py             # Merge detection + GradCAM
│   ├── context.py                # Context generation
│   ├── reasoning.py              # LLM reasoning
│   ├── policy.py                 # Routing logic
│   ├── doctor.py                 # Human-in-loop nodes
│   ├── report.py                 # PDF report generation
│
├── llm/
│   └── medgemma.py               # Adaptive LLM (GPU/CPU)
│
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

# Setup Instructions

##  Step 1: Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/Mac
```

---

##  Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

#  Runtime Configuration

The system automatically adapts based on your hardware:

---

##  GPU Available

* Uses **MedGemma (Google medical LLM)**
* High-quality medical reasoning
* Faster inference with CUDA

---

##  CPU Only

Uses **Ollama-based local inference**

---

###  Install Ollama

👉 https://ollama.com

---

###  Pull Model

```bash
ollama pull llama3.2:latest
```

---

###  Start Ollama

```bash
ollama serve
```

---

#  Running the Pipeline

Once setup is complete:

```bash
python main.py
```

---

#  Input Data

Place DICOM files here:

```
data/input/dicom/
```

---

##  Using Your Own Data

To use custom data:

* Replace files in `data/input/dicom/`
* Ensure they are **multi-frame angiography DICOM videos**
* Supported format:

  * IM0.dcm
  * IM1.dcm
  * IM2.dcm

---

#  Pipeline Overview

```
DICOM Input
   ↓
Frame Extraction
   ↓
YOLO Detection
   ↓
GradCAM Explainability
   ↓
Merge (Detection | GradCAM)
   ↓
Context Generation
   ↓
LLM Reasoning (MedGemma / Ollama)
   ↓
Doctor Validation
   ↓
Final Report
```

---

#  Output

After execution:

```
data/output/patient_x/
```

---

##  Key Outputs

---

###  Frames

```
frames/
```

Extracted angiography frames

---

###  Detection

```
detections/
```

Frames with bounding boxes

---

###  GradCAM

```
gradcam/
```

Explainability heatmaps

---

###  Merged Evidence

```
merged/
```

Side-by-side:

```
[ Detection (boxes) ] | [ GradCAM ]
```

---

###  Final Report

```
final/final_report.pdf
```

---

#  Final Report Includes

* AI-based diagnosis
* Severity classification
* Reasoning explanation
* Doctor validation
* Visual evidence (merged frames)

---

#  Explainability

The system integrates explainability through:

* GradCAM heatmaps
* Detection-aware visualization
* Frame-level importance ranking

---

#  AI Components

---

##  Detection Model

* YOLO-based architecture
* Trained on CADICA / Arcade datasets
* Outputs:

  * blockage presence
  * confidence scores

---

##  Explainability

* GradCAM applied to detection backbone
* Highlights model attention regions

---

##  Reasoning Layer

Adaptive LLM:

| Environment | Model             |
| ----------- | -------------     |
| GPU         | MedGemma          | 
| CPU         | Ollama (llama3.2) |

---

##  Human-in-the-Loop

* Junior doctor validation
* Senior escalation logic
* Feedback integration

---

#  Key Highlights

* End-to-end agentic pipeline (LangGraph)
* DICOM-native processing
* Explainable AI for clinical trust
* Adaptive inference (GPU + CPU)
* Multi-view angiography support
* Structured report generation

---

#  Disclaimer

* For **research and development only**
* Not intended for clinical deployment without validation

---

# Author

**Himanshu**

---

# ⭐ Support

If you find this useful:

* Star the repository ⭐
* Share with medical AI community
