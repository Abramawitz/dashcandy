from flask import Flask, request
import openai
import os

app = Flask(__name__)

# Load OpenAI client using environment variable
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/', methods=['GET', 'POST'])
def home():
    image_url = ""
    user_input = ""
    display_prompt = ""

    if request.method == 'POST':
        user_input = request.form.get('prompt', 'A fantasy landscape')

        # Inject brand-style prompt prefix
        base_style = (
            "A flat-color cartoon illustration. Use a maximum of 6 solid colors. "
            "White background only. No gradients. Sharp, aliased edges. "
            "High contrast. Resolution: 512x512 pixels. "
            "All colors must be directly touching another color" 
            "the image must be overlaid on a shape (polygon or circle)"
            
        )

        prompt = base_style + user_input
        display_prompt = user_input  # For displaying on the page

        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",  # Required, but DALL·E 3 will generate based on model defaults
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
        .prompt-display {{
            max-width: 600px;
            margin-top: 20px;
            font-size: 14px;
            color: #666;
            text-align: center;
        }}
    </style>
</head>
<body>
    <h1>AI Slatelet Generator</h1>
    <form method="POST">
        <input name="prompt" placeholder="Describe an image..." required />
        <button type="submit">Generate Image</button>
    </form>
    <div class="prompt-display">{display_prompt}</div>
    {'<img src="' + image_url + '"/>' if image_url else ''}
</body>
</html>
    '''

if __name__ == '__main__':
    app.run()
