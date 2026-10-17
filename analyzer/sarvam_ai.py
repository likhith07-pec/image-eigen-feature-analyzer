import json
import os
import re
import urllib.request
import urllib.error
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

SARVAM_ENDPOINT = "https://api.sarvam.ai/v1/chat/completions"
DEFAULT_MODEL = os.environ.get("SARVAM_MODEL", "sarvam-105b-conversations") or "sarvam-105b-conversations"


def get_sarvam_api_key() -> str:
    key = os.environ.get("SARVAM_API_KEY")
    if key and key.strip():
        return key.strip()

    # Fallback to reading from .env if present
    base_dir = Path(__file__).resolve().parent.parent
    env_file = base_dir / ".env"
    if env_file.exists():
        try:
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if line.startswith("SARVAM_API_KEY="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val and "replace_with" not in val:
                        return val
        except Exception:
            pass

    return ""


def clean_sarvam_response(raw_text: str) -> str:
    """Removes thinking tags <think>...</think> and markdown code fences."""
    text = raw_text.strip()
    # Remove <think>...</think> reasoning blocks if present
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    # Remove markdown ```json ... ``` or ``` ... ```
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return text


def generate_mathematical_insight(result: dict) -> dict:
    """
    Calls Sarvam AI (sarvam-105b) with the computed matrix and eigenspace metrics
    to generate an executive mathematical interpretation and viva defense Q&A.
    """
    api_key = get_sarvam_api_key()
    if not api_key:
        return {
            "available": False,
            "reason": "SARVAM_API_KEY is not configured in the server environment.",
            "model": DEFAULT_MODEL,
        }

    k = result.get("selected_k", 8)
    rank = result.get("rank", 64)
    cols = result.get("matrix_cols", 64)
    rows = result.get("matrix_rows", 64)
    frob_err = result.get("frobenius_error", 0.0)
    rel_err = result.get("relative_error_percent", 0.0)
    ortho = result.get("orthogonality_status", "Verified")
    top_evals = result.get("eigenvalues", [])[:4]
    formatted_evals = ", ".join([f"{ev:.4f}" for ev in top_evals]) if top_evals else "N/A"

    prompt = f"""You are an expert Linear Algebra and Numerical Analysis professor conducting an engineering viva examination.
An image was converted into a normalized {rows}x{cols} grayscale matrix A in [0, 1].
Here are the exact computed numerical metrics:
- Matrix Dimensions: {rows} x {cols}
- Matrix Rank rho(A): {rank} out of {cols}
- Dominant Eigenspace Dimension (k): {k}
- Orthogonality (V_k^T V_k = I): {ortho}
- Top 4 Covariance Eigenvalues (A^T A): [{formatted_evals}]
- Reconstruction Frobenius Error ||A - A_k||_F: {frob_err:.4f}
- Relative Reconstruction Error: {rel_err:.2f}%

Please provide:
1. An executive mathematical interpretation (2-3 sentences) analyzing the quality of the rank-k subspace approximation and how much energy the top-{k} eigenvectors retain according to the Eckart-Young theorem.
2. Two high-yield Viva Defense Questions with rigorous, concise sample answers tailored to these specific metrics (matrix rank {rank}, k={k}, and {rel_err:.2f}% error).

Respond in pure valid JSON without commentary or code fences, with keys:
- "interpretation": string (2-3 sentences)
- "energy_assessment": string (1 concise sentence on whether k={k} is under-approximating, optimal, or near-lossless)
- "viva_qa": list of 2 objects each with "question" (string) and "answer" (string)
"""

    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a linear algebra professor providing concise, rigorous numerical analysis in JSON format."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 800
    }

    try:
        req = urllib.request.Request(
            SARVAM_ENDPOINT,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "api-subscription-key": api_key,
                "Content-Type": "application/json",
                "User-Agent": "EigenLab-Analyzer/2.0"
            }
        )

        with urllib.request.urlopen(req, timeout=14) as response:
            if response.status == 200:
                raw_body = response.read().decode("utf-8")
                res_data = json.loads(raw_body)
                choices = res_data.get("choices", [])
                if not choices:
                    return {"available": False, "reason": "No choices returned by Sarvam AI", "model": DEFAULT_MODEL}
                msg = choices[0].get("message", {})
                raw_content = (msg.get("content") or msg.get("reasoning_content") or "").strip()
                cleaned_content = clean_sarvam_response(raw_content)

                try:
                    parsed = json.loads(cleaned_content)
                    return {
                        "available": True,
                        "model": DEFAULT_MODEL,
                        "interpretation": parsed.get("interpretation", ""),
                        "energy_assessment": parsed.get("energy_assessment", ""),
                        "viva_qa": parsed.get("viva_qa", [])
                    }
                except json.JSONDecodeError:
                    return {
                        "available": True,
                        "model": DEFAULT_MODEL,
                        "interpretation": cleaned_content,
                        "energy_assessment": f"Subspace dimension k={k} captures dominant energy from rank-{rank} matrix.",
                        "viva_qa": [
                            {
                                "question": f"Why is the reconstruction error {rel_err:.2f}% at k={k}?",
                                "answer": f"By the Eckart-Young theorem, the rank-{k} approximation discards the trailing {rank - k} singular values, bounding the residual Frobenius error."
                            }
                        ]
                    }

    except Exception as exc:
        logger.warning("Sarvam AI call failed: %s", exc)
        return {
            "available": False,
            "reason": f"Sarvam AI service notice: {str(exc)}",
            "model": DEFAULT_MODEL,
        }


