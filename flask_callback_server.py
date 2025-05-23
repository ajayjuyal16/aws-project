from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    oauth_verifier = request.args.get('oauth_verifier')
    if oauth_verifier:
        return f'Verifier (PIN) received: {oauth_verifier}<br>You can now close this page.'
    else:
        return 'No verifier received.'

if __name__ == '__main__':
    app.run(port=8080)
