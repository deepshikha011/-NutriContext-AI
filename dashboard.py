import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import get_last_7_days, get_today_meals, get_evening_snack_pattern, get_daily_calories_today
from logic import calculate_daily_health_score, get_pattern_insights


def show_dashboard(user: dict):
    st.markdown("## 📊 Your Dashboard")

    today_calories = get_daily_calories_today(user["id"])
    target = user["target_calories"]
    remaining = max(0, target - today_calories)

    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 Calories Today", f"{today_calories} kcal", delta=f"-{remaining} remaining")
    col2.metric("🎯 Daily Target", f"{target} kcal")
    col3.metric("🏆 Goal", user["goal"])

    st.divider()

    rows = get_last_7_days(user["id"])
    if not rows:
        st.info("No meal data yet. Start logging meals to see your trends!")
        return

    df = pd.DataFrame(rows, columns=["date", "total_calories", "avg_health_score", "meal_count", "total_carbs", "total_protein", "total_fats"])
    df["date"] = pd.to_datetime(df["date"])
    df["daily_health_score"] = df.apply(
        lambda r: calculate_daily_health_score(int(r["total_calories"]), target, float(r["avg_health_score"])), axis=1
    )

    _calorie_trend_chart(df, target)
    _health_score_chart(df)
    _macro_breakdown_chart(df)
    _pattern_insights(user)
    _today_meals_table(user)


def _calorie_trend_chart(df: pd.DataFrame, target: int):
    st.markdown("### 📈 Calorie Trend (Last 7 Days)")
    fig = px.line(df, x="date", y="total_calories", markers=True,
                  labels={"total_calories": "Calories (kcal)", "date": "Date"},
                  color_discrete_sequence=["#00d4aa"])
    fig.add_hline(y=target, line_dash="dash", line_color="#ff6b6b",
                  annotation_text="Daily Target", annotation_position="top right")
    fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)


def _health_score_chart(df: pd.DataFrame):
    st.markdown("### 🏅 Daily Health Score (Last 7 Days)")
    fig = px.bar(df, x="date", y="daily_health_score",
                 labels={"daily_health_score": "Health Score (0-100)", "date": "Date"},
                 color="daily_health_score",
                 color_continuous_scale=["#ff6b6b", "#ffd93d", "#00d4aa"],
                 range_color=[0, 100])
    fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)


def _macro_breakdown_chart(df: pd.DataFrame):
    st.markdown("### 🥩 Macro Breakdown (Last 7 Days)")
    fig = go.Figure()
    for macro, color in [("total_protein", "#00d4aa"), ("total_carbs", "#ffd93d"), ("total_fats", "#ff6b6b")]:
        fig.add_trace(go.Bar(name=macro.replace("total_", "").capitalize(),
                             x=df["date"], y=df[macro], marker_color=color))
    fig.update_layout(barmode="stack", template="plotly_dark",
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      yaxis_title="Grams")
    st.plotly_chart(fig, use_container_width=True)


def _pattern_insights(user: dict):
    st.markdown("### 🔍 Pattern Detection")
    count = get_evening_snack_pattern(user["id"])
    insights = get_pattern_insights(count)
    if insights:
        for insight in insights:
            st.warning(insight)
    else:
        st.success("✅ Great habits this week! No concerning patterns detected.")


def _today_meals_table(user: dict):
    st.markdown("### 🍽️ Today's Meals")
    rows = get_today_meals(user["id"])
    if not rows:
        st.info("No meals logged today.")
        return
    df = pd.DataFrame(rows, columns=["Food", "Calories", "Protein(g)", "Carbs(g)", "Fats(g)",
                                      "Health Score", "Context", "Warning", "Smart Swap", "Logged At"])
    df["Logged At"] = pd.to_datetime(df["Logged At"]).dt.strftime("%H:%M")
    st.dataframe(df[["Food", "Calories", "Protein(g)", "Carbs(g)", "Fats(g)", "Health Score", "Context", "Logged At"]],
                 use_container_width=True)
