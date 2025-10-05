Inspire AI 🌿

Description:
AI-powered chat assistant for parents of children with mental health challenges, providing daily support, guidance, and motivation.

Table of Contents

Overview

Features

Architecture

Setup & Installation

Environment Variables

Running the App

API Endpoints

Development & Deployment

Future Improvements

Overview

Inspire AI 🌿 is a backend service that provides an empathetic, supportive AI chat assistant for parents of children with serious mental health conditions. It’s designed to help parents:

Stay motivated and consistent in daily caregiving.

Track small improvements in the child’s behavior.

Receive positive reinforcement and micro-guidance.

Use a session-based chat with personalized AI responses.

The AI agent uses OpenAI’s GPT models with enhanced prompts and a system designed to maximize empathy, positivity, and practical advice.

Features

AI chat with session-based history per user.

Empathy-driven system prompt for consistent tone.

Randomized supportive phrases to avoid repetition.

REST API with Swagger documentation.

User authentication (register/login).

Microservices-ready architecture.

Easily updatable AI logic as you continue fine-tuning.

Architecture

Microservices Ready: The AI chat is structured as a standalone service (ai.py) and can be integrated with other services.

Modules:

services/users.py → User authentication and management.

services/ai.py → AI response generation with chat history.

app.py → Main Flask REST API with namespaces for auth and chat.

Data Flow:

Parent logs in or registers.

Sends a message via POST /chat/.

AI generates empathetic response using GPT API and session-based chat history.

Response returned with timestamp and stored in memory (can later be connected to a database).

Setup & Installation

Clone the repository

git clone https://github.com/<your-username>/inspire-ai-chat.git
cd inspire-ai-chat


Create a virtual environment

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows


Install dependencies

pip install -r requirements.txt


Set environment variables

Create a .env file in the root:

OPENAI_API_KEY=<your_openai_api_key>
FLASK_SECRET_KEY=<your_flask_secret_key>

Running the App
python app.py


Swagger UI: http://127.0.0.1:5001/swagger

Chat endpoint: POST /chat/

Auth endpoints: POST /auth/register and POST /auth/login

API Endpoints
Auth

POST /auth/register — Register a new user

POST /auth/login — Login, returns user_id

Chat

POST /chat/ — Send a message to AI

Request body example:

{
  "user_id": "demo_user",
  "message": "Сегодня снова без изменений"
}


Response example:

{
  "reply": "Спасибо, что поделились этим. 🌟 Каждый день вашей заботы — маленькая победа. Ты справишься! 💚",
  "time": "14:03"
}

Development & Deployment

Continuous updates are supported: push code to the repo → backend can automatically pull changes.

AI logic is in services/ai.py → easily fine-tuned by updating the SYSTEM_PROMPT or adding new training datasets.

Dockerizing is recommended for production deployments.

Future Improvements

Integrate persistent database for chat histories.

Fine-tune AI on user-specific datasets for better personalization.

Add mobile or web frontend to connect with backend.

Add notification system for daily reminders or affirmations.
