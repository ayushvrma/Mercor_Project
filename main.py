from flask import Flask, render_template, request
from utils.backend import fetch_repositories
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
        most_complex_repo, reason = fetch_repositories(username)
        print(most_complex_repo,reason)
        
        return render_template('result.html', repository=most_complex_repo, reason=reason)

    except Exception as e:
        return render_template('error.html', error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
