
import streamlit as st
import pandas as pd

from baseline import baseline_answer
from optimized import optimized_answer


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LLM Cost Optimisation Study",
    page_icon="💰",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_quality_score(answer):
    """Local rule-based quality score."""

    score = 50

    words = len(answer.split())

    if 10 <= words <= 80:
        score += 20

    if "." in answer:
        score += 10

    useful_words = [
        "accurate",
        "information",
        "policy",
        "answer",
        "check",
        "depends",
        "customer",
        "support",
        "return",
        "refund"
    ]

    if any(word in answer.lower() for word in useful_words):
        score += 10

    if len(answer.strip()) > 20:
        score += 10

    return min(score, 100)


def calculate_efficiency(quality, tokens):
    """Calculate quality/token efficiency."""

    if tokens <= 0:
        return 0

    efficiency = (quality / tokens) * 100

    return round(min(efficiency, 100), 2)


def calculate_cost(input_tokens, output_tokens):
    """
    Benchmark cost.

    Input  = $0.40 / 1M tokens
    Output = $1.60 / 1M tokens
    """

    input_price_per_million = 0.40
    output_price_per_million = 1.60

    input_cost = (
        input_tokens
        * input_price_per_million
        / 1_000_000
    )

    output_cost = (
        output_tokens
        * output_price_per_million
        / 1_000_000
    )

    return input_cost + output_cost


def calculate_percentage_reduction(old_value, new_value):
    """Calculate percentage reduction."""

    if old_value <= 0:
        return 0

    return ((old_value - new_value) / old_value) * 100


def calculate_quality_tradeoff(
    baseline_quality,
    optimized_quality
):
    """Calculate quality change."""

    return optimized_quality - baseline_quality


# ============================================================
# HEADER
# ============================================================

st.title("💰 LLM Cost Optimisation Study")

