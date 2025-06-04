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
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Image Generator</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #f5f7fa;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            color: #333;
        }}
        h1 {{
            margin-bottom: 20px;
        }}
        form {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }}
        input {{
            padding: 10px;
            width: 300px;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 16px;
        }}
        button {{
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
        }}
        button:hover {{
            background-color: #0056b3;
        }}
        img {{
            margin-top: 30px;
            max-width: 80%;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>
<body>
    <h1>AI Image Generator</h1>
    <form method="POST">
        <input name="prompt" placeholder="Describe an image..." required />
        <button type="submit">Generate Image</button>
    </form>
    <h3>{prompt}</h3>
    {'<img src="' + image_url + '"/>' if image_url else ''}
</body>
</html>
    '''

if __name__ == '__main__':
    app.run()
