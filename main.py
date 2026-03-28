from graph.builder import build_graph
from config import PATIENT_ID

def main():
    graph = build_graph()

    result = graph.invoke({
        "patient_id": PATIENT_ID
    })

    print("\n===== FINAL OUTPUT =====")
    print("Report:", result["final_pdf"])

if __name__ == "__main__":
    main()