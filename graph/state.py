from typing import TypedDict, Optional
import pandas as pd

class State(TypedDict, total=False):
    patient_id: str

    # ADD THESE ↓↓↓
    dicom_list: list
    frames_dir: str

    df: pd.DataFrame
    high_df: pd.DataFrame

    context: str
    report: str

    decision: str
    doctor_decision: str
    feedback: str

    final_pdf: str