import re


def estimate_tokens(text):
    """
    Approximate token count for local cost analysis.
    This is an estimation, not an actual tokenizer.
    """
    words = len(re.findall(r"\S+", text))
    return max(1, int(words * 1.3))


def generate_local_response(question):
    """
    Local demonstration response.

    This replaces the Ollama dependency so the application
    can run on Streamlit Cloud without requiring a local
    Ollama server.
    """

    question_lower = question.lower()

    if any(word in question_lower for word in [
        "refund",
        "return",
        "money back"
    ]):
        answer = (
            "For a refund request, please provide your order "
            "details and explain the reason for the refund. "
            "The request can then be reviewed according to "
            "the applicable refund policy."
        )

    elif any(word in question_lower for word in [
        "payment",
        "pay",
        "card",
        "billing"
    ]):
        answer = (
            "For payment-related questions, please verify that "
            "your payment information is correct and that your "
            "payment method is active. If the issue continues, "
            "check the transaction details or contact customer "
            "support for further assistance."
        )

    elif any(word in question_lower for word in [
        "shipping",
        "delivery",
        "order"
    ]):
        answer = (
            "For shipping or order-related questions, please "
            "check your order status and tracking information. "
            "Delivery times may vary depending on the selected "
            "shipping method and destination."
        )

    elif any(word in question_lower for word in [
        "hello",
        "hi",
        "hey"
    ]):
        answer = (
            "Hello! I am your customer support assistant. "
            "Please ask me about orders, payments, refunds, "
            "shipping, or other customer support topics."
        )

    else:
        answer = (
            f"Thank you for your question: \"{question}\". "
            "For this demonstration, the system analyzes the "
            "request locally and provides a simulated customer "
            "support response. In a production environment, "
            "this component could be connected to an LLM API."
        )

    return answer


def baseline_answer(question):
    """
    Baseline implementation.

    Uses a deliberately longer prompt to represent the
    original, less-optimized implementation.

    No external API or Ollama server is required.
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

    answer = generate_local_response(question)

    output_tokens = estimate_tokens(answer)

    return {
        "answer": answer,
        "model": "Local Demo - Baseline",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "cache_hit": False
    }
