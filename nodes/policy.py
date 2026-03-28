def policy_node(state):
    max_conf = state["high_df"]["max_conf"].max() if len(state["high_df"]) else 0

    if max_conf >= 0.5:
        return {"decision": "SENIOR"}
    return {"decision": "JUNIOR"}