from datetime import datetime


def get_meal_context(dt: datetime = None) -> str:
    if dt is None:
        dt = datetime.now()
    hour = dt.hour
    if 5 <= hour < 10:
        return "Breakfast"
    elif 10 <= hour < 12:
        return "Mid-Morning Snack"
    elif 12 <= hour < 15:
        return "Lunch"
    elif 15 <= hour < 18:
        return "Afternoon Snack"
    elif 18 <= hour < 21:
        return "Dinner"
    elif 21 <= hour < 24:
        return "Late Night Snack"
    else:
        return "Early Morning Snack"


def get_warning(food_name: str, meal_context: str, goal: str, calories: int, health_score: int) -> str | None:
    warnings = []
    late_contexts = {"Late Night Snack", "Early Morning Snack"}

    if meal_context in late_contexts and health_score < 60:
        warnings.append(f"⚠️ Eating {food_name} late at night may hinder your {goal} goal.")

    if goal == "Weight Loss" and calories > 600:
        warnings.append(f"⚠️ This meal has {calories} kcal — quite high for a Weight Loss goal.")

    if goal == "Keto" and health_score < 50:
        warnings.append("⚠️ This meal may not align with a Keto diet (possibly high in carbs).")

    if goal == "Muscle Gain" and health_score < 40:
        warnings.append("⚠️ Low nutritional quality detected — consider a protein-rich alternative.")

    return " ".join(warnings) if warnings else None


def calculate_daily_health_score(total_calories: int, target_calories: int, avg_meal_score: float) -> int:
    if target_calories == 0:
        return 0
    calorie_ratio = total_calories / target_calories
    if calorie_ratio <= 1.0:
        calorie_score = 100
    elif calorie_ratio <= 1.2:
        calorie_score = 70
    elif calorie_ratio <= 1.5:
        calorie_score = 40
    else:
        calorie_score = 10

    score = int((calorie_score * 0.5) + (avg_meal_score * 0.5))
    return max(0, min(100, score))


def get_pattern_insights(evening_unhealthy_count: int) -> list[str]:
    insights = []
    if evening_unhealthy_count >= 4:
        insights.append(f"🔴 You've had {evening_unhealthy_count} unhealthy evening/late-night snacks this week. Consider lighter options after 6 PM.")
    elif evening_unhealthy_count >= 2:
        insights.append(f"🟡 You've had {evening_unhealthy_count} unhealthy evening snacks this week. Watch your late-night habits.")
    return insights
