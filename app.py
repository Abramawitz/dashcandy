from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Maintenance</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                background-color: #f5f7fa;
                color: #333;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                text-align: center;
            }
            h1 {
                font-size: 2em;
                margin-bottom: 0.5em;
            }
            p {
                font-size: 1.1em;
                color: #666;
            }
        </style>
    </head>
    <body>
        <h1>🚧 Under Maintenance</h1>
        <p>This site is temporarily paused while we update things behind the scenes.<br />
        Please check back soon.</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run()
