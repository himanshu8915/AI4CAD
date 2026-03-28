from langchain_ollama import OllamaLLM
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time

# 🔥 Detect device
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"[LLM] Device: {device}")

# ===============================
# GPU → MEDGEMMA
# ===============================
if device == "cuda":

    MODEL_NAME = "google/medgemma-1.5-4b-it"

    print("[LLM] Using MedGemma (GPU)")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    def generate_report(context: str):

        prompt = f"""
You are a cardiology AI assistant.

Findings:
{context}

Provide:
Diagnosis:
Severity:
Reasoning:
Recommendation:
"""

        inputs = tokenizer(prompt, return_tensors="pt").to(device)

        start = time.time()

        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.2,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

        end = time.time()

        generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]
        decoded = tokenizer.decode(generated_tokens, skip_special_tokens=True)

        print(f"[LLM] MedGemma took {end-start:.2f}s")

        return decoded


# ===============================
# CPU → OLLAMA
# ===============================
else:

    print("[LLM] Using Ollama (CPU)")

    llm = OllamaLLM(model="llama3.2:latest")

    def generate_report(context: str):

        prompt = f"""

You are a cardiology AI assistant.

You are analyzing AI-detected angiography frames.

IMPORTANT:
- You ONLY have frame-level detection confidence scores
- You DO NOT have measurements like diameter or calcium score
- DO NOT invent any medical measurements
- DO NOT hallucinate values

Findings:
{context}

Return STRICTLY:

Diagnosis: <blockage present or not>

Severity: <low / moderate / high>

Reasoning: <based only on confidence scores and number of frames>

Recommendation: <next clinical step>

Only use the given data.
"""

        start = time.time()

        response = llm.invoke(prompt)

        end = time.time()

        print(f"[LLM] Ollama took {end-start:.2f}s")

        return response