# 🫀 CAD Pipeline

## 🚀 Overview

This project implements an **end-to-end pipeline for coronary artery analysis** using angiography data.

The system processes **DICOM video inputs**, performs automated analysis, and generates a **structured medical-style report**.

The focus of this repository is on:

* Data flow and system design
* Real-world DICOM handling
* Explainability and evaluation
* Automated reporting

> ⚠️ Note: Model internals are intentionally abstracted.

---

## 🧠 Pipeline Flow

```
DICOM Input
   ↓
Frame Extraction
   ↓
Detection Engine
   ↓
Aggregation / Ensemble
   ↓
Explainability Engine
   ↓
Evaluation Metrics
   ↓
Final Report Generation
```

---

## 📂 Project Structure

```
project/
│
├── input/
│   └── dicom/                  # Place DICOM files here
│
├── output/
│   └── final/
│       └── final_report/       # Generated reports
│
├── src/
│   ├── dicom/                  # DICOM processing
│   ├── detection/              # Detection pipeline
│   ├── explainability/         # CAM methods
│   ├── evaluation/             # Metrics
│   ├── reporting/              # Report generation
│
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 🔹 Step 1: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

---

### 🔹 Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 💻 Runtime Configuration

The pipeline automatically adapts based on your system:

### 🟢 GPU Available

* Uses optimized inference pipeline
* Enables high-performance execution
* Supports advanced model backends

---

### 🟡 CPU Only

Uses local inference via Ollama

#### Install Ollama:

[https://ollama.com](https://ollama.com)

#### Pull a model:

```bash
ollama pull llama3
```

---

## ▶️ Running the Pipeline

Once setup is complete:

```bash
python main.py
```

---

## 📥 Input Data

Place your DICOM files here:

```
input/dicom/
```

---

### 🔁 Using Your Own Data

To use custom data:

* Replace existing DICOM files in the folder
* Ensure files are **multi-frame DICOM videos**

---

## 📤 Output

After execution, results will be available at:

```
output/final/final_report/
```

---

## 📄 Final Report Includes

* Detected regions of interest
* Severity grouping (low / medium / high)
* Visual overlays
* Explainability heatmaps
* Structured interpretation

---

## 🧠 Explainability

The pipeline includes multiple explainability methods:

* Grad-based localization
* Layer-wise attribution
* Score-based attention mapping
* Detection-aware visualization

These are evaluated using:

* Spatial overlap metrics
* Peak localization checks
* Energy distribution analysis

---

## 📊 Evaluation

The system evaluates both:

### Detection Performance

* Precision
* Recall
* F1-score
* mAP

---

### Explainability Quality

* IoU (Intersection over Union)
* Pointing Game Accuracy
* Energy Localization Score

---

## 🔧 Design Philosophy

This repository is built to:

* Simulate real-world medical workflows
* Support modular experimentation
* Enable explainable AI research
* Maintain abstraction over sensitive components

---

## 🚀 Key Highlights

* End-to-end automated pipeline
* DICOM-native processing
* Explainability-focused design
* Hardware-adaptive execution
* Structured output generation

---

## ⚠️ Disclaimer

* This system is intended for **research and development purposes only**
* Not for clinical use without validation

---

## 👨‍💻 Author

Himanshu

---

## ⭐ Support

If you find this useful:

* Star the repository ⭐
* Share with others in medical AI

---
