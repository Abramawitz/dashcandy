import openai
import os
from flask import Flask, request

openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this in your environment

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message['content']
        return f"<h1>AI says:</h1><p>{reply}</p>"
    return '''
        <form method="POST">
            <input name="prompt" placeholder="Ask ChatGPT" />
            <button type="submit">Submit</button>
        </form>
    '''

if __name__ == '__main__':
    app.run()
