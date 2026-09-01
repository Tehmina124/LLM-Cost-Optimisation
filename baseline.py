import re
import ollama


def estimate_tokens(text):
    """Approximate token count for local cost analysis."""
    words = len(re.findall(r"\S+", text))
    return max(1, int(words * 1.3))


def baseline_answer(question):
    """
    Baseline Generative AI implementation.

    Uses Gemma 3 with a longer prompt.
    This represents the original, less-optimized version.
    """

    prompt = f"""
You are a highly intelligent and professional customer support
assistant.

Your job is to answer the customer's question accurately,
clearly, professionally, and in a helpful manner.

Read the customer's question carefully and consider all
possible interpretations before answering.

Provide enough explanation so that the customer fully
understands the answer.

Do not make up information.

If the answer is not known, clearly state that you do not know.

Customer Question:
{question}

Please provide a detailed and helpful response.
"""

    input_tokens = estimate_tokens(prompt)

    response = ollama.chat(
        model="gemma3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    output_tokens = estimate_tokens(answer)

    return {
        "answer": answer,
        "model": "Gemma 3 - Baseline",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cache_hit": False
    }