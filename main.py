from flask import Flask, render_template, request
from utils.github_api import fetch_repositories
from utils.preprocessing import preprocess_code
from utils.gpt import generate_gpt_response

app = Flask(__name__, template_folder = 'app/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the GitHub username from the form data
    username = request.form['username']

    try:
        # Fetch user repositories
        repositories = fetch_repositories(username)
        print(repositories)
        
        return render_template('result.html', repository=repositories['name'])

    except Exception as e:
        return render_template('error.html', error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
