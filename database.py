import streamlit as st
import psycopg2
import psycopg2.extras
from datetime import date


def get_connection():
    db = st.secrets["database"]
    conn = psycopg2.connect(
        host=db["host"],
        port=db["port"],
        dbname=db["name"],
        user=db["user"],
        password=db["password"],
        sslmode="require"
    )
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            goal TEXT,
            target_calories INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            food_name TEXT,
            calories INTEGER,
            protein REAL,
            carbs REAL,
            fats REAL,
            health_score INTEGER,
            meal_context TEXT,
            warning TEXT,
            smart_swap TEXT,
            logged_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


# ---------- User Queries ----------

def create_user(username, password_hash, goal, target_calories):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, password_hash, goal, target_calories) VALUES (%s, %s, %s, %s)",
            (username, password_hash, goal, target_calories)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()


def get_user(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash, goal, target_calories FROM users WHERE username = %s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "password_hash": row[2], "goal": row[3], "target_calories": row[4]}
    return None


def update_profile(user_id, goal, target_calories):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET goal = %s, target_calories = %s WHERE id = %s", (goal, target_calories, user_id))
    conn.commit()
    cur.close()
    conn.close()


# ---------- Meal Queries ----------

def log_meal(user_id, food_name, calories, protein, carbs, fats, health_score, meal_context, warning, smart_swap):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO meals (user_id, food_name, calories, protein, carbs, fats, health_score, meal_context, warning, smart_swap)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (user_id, food_name, calories, protein, carbs, fats, health_score, meal_context, warning, smart_swap))
    conn.commit()
    cur.close()
    conn.close()


def get_today_meals(user_id):
    conn = get_connection()
    cur = conn.cursor()
    today = date.today().isoformat()
    cur.execute("""
        SELECT food_name, calories, protein, carbs, fats, health_score, meal_context, warning, smart_swap, logged_at
        FROM meals WHERE user_id = %s AND DATE(logged_at) = %s ORDER BY logged_at DESC
    """, (user_id, today))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_last_7_days(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT DATE(logged_at) as day, SUM(calories), AVG(health_score), COUNT(*),
               SUM(carbs), SUM(protein), SUM(fats)
        FROM meals WHERE user_id = %s AND logged_at >= NOW() - INTERVAL '7 days'
        GROUP BY day ORDER BY day
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_evening_snack_pattern(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM meals
        WHERE user_id = ?
          AND meal_context IN ('Evening Snack', 'Late Night Snack')
          AND health_score < 50
          AND logged_at >= NOW() - INTERVAL '7 days'
    """, (user_id,))
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return count


def get_daily_calories_today(user_id):
    conn = get_connection()
    cur = conn.cursor()
    today = date.today().isoformat()
    cur.execute("""
        SELECT COALESCE(SUM(calories), 0) FROM meals
        WHERE user_id = %s AND DATE(logged_at) = %s
    """, (user_id, today))
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return total
