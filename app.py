from flask import Flask, request
import openai
import os

app = Flask(__name__)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form.get('prompt', 'No prompt provided')

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"Error: {str(e)}"

        return (
            f"<h1>Prompt:</h1><p>{prompt}</p>"
            f"<h2>ChatGPT says:</h2><p>{reply}</p>"
            f'<a href="/">Try another</a>'
        )

    return (
        '<form method="POST">'
        '<input name="prompt" placeholder="Ask ChatGPT" style="width: 300px;" />'
        '<button type="submit">Submit</button>'
        '</form>'
    )

if __name__ == '__main__':
    app.run()
