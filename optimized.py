
import re
import hashlib
import ollama


# ============================================================
# LOCAL RESPONSE CACHE
# ============================================================

cache = {}


# ============================================================
# TOKEN ESTIMATION FALLBACK
# ============================================================

def estimate_tokens(text):
    """
    Approximate token count for local cost analysis.
    Used only when Ollama does not provide token metadata.
    """

    words = len(re.findall(r"\S+", text))

    return max(1, int(words * 1.3))


# ============================================================
# GET ACTUAL TOKEN COUNT
# ============================================================

def get_token_count(response, token_type):
    """
    Get actual token usage from Ollama response.

    input  -> prompt_eval_count
    output -> eval_count
    """

    if token_type == "input":
        value = response.get("prompt_eval_count")
    else:
        value = response.get("eval_count")

    if isinstance(value, int) and value > 0:
        return value

    return None


# ============================================================
# CACHE KEY
# ============================================================

def get_cache_key(question):
    """
    Creates a unique cache key for each question.
    """

    normalized_question = question.strip().lower()

    return hashlib.md5(
        normalized_question.encode("utf-8")
    ).hexdigest()


# ============================================================
# AVAILABLE MODEL CHECK
# ============================================================

def get_available_models():
    """
    Returns models currently installed in Ollama.
    """

    try:

        result = ollama.list()

        models = []

        # New Ollama Python response format
        if hasattr(result, "models"):

            for model in result.models:

                if hasattr(model, "model"):

                    models.append(model.model)

                elif isinstance(model, dict):

                    name = (
                        model.get("model")
                        or model.get("name")
                    )

                    if name:
                        models.append(name)

        # Older dictionary format
        elif isinstance(result, dict):

            for model in result.get("models", []):

                if isinstance(model, dict):

                    name = (
                        model.get("model")
                        or model.get("name")
                    )

                    if name:
                        models.append(name)

        return models

    except Exception:

        return []


# ============================================================
# MODEL ROUTING
# ============================================================

def choose_model(question):
    """
    Selects a smaller model for simple questions
    when available.

    Uses Gemma 3 for more complex questions.
    """

    question_words = len(question.split())

    available_models = get_available_models()

    # Possible smaller models
    smaller_models = [
        "gemma3:1b",
        "gemma3:270m",
        "llama3.2:1b",
        "qwen2.5:0.5b",
        "qwen2.5:1.5b"
    ]

    # Find installed smaller model
    small_model = None

    for candidate in smaller_models:

        if candidate in available_models:

            small_model = candidate
            break

    # Simple question
    if question_words <= 12 and small_model:

        return small_model

    # Complex question
    if "gemma3" in available_models:

        return "gemma3"

    # Fallback to first installed model
    if available_models:

        return available_models[0]

    # Final fallback
    return "gemma3"


# ============================================================
# PROMPT COMPRESSION
# ============================================================

def build_optimized_prompt(question):
    """
    Short optimized prompt.

    Removes unnecessary instructions from
    the baseline implementation.
    """

    prompt = f"""
Answer accurately and concisely.

Question: {question}
"""

    return prompt.strip()


# ============================================================
# OPTIMIZED ANSWER
# ============================================================

def optimized_answer(question):

    # ========================================================
    # VALIDATE QUESTION
    # ========================================================

    if not question or not question.strip():

        return {
            "answer": "Please enter a valid question.",
            "model": "None",
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "cache_hit": False
        }

    question = question.strip()


    # ========================================================
    # 1. CHECK CACHE
    # ========================================================

    cache_key = get_cache_key(question)

    if cache_key in cache:

        cached = cache[cache_key]

        return {
            "answer": cached["answer"],
            "model": cached["model"],
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "cache_hit": True
        }


    # ========================================================
    # 2. MODEL ROUTING
    # ========================================================

    model = choose_model(question)


    # ========================================================
    # 3. PROMPT COMPRESSION
    # ========================================================

    prompt = build_optimized_prompt(question)


    # ========================================================
    # 4. GENERATE RESPONSE
    # ========================================================

    try:

        response = ollama.chat(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    except Exception as error:

        return {
            "answer": (
                "Unable to generate a response.\n\n"
                "Please make sure Ollama is running "
                "and the required model is installed.\n\n"
                f"Error: {error}"
            ),
            "model": model,
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0,
            "cache_hit": False
        }


    # ========================================================
    # 5. GET ANSWER
    # ========================================================

    try:

        answer = response["message"]["content"]

    except Exception:

        answer = (
            "The model returned an unexpected response format."
        )


    # ========================================================
    # 6. GET ACTUAL TOKEN USAGE
    # ========================================================

    actual_input_tokens = get_token_count(
        response,
        "input"
    )

    actual_output_tokens = get_token_count(
        response,
        "output"
    )


    # ========================================================
    # 7. FALLBACK TOKEN COUNT
    # ========================================================

    if actual_input_tokens is None:

        actual_input_tokens = estimate_tokens(prompt)

    if actual_output_tokens is None:

        actual_output_tokens = estimate_tokens(answer)


    # ========================================================
    # 8. TOTAL TOKENS
    # ========================================================

    total_tokens = (
        actual_input_tokens
        + actual_output_tokens
    )


    # ========================================================
    # 9. SAVE TO CACHE
    # ========================================================

    cache[cache_key] = {
        "answer": answer,
        "model": f"{model} - Optimized"
    }


    # ========================================================
    # 10. RETURN RESULTS
    # ========================================================

    return {
        "answer": answer,
        "model": f"{model} - Optimized",
        "input_tokens": actual_input_tokens,
        "output_tokens": actual_output_tokens,
        "total_tokens": total_tokens,
        "cache_hit": False
    }

