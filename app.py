from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prompt = request.form.get('prompt', 'No prompt provided')
        return f"<h1>You entered:</h1><p>{prompt}</p>"
    return '''
        <form method="POST">
            <input name="prompt" placeholder="Enter your prompt" />
            <button type="submit">Submit</button>
        </form>
    '''

if __name__ == '__main__':
    app.run()