INDIC_LANGUAGES = {
    "English": "English",
    "Hindi": "Hindi (हिन्दी)",
    "Kannada": "Kannada (ಕನ್ನಡ)",
    "Tamil": "Tamil (தமிழ்)",
    "Telugu": "Telugu (తెలుగు)",
    "Marathi": "Marathi (मराठी)",
    "Bengali": "Bengali (বাংলা)",
    "Gujarati": "Gujarati (ગુજરાતી)",
    "Malayalam": "Malayalam (മലയാളം)",
    "Punjabi": "Punjabi (ਪੰਜਾਬੀ)",
}


def ask_sarvam_question(question: str, language: str = "English", matrix_context: dict = None, history: list = None) -> dict:
    """
    Answers a student's custom question regarding their analyzed image
    in the requested Indian language, retaining English mathematical terms in parentheses.
    Supports multi-turn conversation history.
    """
    api_key = get_sarvam_api_key()
    if not api_key:
        return {
            "success": False,
            "error": "SARVAM_API_KEY is not configured.",
        }

    ctx = matrix_context or {}
    rows = ctx.get("matrix_rows", 64)
    cols = ctx.get("matrix_cols", 64)
    rank = ctx.get("rank", 34)
    k = ctx.get("selected_k", 16)
    frob = ctx.get("frobenius_error", 0.0184)
    rel_err = ctx.get("relative_error_percent", 0.03)

    target_lang_label = INDIC_LANGUAGES.get(language, language)

    prompt = f"""You are Sarvam AI, an expert Linear Algebra and Image Analysis professor specialized in Indian regional languages.
The student has analyzed an image with these exact numerical parameters:
- Matrix Size: {rows} x {cols}
- Matrix Rank rho(A): {rank} out of {cols}
- Retained Subspace: k = {k} dominant eigenvectors
- Frobenius Reconstruction Error ||A - A_k||_F: {frob:.4f}
- Relative Reconstruction Error: {rel_err:.2f}%

Student's Question: "{question}"
Target Response Language: {target_lang_label}

Instructions:
1. Provide a rigorous yet clear explanation answering the student's question based on their matrix data.
2. Formulate your response in the requested language ({target_lang_label}).
3. If writing in an Indian language (like Hindi, Kannada, Tamil, Telugu, Marathi, etc.), write in that native script, but include standard English mathematical terms in parentheses (e.g., 'रैखिक रूप से स्वतंत्र (linearly independent)', 'ಮ್ಯಾಟ್ರಿಕ್ಸ್ ರ್ಯಾಂಕ್ (matrix rank)', 'Eckart-Young theorem') so the student can use it directly in their college viva examination.
4. Keep the explanation concise and structured with bullet points.
"""

    messages = [
        {
            "role": "system",
            "content": f"You are a helpful linear algebra professor fluent in {target_lang_label} and Indian regional languages."
        }
    ]

    # Incorporate prior conversation history (up to last 6 turns)
    if history and isinstance(history, list):
        for item in history[-6:]:
            if isinstance(item, dict) and "role" in item and "content" in item:
                r = "user" if item["role"] == "user" else "assistant"
                c = str(item["content"]).strip()
                if c:
                    messages.append({"role": r, "content": c})

    messages.append({
        "role": "user",
        "content": prompt
    })

    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "temperature": 0.25,
        "max_tokens": 700
    }

    try:
        req = urllib.request.Request(
            SARVAM_ENDPOINT,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "api-subscription-key": api_key,
                "Content-Type": "application/json",
                "User-Agent": "EigenLab-Analyzer/2.0"
            }
        )
        with urllib.request.urlopen(req, timeout=14) as response:
            if response.status == 200:
                raw_body = response.read().decode("utf-8")
                res_data = json.loads(raw_body)
                choices = res_data.get("choices", [])
                if choices:
                    msg = choices[0].get("message", {})
                    answer = (msg.get("content") or msg.get("reasoning_content") or "").strip()
                    cleaned_answer = clean_sarvam_response(answer)
                    return {
                        "success": True,
                        "answer": cleaned_answer,
                        "language": language,
                        "model": DEFAULT_MODEL
                    }
        return {"success": False, "error": "Empty response from Sarvam AI"}
    except Exception as exc:
        logger.warning("ask_sarvam_question failed: %s", exc)
        return {"success": False, "error": str(exc)}


