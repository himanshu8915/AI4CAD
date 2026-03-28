def senior_doctor_node(state):
    print("\n👨‍⚕️ Senior Doctor Review")
    return {
        "doctor_decision": input("Confirm blockage? "),
        "feedback": input("Notes: ")
    }


def junior_doctor_node(state):
    print("\n🧑‍⚕️ Junior Doctor Review")
    return {
        "doctor_decision": input("Abnormality? "),
        "feedback": input("Notes: ")
    }