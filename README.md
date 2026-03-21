# NutriContext AI 🥗🤖

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

**AI-Powered Meal Analysis with Personalized Nutrition Insights**

Upload a photo of your meal, and [Gemini AI](https://ai.google.dev/) instantly analyzes it – detecting food items, estimating nutrition (calories, macros), scoring healthiness, and providing **personalized recommendations** based on your fitness goal (Weight Loss, Muscle Gain, Keto, etc.).

Gets **context-aware** (post-workout? late night?) and suggests **smart swaps**!

## 🚀 Features

- 🖼️ **AI Vision Analysis**: Gemini 2.5 Flash detects food & estimates nutrition from any meal photo
- 👤 **User Profiles**: Set goals, daily calorie targets
- ⚠️ **Smart Warnings**: Context-aware alerts (e.g., 'Heavy carbs after workout!')
- 💡 **Smart Swaps**: Healthier alternatives tailored to your goal
- 📊 **Dashboard**: Track logged meals, nutrition trends
- 🔒 **Secure Auth**: Username/password + bcrypt
- 🗄️ **Database**: PostgreSQL logging
- 🌙 **Dark Mode**: Beautiful responsive UI

## 📱 Live Demo
*(Coming soon after Streamlit Cloud deploy!)*

## 🎯 Quick Start (Local)

1. **Clone & Install**
   ```bash
   git clone https://github.com/deepshikha011/-NutriContext-AI.git
   cd NutriContext-AI
   pip install -r requirements.txt
   ```

2. **Get Gemini API Key**
   - [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Add to `.streamlit/secrets.toml`:
     ```
     GEMINI_API_KEY = "your_key_here"
     ```

3. **Database** (PostgreSQL)
   - Update connection in `database.py` (or use env vars)

4. **Run**
   ```bash
   streamlit run app.py
   ```

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI**: Google Gemini 2.5 Flash (Vision)
- **Backend**: Python, psycopg2 (PostgreSQL)
- **Auth**: bcrypt
- **Deployment**: Streamlit Cloud

## 📁 Structure
```
.
├── app.py              # Main Streamlit app
├── ai_engine.py        # Gemini AI meal analysis
├── database.py         # PostgreSQL ops
├── auth.py            # Login/signup
├── dashboard.py        # Analytics UI
├── logic.py           # Business rules
├── requirements.txt    # Dependencies
└── .streamlit/secrets.toml  # API keys (gitignored)
```

## 🤝 Contributing
1. Fork & PR
2. Add your nutrition AI improvements!
3. Issues welcome 🐛

## 📄 License
MIT

**Made with ❤️ for health-conscious eaters**

