from flask import Flask, request
import openai
import os

app = Flask(__name__)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/', methods=['GET', 'POST'])
def home():
    image_url = ""
    prompt = ""

    if request.method == 'POST':
        prompt = request.form.get('prompt', 'A fantasy landscape')
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            image_url = response.data[0].url
        except Exception as e:
            image_url = ""
            prompt = f"Error: {str(e)}"

    return f'''
        <form method="POST">
            <input name="prompt" placeholder="Describe an image" style="width: 300px;" />
            <button type="submit">Generate Image</button>
        </form>
        <h2>Prompt:</h2><p>{prompt}</p>
        {'<img src="' + image_url + '" style="max-width: 500px;"/>' if image_url else ''}
    '''

if __name__ == '__main__':
    app.run()
