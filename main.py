from flask import Flask, request, jsonify, session
from flask_cors import CORS
import openai
import secrets

openai.api_key = "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"
secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
CORS(app)

responses = {}  # This will store the responses from each user


valid_responses = [
    ["Hello!", "Hi!", "Hello, Eden AI!"],
    ["Yes, I am ready.", "Sure.", "Absolutely."],
    ["In 6 months.", "In one year.", "As soon as possible."],
    ["Yes, I am.", "Not yet.", "I am currently looking for one."],
    ["I have $50,000 saved up.", "I have a budget of $100,000.", "I can put down $75,000."],
    ["Yes, I have.", "Not yet.", "I am planning to do so."],
    ["Yes, I would need that.", "No, I have got it figured out.", "Maybe."],
    ["I am looking for a property in New York.", "Somewhere in California.", "I would prefer Texas."],
    ["A 2 bedroom house.", "A house with 3 bedrooms and 2 bathrooms.", "A 4 bedroom house with a garage."],
    ["A big garden.", "I would love a pool.", "A big kitchen is a must."],
]




def chatbot(system_message, user_message):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages)
    return response.choices[0].message["content"]

@app.route('/get-start-message', methods=['GET'])
def get_start_message():
    session_id = request.cookies.get('session_id')
    responses[session_id] = []
    system_message = "Welcome to Eden AI! Are you ready to start the home buying process?"
    valid_responses = ["Yes, I am.", "No, I'm just browsing."]  # Valid responses for the initial message
    return jsonify({'message': system_message, 'valid_responses': valid_responses})

#comment
@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_message = data['message']
    step = data.get('step', 0)
    session_id = request.cookies.get('session_id')

    if session_id not in responses:
        responses[session_id] = []

    responses[session_id].append(user_message)  # Store user's response

    system_messages = [
        "Welcome to Eden AI! Are you ready to start the home buying process?",
        "Determine if the user is ready to start the home buying process.",
        "Ask about the timeline for making a purchase.",
        "Inquire if the user is already working with a real estate agent.",
        "Inquire about the user's budget and how much down payment they have.",
        "Ask if the user has discussed financing options with a bank or a mortgage agent.",
        "Help users calculate their potential mortgage, based on income, loans and credit score.",
        "Inquire about desired property location and type.",
        "Ask about property specifications like number of bedrooms, bathrooms, parking spaces, etc.",
        "Ask about user's property preferences (must haves or must not haves)."
    ]

    valid_responses = [
        ["Yes, I am.", "No, I'm just browsing."],
        ["In a month.", "In six months.", "In a year."],
        ["Yes, I am.", "No, I'm not."],
        # more arrays of valid responses
    ]

    if step < len(system_messages):
        system_message = system_messages[step]
        current_valid_responses = valid_responses[step]
    else:
        system_message = "No more questions."
        current_valid_responses = []

    step = (step + 1) % len(system_messages)

    return jsonify({'message': system_message, 'valid_responses': current_valid_responses, 'step': step})


if __name__ == '__main__':
    app.run(port=5000)