def translate_sarvam_text(text: str, target_language: str = "Hindi") -> dict:
    """
    Translates mathematical synthesis text into an Indian language
    using Sarvam AI.
    """
    api_key = get_sarvam_api_key()
    if not api_key:
        return {"success": False, "error": "SARVAM_API_KEY is not configured."}

    target_lang_label = INDIC_LANGUAGES.get(target_language, target_language)

    prompt = f"""Translate the following mathematical linear algebra explanation into {target_lang_label}.
Preserve mathematical formulas, numbers, and symbols exactly as they are (e.g. A, V_k, lambda_i, ||A - A_k||_F, rho(A)).
Include English technical terms in parentheses where helpful for an engineering college student.

Text to translate:
{text}
"""

    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {
                "role": "system",
                "content": f"You are a professional mathematical translator specialized in {target_lang_label}."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1,
        "max_tokens": 600
    }

    try:
        req = urllib.request.Request(
            SARVAM_ENDPOINT,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "api-subscription-key": api_key,
                "Content-Type": "application/json",
                "User-Agent": "EigenLab-Analyzer/2.0"
            }
        )
        with urllib.request.urlopen(req, timeout=14) as response:
            if response.status == 200:
                raw_body = response.read().decode("utf-8")
                res_data = json.loads(raw_body)
                choices = res_data.get("choices", [])
                if choices:
                    msg = choices[0].get("message", {})
                    answer = (msg.get("content") or msg.get("reasoning_content") or "").strip()
                    cleaned_answer = clean_sarvam_response(answer)
                    return {
                        "success": True,
                        "translated_text": cleaned_answer,
                        "language": target_language
                    }
        return {"success": False, "error": "Empty response from Sarvam AI"}
    except Exception as exc:
        logger.warning("translate_sarvam_text failed: %s", exc)
        return {"success": False, "error": str(exc)}

