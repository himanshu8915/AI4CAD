from llm.medgemma import generate_report
import time


def reasoning_node(state):
    print("\n==============================")
    print("🚀 NODE: REASONING (MedGemma)")
    print("Incoming state keys:", list(state.keys()))
    print("==============================")

    # 🔒 Safe access
    context = state.get("context")

    if not context:
        print("[WARNING] No context found — skipping LLM")
        return {"report": "No context available for reasoning"}

    print("\n[Reasoning] Context preview:")
    print(context[:300])  # avoid dumping too much

    print("\n[LLM] Generating report...")

    start_time = time.time()

    try:
        report = generate_report(context)
    except Exception as e:
        print(f"[ERROR] LLM failed: {e}")
        return {"report": "LLM generation failed"}

    end_time = time.time()

    print(f"[LLM] Generation completed in {end_time - start_time:.2f} seconds")

    print("\n[Reasoning] Report preview:")
    print(report[:500])  # partial print

    output = {"report": report}

    print("✅ NODE COMPLETE: REASONING")
    print("Output keys:", list(output.keys()))
    print("==============================\n")

    return output