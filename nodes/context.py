def context_node(state):
    print("\n==============================")
    print("🚀 NODE: CONTEXT")
    print("Incoming state keys:", list(state.keys()))
    print("==============================")

    # 🔒 Safe access
    df = state.get("high_df")

    # 🛑 Handle missing or empty dataframe
    if df is None:
        print("[ERROR] 'high_df' not found in state")
        return {"context": "No detection data available"}

    if len(df) == 0:
        print("[WARNING] 'high_df' is empty")
        return {"context": "No high-confidence detections found"}

    print(f"[Context] Total rows in high_df: {len(df)}")

    # 🧠 Build context string
    context = ""

    # 🔥 SORT BY CONFIDENCE (optional but good)
    df_sorted = df.sort_values("max_conf", ascending=False)

    for i, (_, row) in enumerate(df_sorted.head(5).iterrows()):
        study = row.get("study", "IM?")
        frame = row.get("frame", "unknown")
        conf = row.get("max_conf", 0)

        # 🔥 KEY CHANGE → include study (IM0, IM1, etc.)
        line = f"{study}/{frame} -> {conf:.2f}"

        print(f"[Context] Row {i}: {line}")

        context += line + "\n"

    print("\n[Context] Final generated context:")
    print(context)

    output = {"context": context}

    print("✅ NODE COMPLETE: CONTEXT")
    print("Output keys:", list(output.keys()))
    print("==============================\n")

    return output