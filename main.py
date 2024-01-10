from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from the .env file
api_key = os.getenv("openAI_key")
openai.api_key = api_key


app = Flask(__name__)
CORS(app)

def get_gpt_response(input_string, content):
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {
                "role": "system",
                "content": input_string  # The users input
            },
            {
                "role": "user",
                "content": content  # The task of the bot eg, be a helpful assistant
            }
        ]
    )
    return response['choices'][0]['message']['content'].strip()


@app.route('/', methods=['POST'])
def process_string():

    # Get the input string from the request
    input_data = request.json

    # Check if input_data is provided
    if 'user_input' not in input_data or 'content' not in input_data:
        return jsonify({'error': 'Both user_input and content are required'}), 400

    # Extract the user input and content from the api call
    user_input = input_data['user_input']
    content = input_data['content']

    # Process the input string
    response = get_gpt_response(user_input, content)

    # Return the processed string
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)

# TODO
# Add chatGPT logic to process_input func /
# Add the .env functionality to the script to keep the API key secret /
# May need to use cors