st.markdown(
    """
### Cut the cost of an LLM feature without materially hurting quality

This dashboard compares a **baseline implementation**
with an **optimized implementation**.

The optimization pipeline demonstrates:

- ✂️ Prompt Compression
- 🤖 Model Routing
- ⚡ Response Caching
- 📉 Token Reduction
- 🎯 Quality Measurement
- 📊 Measured Cost per 1,000 Requests
- 📅 Monthly Cost Projection
- 🏆 Final Trade-off Recommendation
- 📈 Optimization History

**🆓 Free Local Demonstration**

This project does not require a paid API.

Responses are generated locally, while cost is measured
from the actual token usage recorded during each experiment
using a documented benchmark token price.
"""
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Settings")

question = st.sidebar.text_area(
    "Enter your question:",
    "What is your refund policy?"
)

st.sidebar.markdown("---")

st.sidebar.subheader("📊 Cost Projection")

requests_per_month = st.sidebar.number_input(
    "Monthly Requests",
    min_value=100,
    max_value=10_000_000,
    value=10_000,
    step=100
)

st.sidebar.markdown("---")

run_button = st.sidebar.button(
    "🚀 Run Comparison",
    use_container_width=True
)

clear_button = st.sidebar.button(
    "🧹 Clear History",
    use_container_width=True
)


# ============================================================
# CLEAR HISTORY
# ============================================================

if clear_button:

    st.session_state.history = []
    st.session_state.last_result = None

    st.success(
        "🧹 Optimization history cleared."
    )


# ============================================================
# RUN COMPARISON
# ============================================================

if run_button:

    if not question.strip():

        st.warning(
            "⚠️ Please enter a question."
        )

    else:

        # ====================================================
        # BASELINE
        # ====================================================

        with st.spinner(
            "🔴 Running baseline implementation..."
        ):

            baseline = baseline_answer(
                question
            )

        # ====================================================
        # OPTIMIZED
        # ====================================================

        with st.spinner(
            "🟢 Running optimized implementation..."
        ):

            optimized = optimized_answer(
                question
            )

        # ====================================================
        # CACHE STATUS
        # ====================================================

        cache_hit = optimized.get(
            "cache_hit",
            False
        )

        if cache_hit:

            st.info(
                "⚡ Cache HIT — optimized response was "
                "returned from memory without new LLM generation."
            )

        else:

            st.success(
                "✅ Comparison completed successfully!"
            )

        # ====================================================
        # IMPORTANT CACHE HANDLING
        # ====================================================
        #
        # If cache HIT occurs, optimized.py intentionally
        # returns 0 tokens because no new generation happened.
        #
        # We must NOT treat those zero tokens as a new
        # optimized benchmark.
        #
        # Instead, use the last actual optimized benchmark
        # for cost/token comparison when possible.
        # ====================================================

        optimized_for_comparison = optimized

        if cache_hit:

            previous_actual = None

            for old_result in reversed(
                st.session_state.history
            ):

                if (
                    old_result.get("Question") == question
                    and old_result.get("Cache") == "MISS"
                ):

                    previous_actual = old_result
                    break

            if previous_actual is not None:

                optimized_for_comparison = {
                    "answer": optimized["answer"],
                    "model": optimized["model"],
                    "input_tokens": previous_actual[
                        "Optimized Input Tokens"
                    ],
                    "output_tokens": previous_actual[
                        "Optimized Output Tokens"
                    ],
                    "total_tokens": previous_actual[
                        "Optimized Tokens"
                    ],
                    "cache_hit": True
                }

            else:

                # No previous benchmark exists.
                # Keep actual zero-token cache result,
                # but don't claim a benchmark reduction.

                optimized_for_comparison = optimized

        # ====================================================
        # TOKEN VALUES
        # ====================================================

        baseline_input_tokens = baseline.get(
            "input_tokens",
            0
        )

        baseline_output_tokens = baseline.get(
            "output_tokens",
            0
        )

        baseline_total_tokens = baseline.get(
            "total_tokens",
            baseline_input_tokens + baseline_output_tokens
        )

        optimized_input_tokens = optimized_for_comparison.get(
            "input_tokens",
            0
        )

        optimized_output_tokens = optimized_for_comparison.get(
            "output_tokens",
            0
        )

        optimized_total_tokens = optimized_for_comparison.get(
            "total_tokens",
            optimized_input_tokens + optimized_output_tokens
        )

        # ====================================================
        # COST
        # ====================================================

        baseline_cost = calculate_cost(
            baseline_input_tokens,
            baseline_output_tokens
        )

        optimized_cost = calculate_cost(
            optimized_input_tokens,
            optimized_output_tokens
        )

        # ====================================================
        # COST PER 1000
        # ====================================================

        baseline_cost_1000 = (
            baseline_cost * 1000
        )

        optimized_cost_1000 = (
            optimized_cost * 1000
        )

        saving_1000 = (
            baseline_cost_1000
            - optimized_cost_1000
        )

        # ====================================================
        # MONTHLY COST
        # ====================================================

        baseline_monthly_cost = (
            baseline_cost
            * requests_per_month
        )

        optimized_monthly_cost = (
            optimized_cost
            * requests_per_month
        )

        monthly_saving = (
            baseline_monthly_cost
            - optimized_monthly_cost
        )

        # ====================================================
        # QUALITY
        # ====================================================

        baseline_quality = calculate_quality_score(
            baseline["answer"]
        )

        optimized_quality = calculate_quality_score(
            optimized["answer"]
        )

        quality_tradeoff = calculate_quality_tradeoff(
            baseline_quality,
            optimized_quality
        )

        # ====================================================
        # EFFICIENCY
        # ====================================================

        baseline_efficiency = calculate_efficiency(
            baseline_quality,
            baseline_total_tokens
        )

        optimized_efficiency = calculate_efficiency(
            optimized_quality,
            optimized_total_tokens
        )

        # ====================================================
        # REDUCTIONS
        # ====================================================

        if cache_hit and optimized_total_tokens == 0:

            token_reduction = 0
            cost_reduction = 0

        else:

            token_reduction = calculate_percentage_reduction(
                baseline_total_tokens,
                optimized_total_tokens
            )

            cost_reduction = calculate_percentage_reduction(
                baseline_cost,
                optimized_cost
            )

        # ====================================================
        # WORD COUNT
        # ====================================================

        baseline_words = len(
            baseline["answer"].split()
        )

        optimized_words = len(
            optimized["answer"].split()
        )

        # ====================================================
        # QUALITY MESSAGE
        # ====================================================

        if quality_tradeoff > 0:

            tradeoff_message = (
                "Quality improved while reducing measured cost."
            )

        elif quality_tradeoff == 0:

            tradeoff_message = (
                "Quality remained unchanged while reducing measured cost."
            )

        else:

            tradeoff_message = (
                f"Quality decreased by "
                f"{abs(quality_tradeoff):.0f} points."
            )

        # ====================================================
        # RECOMMENDATION
        # ====================================================

        if cache_hit and optimized_total_tokens == 0:

            recommendation = (
                "⚡ CACHE HIT"
            )

            recommendation_text = (
                "The optimized answer was served from cache. "
                "No new LLM tokens were generated, so this run "
                "is not counted as a new token/cost benchmark."
            )

        elif (
            optimized_quality >= baseline_quality
            and optimized_cost < baseline_cost
        ):

            recommendation = (
                "🟢 RECOMMEND OPTIMIZED"
            )

            recommendation_text = (
                "The optimized implementation is recommended "
                "because it reduces measured benchmark cost "
                "without reducing response quality."
            )

        elif (
            optimized_cost < baseline_cost
            and quality_tradeoff >= -5
        ):

            recommendation = (
                "🟡 OPTIMIZED WITH MONITORING"
            )

            recommendation_text = (
                "The optimized implementation provides measured "
                "cost savings with a small quality trade-off. "
                "Quality should be monitored in production."
            )

        else:

            recommendation = (
                "🔴 KEEP BASELINE"
            )

            recommendation_text = (
                "For this test, the baseline provides a better "
                "quality/cost trade-off."
            )

        # ====================================================
        # WINNER
        # ====================================================

        if cache_hit and optimized_total_tokens == 0:

            winner = "⚡ Cache"

        elif optimized_efficiency >= baseline_efficiency:

            winner = "🟢 Optimized"

        else:

            winner = "🔴 Baseline"

        # ====================================================
        # CACHE STATUS
        # ====================================================

        cache_status = (
            "HIT"
            if cache_hit
            else "MISS"
        )

        # ====================================================
        # SAVE HISTORY
        # ====================================================

        history_item = {

            "Question":
                question,

            "Baseline Input Tokens":
                baseline_input_tokens,

            "Baseline Output Tokens":
                baseline_output_tokens,

            "Baseline Tokens":
                baseline_total_tokens,

            "Optimized Input Tokens":
                optimized_input_tokens,

            "Optimized Output Tokens":
                optimized_output_tokens,

            "Optimized Tokens":
                optimized_total_tokens,

            "Baseline Cost":
                baseline_cost,

            "Optimized Cost":
                optimized_cost,

            "Cost Reduction (%)":
                cost_reduction,

            "Token Reduction (%)":
                token_reduction,

            "Baseline Quality":
                baseline_quality,

            "Optimized Quality":
                optimized_quality,

            "Quality Trade-off":
                quality_tradeoff,

            "Baseline Efficiency":
                baseline_efficiency,

            "Optimized Efficiency":
                optimized_efficiency,

            "Cost / 1000 Baseline":
                baseline_cost_1000,

            "Cost / 1000 Optimized":
                optimized_cost_1000,

            "Monthly Baseline":
                baseline_monthly_cost,

            "Monthly Optimized":
                optimized_monthly_cost,

            "Monthly Saving":
                monthly_saving,

            "Winner":
                winner,

            "Cache":
                cache_status
        }

        # Only add a new benchmark history item when
        # this is a real generation (MISS).
        #
        # Cache HIT is displayed but does not create
        # another benchmark that would distort averages.

        if not cache_hit:

            st.session_state.history.append(
                history_item
            )

        # Save current result for display
        st.session_state.last_result = {
            "baseline": baseline,
            "optimized": optimized,
            "optimized_comparison": optimized_for_comparison,
            "baseline_cost": baseline_cost,
            "optimized_cost": optimized_cost,
            "baseline_cost_1000": baseline_cost_1000,
            "optimized_cost_1000": optimized_cost_1000,
            "saving_1000": saving_1000,
            "baseline_monthly_cost": baseline_monthly_cost,
            "optimized_monthly_cost": optimized_monthly_cost,
            "monthly_saving": monthly_saving,
            "baseline_quality": baseline_quality,
            "optimized_quality": optimized_quality,
            "quality_tradeoff": quality_tradeoff,
            "baseline_efficiency": baseline_efficiency,
            "optimized_efficiency": optimized_efficiency,
            "token_reduction": token_reduction,
            "cost_reduction": cost_reduction,
            "baseline_words": baseline_words,
            "optimized_words": optimized_words,
            "tradeoff_message": tradeoff_message,
            "recommendation": recommendation,
            "recommendation_text": recommendation_text,
            "winner": winner,
            "cache_status": cache_status
        }


# ============================================================
# DISPLAY LAST RESULT
# ============================================================

result = st.session_state.last_result

if result is not None:

    baseline = result["baseline"]
    optimized = result["optimized"]

    baseline_cost = result["baseline_cost"]
    optimized_cost = result["optimized_cost"]

    baseline_cost_1000 = result["baseline_cost_1000"]
    optimized_cost_1000 = result["optimized_cost_1000"]

    saving_1000 = result["saving_1000"]

    baseline_monthly_cost = result["baseline_monthly_cost"]
    optimized_monthly_cost = result["optimized_monthly_cost"]

    monthly_saving = result["monthly_saving"]

    baseline_quality = result["baseline_quality"]
    optimized_quality = result["optimized_quality"]

    quality_tradeoff = result["quality_tradeoff"]

    baseline_efficiency = result["baseline_efficiency"]
    optimized_efficiency = result["optimized_efficiency"]

    token_reduction = result["token_reduction"]
    cost_reduction = result["cost_reduction"]

    baseline_words = result["baseline_words"]
    optimized_words = result["optimized_words"]

    tradeoff_message = result["tradeoff_message"]

    recommendation = result["recommendation"]
    recommendation_text = result["recommendation_text"]

    winner = result["winner"]
    cache_status = result["cache_status"]

    optimized_comparison = result[
        "optimized_comparison"
    ]

    # ========================================================
    # PERFORMANCE METRICS
    # ========================================================

    st.subheader(
        "📊 Performance Metrics"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🔴 Baseline Tokens",
        baseline["total_tokens"]
    )

    col2.metric(
        "🟢 Optimized Tokens",
        optimized_comparison["total_tokens"],
        delta=(
            f"-{token_reduction:.2f}%"
            if cache_status == "MISS"
            else "Cache"
        )
    )

    col3.metric(
        "🔴 Baseline Measured Cost",
        f"${baseline_cost:.6f}"
    )

    col4.metric(
        "🟢 Optimized Measured Cost",
        f"${optimized_cost:.6f}",
        delta=(
            f"-{cost_reduction:.2f}%"
            if cache_status == "MISS"
            else "Cache"
        )
    )

    # ========================================================
    # ANSWERS
    # ========================================================

    st.subheader(
        "📝 Before & After Answers"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            "### 🔴 Baseline"
        )

        st.info(
            baseline["answer"]
        )

        st.caption(
            f"Model: {baseline['model']}"
        )

        st.caption(
            f"📝 Words: {baseline_words}"
        )

    with col2:

        st.markdown(
            "### 🟢 Optimized"
        )

        st.success(
            optimized["answer"]
        )

        st.caption(
            f"Model: {optimized['model']}"
        )

        st.caption(
            f"📝 Words: {optimized_words}"
        )

        if cache_status == "HIT":

            st.info(
                "⚡ Cache HIT — this answer came from "
                "memory. No new LLM tokens were generated."
            )

        else:

            st.caption(
                "⚡ Cache: MISS"
            )

    # ========================================================
    # QUALITY
    # ========================================================

    st.subheader(
        "🎯 Quality Before & After"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🔴 Baseline Quality",
        f"{baseline_quality}/100"
    )

    col2.metric(
        "🟢 Optimized Quality",
        f"{optimized_quality}/100"
    )

    col3.metric(
        "🎯 Quality Change",
        f"{quality_tradeoff:+.0f}"
    )

    col4.metric(
        "🏆 Efficiency",
        f"{optimized_efficiency}"
    )

    if cache_status == "HIT":

        st.info(
            "⚡ Cache HIT: quality is shown for the cached "
            "answer, but this run is excluded from new "
            "cost/token benchmark calculations."
        )

    elif quality_tradeoff > 0:

        st.success(
            f"📈 {tradeoff_message}"
        )

    elif quality_tradeoff == 0:

        st.info(
            f"➡️ {tradeoff_message}"
        )

    else:

        st.warning(
            f"⚠️ {tradeoff_message}"
        )

    # ========================================================
    # COST PER 1000
    # ========================================================

    st.subheader(
        "💰 Measured Cost per 1,000 Requests"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🔴 Baseline",
        f"${baseline_cost_1000:.4f}"
    )

    col2.metric(
        "🟢 Optimized",
        f"${optimized_cost_1000:.4f}"
    )

    col3.metric(
        "💸 Saving / 1,000",
        f"${saving_1000:.4f}"
    )

    if cache_status == "HIT":

        st.caption(
            "ℹ️ These cost figures use the previous actual "
            "optimized generation for this same question, "
            "rather than treating the cache HIT as a new "
            "zero-token benchmark."
        )

    cost_table = pd.DataFrame({

        "Metric": [
            "Input Tokens",
            "Output Tokens",
            "Total Tokens",
            "Measured Cost per Request",
            "Measured Cost per 1,000 Requests"
        ],

        "Baseline": [
            baseline["input_tokens"],
            baseline["output_tokens"],
            baseline["total_tokens"],
            f"${baseline_cost:.6f}",
            f"${baseline_cost_1000:.4f}"
        ],

        "Optimized": [
            optimized_comparison["input_tokens"],
            optimized_comparison["output_tokens"],
            optimized_comparison["total_tokens"],
            f"${optimized_cost:.6f}",
            f"${optimized_cost_1000:.4f}"
        ]
    })

    st.dataframe(
        cost_table,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Cost is calculated from the actual token usage "
        "recorded during the benchmark generation."
    )

    # ========================================================
    # MONTHLY COST
    # ========================================================

    st.subheader(
        "📅 Monthly Cost Projection"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📨 Monthly Requests",
        f"{requests_per_month:,}"
    )

    col2.metric(
        "🔴 Baseline Monthly Cost",
        f"${baseline_monthly_cost:.2f}"
    )

    col3.metric(
        "🟢 Optimized Monthly Cost",
        f"${optimized_monthly_cost:.2f}"
    )

    col4.metric(
        "💰 Monthly Saving",
        f"${monthly_saving:.2f}"
    )

    # ========================================================
    # OPTIMIZATION RESULTS
    # ========================================================

    st.subheader(
        "📉 Optimization Results"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "💸 Cost Reduction",
        f"{cost_reduction:.2f}%"
    )

    col2.metric(
        "✂️ Token Reduction",
        f"{token_reduction:.2f}%"
    )

    col3.metric(
        "⚡ Cache",
        cache_status
    )

    col4.metric(
        "🎯 Quality Trade-off",
        f"{quality_tradeoff:+.0f}"
    )

    # ========================================================
    # QUALITY CHART
    # ========================================================

    st.subheader(
        "🎯 Quality Score Comparison"
    )

    quality_data = pd.DataFrame({

        "Implementation": [
            "Baseline",
            "Optimized"
        ],

        "Quality Score": [
            baseline_quality,
            optimized_quality
        ]
    })

    st.bar_chart(
        quality_data.set_index(
            "Implementation"
        )
    )

    # ========================================================
    # TOKEN CHART
    # ========================================================

    st.subheader(
        "📊 Token Usage Comparison"
    )

    token_data = pd.DataFrame({

        "Implementation": [
            "Baseline",
            "Optimized"
        ],

        "Tokens": [
            baseline["total_tokens"],
            optimized_comparison["total_tokens"]
        ]
    })

    st.bar_chart(
        token_data.set_index(
            "Implementation"
        )
    )

    # ========================================================
    # COST CHART
    # ========================================================

    st.subheader(
        "💰 Measured Cost per 1,000 Requests"
    )

    cost_chart = pd.DataFrame({

        "Implementation": [
            "Baseline",
            "Optimized"
        ],

        "Cost": [
            baseline_cost_1000,
            optimized_cost_1000
        ]
    })

    st.bar_chart(
        cost_chart.set_index(
            "Implementation"
        )
    )

    # ========================================================
    # FINAL RECOMMENDATION
    # ========================================================

    st.subheader(
        "🏆 Final Recommendation"
    )

    if cache_status == "HIT":

        st.info(
            f"""
### {recommendation}

{recommendation_text}

**Cache Status:** HIT

The cache prevented a new model generation for this request.
"""
        )

    elif recommendation == "🟢 RECOMMEND OPTIMIZED":

        st.success(
            f"""
### {recommendation}

{recommendation_text}

**Cost Reduction:** {cost_reduction:.2f}%

**Token Reduction:** {token_reduction:.2f}%

**Quality Change:** {quality_tradeoff:+.0f} points

**Saving per 1,000 requests:** ${saving_1000:.4f}

**Projected Monthly Saving:** ${monthly_saving:.2f}
"""
        )

    elif recommendation == "🟡 OPTIMIZED WITH MONITORING":

        st.warning(
            f"""
### {recommendation}

{recommendation_text}

**Cost Reduction:** {cost_reduction:.2f}%

**Token Reduction:** {token_reduction:.2f}%

**Quality Change:** {quality_tradeoff:+.0f} points

**Saving per 1,000 requests:** ${saving_1000:.4f}

**Projected Monthly Saving:** ${monthly_saving:.2f}
"""
        )

    else:

        st.error(
            f"""
### {recommendation}

{recommendation_text}

**Cost Reduction:** {cost_reduction:.2f}%

**Token Reduction:** {token_reduction:.2f}%

**Quality Change:** {quality_tradeoff:+.0f} points
"""
        )

    # ========================================================
    # OPTIMIZATION SUMMARY
    # ========================================================

    st.subheader(
        "🎯 Optimization Summary"
    )

    st.markdown(
        f"""
**Question:** {question}

**Baseline Model:** `{baseline["model"]}`

**Optimized Model:** `{optimized["model"]}`

**Baseline Tokens:** `{baseline["total_tokens"]}`

**Optimized Tokens:** `{optimized_comparison["total_tokens"]}`

**Cost Reduction:** `{cost_reduction:.2f}%`

**Token Reduction:** `{token_reduction:.2f}%`

**Baseline Quality:** `{baseline_quality}/100`

**Optimized Quality:** `{optimized_quality}/100`

**Quality Trade-off:** `{quality_tradeoff:+.0f} points`

**Baseline Measured Cost / 1,000 Requests:** `${baseline_cost_1000:.4f}`

**Optimized Measured Cost / 1,000 Requests:** `${optimized_cost_1000:.4f}`

**Saving / 1,000 Requests:** `${saving_1000:.4f}`

**Monthly Requests:** `{requests_per_month:,}`

**Baseline Monthly Cost:** `${baseline_monthly_cost:.2f}`

**Optimized Monthly Cost:** `${optimized_monthly_cost:.2f}`

**Monthly Saving:** `${monthly_saving:.2f}`

**Overall Efficiency Winner:** `{winner}`

**Cache Status:** `{cache_status}`

**Final Recommendation:** `{recommendation}`
"""
    )


# ============================================================
# OPTIMIZATION HISTORY
# ============================================================

if st.session_state.history:

    st.divider()

    st.subheader(
        "📈 Optimization History"
    )

    history_df = pd.DataFrame(
        st.session_state.history
    )

    display_df = history_df.copy()

    # ========================================================
    # FORMAT CURRENCY
    # ========================================================

    currency_columns = [
        "Baseline Cost",
        "Optimized Cost",
        "Cost / 1000 Baseline",
        "Cost / 1000 Optimized",
        "Monthly Baseline",
        "Monthly Optimized",
        "Monthly Saving"
    ]

    for column in currency_columns:

        if column in display_df.columns:

            if "1000" in column:

                display_df[column] = display_df[column].map(
                    lambda x: f"${x:.4f}"
                )

            elif "Monthly" in column:

                display_df[column] = display_df[column].map(
                    lambda x: f"${x:.2f}"
                )

            else:

                display_df[column] = display_df[column].map(
                    lambda x: f"${x:.6f}"
                )

    # ========================================================
    # FORMAT PERCENTAGES
    # ========================================================

    percentage_columns = [
        "Cost Reduction (%)",
        "Token Reduction (%)"
    ]

    for column in percentage_columns:

        if column in display_df.columns:

            display_df[column] = display_df[column].map(
                lambda x: f"{x:.2f}%"
            )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # EXPORT
    # ========================================================

    st.subheader(
        "📥 Export Cost Analysis"
    )

    csv_data = history_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Cost Analysis CSV",
        data=csv_data,
        file_name="llm_cost_optimisation_analysis.csv",
        mime="text/csv"
    )

    # ========================================================
    # OVERALL PERFORMANCE
    # ========================================================

    st.subheader(
        "📊 Overall Performance"
    )

    avg_cost_reduction = (
        history_df[
            "Cost Reduction (%)"
        ].mean()
    )

    avg_token_reduction = (
        history_df[
            "Token Reduction (%)"
        ].mean()
    )

    avg_quality_optimized = (
        history_df[
            "Optimized Quality"
        ].mean()
    )

    total_tests = len(
        history_df
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🧪 Total Tests",
        total_tests
    )

    col2.metric(
        "💸 Avg Cost Reduction",
        f"{avg_cost_reduction:.2f}%"
    )

    col3.metric(
        "✂️ Avg Token Reduction",
        f"{avg_token_reduction:.2f}%"
    )

    col4.metric(
        "🎯 Avg Optimized Quality",
        f"{avg_quality_optimized:.1f}/100"
    )


