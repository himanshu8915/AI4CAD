import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from config import INPUT_DIR, get_patient_paths


def final_report_node(state):
    print("\n==============================")
    print("🚀 NODE: FINAL REPORT")
    print("==============================")

    patient_id = state.get("patient_id")
    report = state.get("report", "No report generated")
    doctor_decision = state.get("doctor_decision", "Not provided")
    feedback = state.get("feedback", "No feedback")

    paths = get_patient_paths(patient_id)

    final_dir = paths["final"]

    os.makedirs(final_dir, exist_ok=True)

    final_pdf = os.path.join(final_dir, "final_report.pdf")

    doc = SimpleDocTemplate(final_pdf)
    styles = getSampleStyleSheet()

    elements = []

    # 🔥 TITLE
    elements.append(Paragraph("AI4CAD Diagnostic Report", styles['Title']))
    elements.append(Spacer(1, 15))

    # 🔥 STRUCTURED SECTIONS (better parsing)
    sections = ["Diagnosis", "Severity", "Reasoning", "Recommendation"]

    for sec in sections:
        if sec.lower() in report.lower():
            elements.append(Paragraph(f"<b>{sec}</b>", styles['Heading2']))
            
            # extract section content roughly
            try:
                part = report.split(sec)[1]
                part = part.split("\n")[0]
            except:
                part = report[:200]

            elements.append(Paragraph(part, styles['BodyText']))
            elements.append(Spacer(1, 10))

    # 🔥 FULL RAW REPORT (backup)
    elements.append(Paragraph("<b>Full AI Report</b>", styles['Heading2']))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(report, styles['BodyText']))
    elements.append(Spacer(1, 15))

    # 🔥 DOCTOR INPUT
    elements.append(Paragraph("<b>Doctor Decision</b>", styles['Heading2']))
    elements.append(Paragraph(doctor_decision, styles['BodyText']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>Doctor Feedback</b>", styles['Heading2']))
    elements.append(Paragraph(feedback, styles['BodyText']))
    elements.append(Spacer(1, 15))

    # 🔥 VISUAL EVIDENCE SECTION
    elements.append(Paragraph("<b>Visual Evidence (Detection + GradCAM)</b>", styles['Heading2']))
    elements.append(Spacer(1, 10))

    merged_dir = state.get("merged_dir", paths["merged"])

    image_paths = []

    if os.path.exists(merged_dir):
        # 🔥 sort for consistency
        files = sorted(os.listdir(merged_dir))

        for f in files[:6]:
            image_paths.append(os.path.join(merged_dir, f))
    else:
        print("[WARNING] Merged directory not found")

    # 🔥 Add images
    for img_path in image_paths[:6]:
        try:
            elements.append(Image(img_path, width=400, height=250))
            elements.append(Spacer(1, 10))
        except Exception as e:
            print(f"[WARNING] Failed to load image: {img_path}")

    # 🔥 BUILD PDF
    doc.build(elements)

    print(f"✅ Final report saved: {final_pdf}")
    print("==============================\n")

    return {"final_pdf": final_pdf}