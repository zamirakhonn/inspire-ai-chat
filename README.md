# 🌿 Inspire AI

![Python](https://img.shields.io/badge/python-3.12-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

AI-powered chat assistant for parents of children with mental health challenges, providing **daily support, guidance, and motivation**.

---

## 📖 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Running the App](#running-the-app)
- [API Endpoints](#api-endpoints)
- [Development & Deployment](#development--deployment)
- [Future Improvements](#future-improvements)

---

## 🌟 Overview
Inspire AI 🌿 is a **backend service** that provides an **empathetic AI chat assistant** for parents of children with serious mental health conditions.  

It helps parents to:  
- Stay motivated and consistent in daily caregiving 💪  
- Track small improvements in the child’s behavior 📈  
- Receive positive reinforcement and micro-guidance 🌈  
- Use a session-based chat with personalized AI responses 🗨️  

The AI agent uses **OpenAI GPT models** with enhanced prompts designed to maximize **empathy, positivity, and practical advice**.

---

## ✨ Features
| Feature | Description |
|---------|-------------|
| 💬 AI Chat | Session-based history per user |
| 🤝 Empathy System | Predefined system prompts ensure supportive tone |
| 🔄 Randomized Phrases | Avoid repetitive responses |
| 🛠 REST API | Full Swagger documentation |
| 🔑 Authentication | Register/Login with user management |
| ⚙️ Microservices-ready | AI logic in standalone service (ai.py) |
| 🔄 Easily Updatable | Push updates to fine-tune AI |

---

## 🏗 Architecture
**Microservices Ready:** The AI chat runs as a standalone service (`services/ai.py`) and integrates with other services.  

**Modules:**  
- `services/users.py` → User authentication & management  
- `services/ai.py` → AI response generator & chat history  
- `app.py` → Flask REST API with namespaces for `auth` & `chat`  

**Data Flow:**


flowchart LR
    A["Parent/User"] -->|POST /auth/login or /register| B["Flask API"]
    B --> C["Auth Service - users.py"]
    B --> D["AI Service - ai.py"]
    D -->|AI Response| B
    B -->|Return JSON| A


