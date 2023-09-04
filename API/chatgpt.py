# chatgpt_integration/api.py
import requests
OPENAI_API_KEY = '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'
OPENAI_API_ENDPOINT = 'https://chatgpt-api.shn.hk/v1/'
def generate_chat_response(prompt):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }

    data = {
        "model": "gpt-3.5-turbo-0613",
        "messages": [{"role": "user", "content": "Hello, how are you?"}]
    }

    response = requests.post(
        OPENAI_API_ENDPOINT,
        headers=headers,
        json=data
    )

    return response.json()

print(generate_chat_response('what is a book?'))

"""# chatgpt_integration/api.py
import openai

openai.api_key = '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'

def generate_chat_response():
    messages = [{"role": "system", "content": "You are an intelligent assistant."}]

    while True:
        user_message = input("User: ")
        if user_message:
            messages.append({"role": "user", "content": user_message})

            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            assistant_reply = chat.choices[0].message.content
            print(f"ChatGPT: {assistant_reply}")

            messages.append({"role": "assistant", "content": assistant_reply})

generate_chat_response()

"""