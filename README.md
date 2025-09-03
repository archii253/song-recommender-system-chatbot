# 🎵 Song Recommender System Chatbot  

An **AI-powered chatbot** that recommends songs based on user mood, queries, or preferences.  
Built with **Flask (Python)** for backend, **React + Tailwind CSS** for frontend, and **Collaborative Filtering** for recommendations.  

---

## 🚀 Features  
- 🤖 Chatbot interface for natural interaction  
- 🎧 Personalized song recommendations  
- 🧠 NLP support for mood/artist queries  
- 🌐 Full-stack: Flask API + React UI  
- 📊 Clean and scalable project structure  

---
## 🛠️ Tech Stack

Frontend: React, Tailwind CSS

Backend: Flask, Python

ML/NLP: Scikit-learn, NLTK

Database: SQLite / MySQL

## ⚙️ Setup  

### 1️⃣ Clone the Repository  
git clone https://github.com/your-username/song-recommender-system-chatbot.git
cd song-recommender-system-chatbot

### 2️⃣ Backend (Flask)
cd backend
python -m venv venv
venv\Scripts\activate   # Windows  
source venv/bin/activate  # Linux/Mac  

pip install -r requirements.txt
python app.py

### 3️⃣ Frontend (React)
cd frontend
npm install
npm run dev

## 📂 Project Structure
backend/   → Flask API + ML/NLP models  
frontend/  → React + Tailwind chatbot UI  
ml_models/ → Pre-trained recommendation models  