# ============================================================
# PROJECT INFORMATION
# ============================================================

st.divider()

st.subheader(
    "📚 Optimizations Applied"
)

st.markdown(
    """
### 1. ✂️ Prompt Compression

The optimized implementation uses a shorter prompt,
reducing unnecessary input tokens.

### 2. 🤖 Model Routing

Simple questions are routed to a smaller model when
available, while longer questions use a stronger model.

### 3. ⚡ Response Caching

Repeated questions are stored in memory and can be
returned without generating new tokens.

### 4. 📉 Token Reduction

The system compares actual token usage between
baseline and optimized implementations.

### 5. 🎯 Quality Measurement

Response quality is measured before and after
optimization using a local rule-based scoring system.

### 6. 📊 Measured Cost per 1,000 Requests

The dashboard calculates benchmark cost for 1,000
requests using recorded input/output token usage.

### 7. 📅 Monthly Cost Projection

Users can enter expected monthly request volume
to calculate baseline cost, optimized cost and savings.

### 8. ⚖️ Quality-Cost Trade-off

The system compares cost reduction against changes
in response quality.

### 9. 🏆 Final Recommendation

The dashboard recommends whether the optimized
implementation should be used based on measured
cost and quality results.

### 10. 📈 Optimization History

Multiple actual generation experiments are recorded
during the current Streamlit session.

### 11. 📥 Cost Analysis Export

Experiment results can be downloaded as a CSV file.
"""
)


# ============================================================
# LOCAL EXECUTION
# ============================================================

st.subheader(
    "🆓 Local Execution"
)

st.markdown(
    """
This project runs locally without requiring an OpenAI API
key or paid API credits.

The LLM is executed through Ollama.
"""
)


# ============================================================
# PROJECT GOAL
# ============================================================

st.subheader(
    "🎯 Project Goal"
)

st.markdown(
    """
Reduce the cost of an LLM-powered feature without materially
hurting quality, then measure and explain the resulting
quality/cost trade-off.
"""
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
<center>

💰 <b>LLM Cost Optimisation Study</b>

<br><br>

👩‍💻 Created by <b>Tehmina Anwar</b>

<br>

AI/ML Engineer | Python Developer | Generative AI Enthusiast

<br><br>

🆓 Free Local Demonstration

<br><br>

Built with Python • Streamlit • Pandas

</center>
""",
    unsafe_allow_html=True
)