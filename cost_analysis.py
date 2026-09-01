import pandas as pd


# =========================================================
# LLM MODEL PRICING
# =========================================================
# Prices are USD per 1 million tokens.
# Verify current official pricing before final submission.

MODEL_PRICING = {
    "gpt-4.1-mini": {
        "input": 0.40,
        "output": 1.60
    },
    "gpt-4.1": {
        "input": 2.00,
        "output": 8.00
    }
}


# =========================================================
# CALCULATE SINGLE REQUEST COST
# =========================================================

def calculate_request_cost(
    model,
    input_tokens,
    output_tokens
):
    """
    Calculate the cost of one LLM API request.
    """

    if model not in MODEL_PRICING:
        return 0.0

    input_price = MODEL_PRICING[model]["input"]
    output_price = MODEL_PRICING[model]["output"]

    input_cost = (
        input_tokens / 1_000_000
    ) * input_price

    output_cost = (
        output_tokens / 1_000_000
    ) * output_price

    total_cost = input_cost + output_cost

    return total_cost


# =========================================================
# COST PER 1,000 REQUESTS
# =========================================================

def calculate_cost_per_1000(
    total_cost,
    total_requests
):
    """
    Convert total experiment cost
    into cost per 1,000 requests.
    """

    if total_requests == 0:
        return 0.0

    return (
        total_cost / total_requests
    ) * 1000


# =========================================================
# COST REDUCTION
# =========================================================

def calculate_cost_reduction(
    baseline_cost,
    optimized_cost
):
    """
    Calculate percentage cost reduction.
    """

    if baseline_cost == 0:
        return 0.0

    reduction = (
        (baseline_cost - optimized_cost)
        / baseline_cost
    ) * 100

    return reduction


# =========================================================
# QUALITY DIFFERENCE
# =========================================================

def calculate_quality_difference(
    baseline_quality,
    optimized_quality
):
    """
    Calculate quality change in percentage points.
    """

    return optimized_quality - baseline_quality


# =========================================================
# ANALYZE CSV RESULTS
# =========================================================

def analyze_results(csv_file):
    """
    Analyze an experiment CSV file.

    Expected columns:

    model
    input_tokens
    output_tokens
    cost
    quality_score
    """

    df = pd.read_csv(csv_file)

    total_requests = len(df)

    total_cost = df["cost"].sum()

    cost_per_1000 = calculate_cost_per_1000(
        total_cost,
        total_requests
    )

    average_quality = df[
        "quality_score"
    ].mean()

    return {
        "requests": total_requests,
        "total_cost": total_cost,
        "cost_per_1000": cost_per_1000,
        "average_quality": average_quality
    }


# =========================================================
# COMPARE BASELINE VS OPTIMIZED
# =========================================================

def compare_results(
    baseline,
    optimized
):
    """
    Compare baseline and optimized experiments.
    """

    cost_reduction = calculate_cost_reduction(
        baseline["cost_per_1000"],
        optimized["cost_per_1000"]
    )

    quality_difference = calculate_quality_difference(
        baseline["average_quality"],
        optimized["average_quality"]
    )

    return {
        "baseline_cost_per_1000":
            baseline["cost_per_1000"],

        "optimized_cost_per_1000":
            optimized["cost_per_1000"],

        "cost_reduction_percent":
            cost_reduction,

        "baseline_quality":
            baseline["average_quality"],

        "optimized_quality":
            optimized["average_quality"],

        "quality_difference":
            quality_difference
    }


# =========================================================
# CREATE BEFORE / AFTER TABLE
# =========================================================

def create_comparison_table(
    baseline,
    optimized
):
    """
    Create a simple before/after comparison table.
    """

    table = pd.DataFrame({

        "Metric": [
            "Total Requests",
            "Total Cost ($)",
            "Cost per 1,000 Requests ($)",
            "Average Quality (%)"
        ],

        "Baseline": [
            baseline["requests"],
            round(baseline["total_cost"], 6),
            round(baseline["cost_per_1000"], 4),
            round(baseline["average_quality"], 2)
        ],

        "Optimized": [
            optimized["requests"],
            round(optimized["total_cost"], 6),
            round(optimized["cost_per_1000"], 4),
            round(optimized["average_quality"], 2)
        ]
    })

    return table