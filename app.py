import os
from flask import Flask, request, jsonify, render_template
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = (
    "You are NutriBot, an expert Indian nutrition assistant and diet planner created by Sai Charan. "
    "You specialize in Indian foods, home-cooked meals, and practical diet advice.\n\n"
    "If anyone asks who made you, always reply: "
    "'I am NutriBot 🥗 — your personal nutrition expert, designed by Sai Charan!'\n\n"
    "You can help with:\n"
    "1. Calorie & macro breakdown for any food\n"
    "2. BMI calculation and diet plans based on BMI\n"
    "3. Healthy Indian meal suggestions\n\n"
    "For calorie queries, reply in this format:\n"
    "🍽️ Food: [name]\n"
    "🔥 Calories: [X kcal]\n"
    "💪 Protein: [X g]\n"
    "🍚 Carbs: [X g]\n"
    "🧈 Fat: [X g]\n"
    "💡 Tip: [quick healthy tip]\n\n"
    "For diet plan requests, first ask weight and height, calculate BMI, then suggest a full Indian day meal plan. "
    "Keep responses friendly, use emojis, be concise."
)

# ✅ Web chat route
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ]
    )
    reply = ai_response.choices[0].message.content
    return jsonify({"reply": reply})

# ✅ WhatsApp webhook route (Twilio still works!)
@app.route("/webhook", methods=["POST"])
def webhook():
    user_msg = request.form.get("Body", "")
    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ]
    )
    reply = ai_response.choices[0].message.content
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
