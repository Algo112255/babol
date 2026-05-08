from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

oauth = OAuth(app)

github = oauth.register(
    name='github',

    client_id='Ov23li2ANP84LLLdtYp4',

    client_secret='7b93112886f78edce47cbb4d97848bde7e8bd6a7',

    access_token_url='https://github.com/login/oauth/access_token',

    authorize_url='https://github.com/login/oauth/authorize',

    api_base_url='https://api.github.com/',

    client_kwargs={
        'scope': 'user:email',
    },
)

@app.route('/')
def home():
    return '''
    <h1>GitHub OAuth Login</h1>

    <a href="/login">Login with GitHub</a>
    '''

@app.route('/login')
def login():

    return github.authorize_redirect(
        url_for('callback', _external=True)
    )

@app.route('/callback')
def callback():

    token = github.authorize_access_token()

    user = github.get('user').json()

    session['user'] = user

    return redirect('/profile')

@app.route('/profile')
def profile():

    if 'user' not in session:
        return "Unauthorized", 401

    return jsonify(session['user'])

@app.route('/api/secure-data')
def secure_data():

    if 'user' not in session:
        return jsonify({
            "error": "Unauthorized access"
        }), 401

    return jsonify({
        "message": "This is protected API data",
        "username": session['user']['login']
    })

@app.route('/logout')
def logout():

    session.pop('user', None)

    return '''
    <h2>Logged out successfully</h2>

    <a href="/profile">Try Accessing Profile Again</a>
    '''

if __name__ == '__main__':

    app.run(
        debug=True,
        use_reloader=False
    )