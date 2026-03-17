from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key="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")

@app.route("/webhook", methods=["POST"])
def webhook():
    user_msg = request.form.get("Body", "")

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a nutrition expert specializing in Indian foods. "
                    "When a user sends a food item or meal (like '2 idlis, 1 dosa, biryani'), "
                    "reply with approximate calories and macros in this exact format:\n\n"
                    "🍽️ *Food:* [food name]\n"
                    "🔥 *Calories:* [X kcal]\n"
                    "💪 *Protein:* [X g]\n"
                    "🍚 *Carbs:* [X g]\n"
                    "🧈 *Fat:* [X g]\n\n"
                    "Keep it short, friendly, and accurate. Support Indian foods like idli, dosa, biryani, dal, roti, sabzi, etc."
                )
            },
            {"role": "user", "content": user_msg}
        ]
    )

    reply = ai_response.choices[0].message.content
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
