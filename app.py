from flask import Flask, request
import openai
import os

app = Flask(__name__)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/', methods=['GET', 'POST'])
def home():
    image_url = ""
    user_input = ""
    display_prompt = ""

    if request.method == 'POST':
        user_input = request.form.get('prompt', 'A fantasy landscape')
        base_style = (
            "A flat-color cartoon illustration. Use a maximum of 6 solid colors. "
            "White background only. No gradients. Sharp, aliased edges. "
            "High contrast. Resolution: 512x512 pixels. "
        )

        prompt = base_style + user_input
        display_prompt = prompt

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
            display_prompt = f"Error: {str(e)}"

    return f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Slatelet Generator</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #f5f7fa;
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            padding: 20px;
            max-width: 100%;
        }}
        .content {{
            display: flex;
            flex-direction: column;
            gap: 40px;
        }}
        @media (min-width: 768px) {{
            .content {{
                flex-direction: row;
                align-items: flex-start;
            }}
        }}
        form {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
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
        .image-block {{
            max-width: 400px;
            text-align: center;
            position: relative;
        }}
        .image-block img {{
            width: 100%;
            max-height: 300px;
            object-fit: contain;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            opacity: 0;
            transition: opacity 0.5s ease-in;
        }}
        .image-block img.loaded {{
            opacity: 1;
        }}
        .download-btn {{
            display: inline-block;
            margin-top: 10px;
            background-color: #28a745;
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 14px;
        }}
        .download-btn:hover {{
            background-color: #1e7e34;
        }}
        .prompt-display {{
            font-size: 14px;
            color: #666;
            margin-top: 10px;
        }}
        .spinner {{
            display: none;
            margin-top: 20px;
            width: 40px;
            height: 40px;
            border: 4px solid #ccc;
            border-top-color: #007bff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Slatelet Generator</h1>
        <div class="content">
            <form method="POST" onsubmit="showSpinner()">
                <input name="prompt" placeholder="Describe an image..." required />
                <button type="submit">Generate Image</button>
                <div class="spinner" id="spinner"></div>
            </form>
            <div class="image-block">
                {'<img id="result-img" src="' + image_url + '" onload="onImageLoad()" />' if image_url else ''}
                {f'<a class="download-btn" href="{image_url}" download="generated-image.png">Download Image</a>' if image_url else ''}
                <div class="prompt-display">{display_prompt}</div>
            </div>
        </div>
    </div>
    <script>
        function showSpinner() {{
            document.getElementById('spinner').style.display = 'block';
        }}
        function onImageLoad() {{
            const img = document.getElementById('result-img');
            if (img) img.classList.add('loaded');
            document.getElementById('spinner').style.display = 'none';
        }}
    </script>
</body>
</html>
    '''

if __name__ == '__main__':
    app.run()
