from flask import Flask, render_template, request
from utils.github_api import get_user_repositories
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
        repositories = get_user_repositories(username)
        
        # Initialize variables to track the most complex repository
        most_complex_repo = None
        max_complexity_score = float('-inf')

        for repo in repositories:
            # Preprocess code
            preprocessed_code = preprocess_code(repo['code'])
            
            # Generate GPT response
            prompt = f"Based on code complexity, how challenging is the {repo['name']} repository?"
            gpt_response = generate_gpt_response(prompt)
            
            # Calculate complexity score (example: based on length of GPT response)
            complexity_score = len(gpt_response)
            
            # Update most complex repository if applicable
            if complexity_score > max_complexity_score:
                max_complexity_score = complexity_score
                most_complex_repo = repo

        return render_template('result.html', repository=most_complex_repo, gpt_response=gpt_response)

    except Exception as e:
        return render_template('error.html', error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
