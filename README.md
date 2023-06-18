# Mercor Project

a Python-based tool which, when given a GitHub user's URL, returns the most technically complex and challenging repository from that user's profile. The tool will use GPT and LangChain to assess each repository individually before determining the most technically challenging one.

## Backend Logic

--------------

The main logic of this backend is to send the code in 'chunks' and concatenate them with prompts. The prompts used are:

1. `'Provide me a score of code complexity out of 10 for the following code'` for each code file
2. `'Continued in next message...'` for each chunk of code

This approach allows for efficient processing and analysis of large code files, as the code can be broken down into manageable chunks and evaluated separately. The prompts also ensure that the model is aware of the context of each code chunk and can provide accurate feedback.


- `app/`: Contains the web application code.
  - `templates/`: Holds the HTML templates for the user interface.
  - `__init__.py`: Initializes the Flask application and defines routes.

- `data/`: Stores any data related to the project, such as preprocessed code files or cached API responses.

- `models/`: Contains custom models or utilities related to the project.

- `utils/`: Holds utility functions or modules used in the project.
  - `github_api.py`: Functions to interact with the GitHub API and fetch user repositories.
  - `preprocessing.py`: Functions for preprocessing code before passing it to GPT.
  - `gpt.py`: Functions for interacting with GPT and generating responses.
  - `__init__.py`: Initializes the `utils` module.

- `main.py`: The entry point of the application. Contains the main Flask application and routes for handling user requests.

- `requirements.txt`: Lists the dependencies required for the project. Include libraries like Flask, requests, etc.

- `README.md`: The documentation file explaining the project, its file structure, and instructions for running and deploying.

## Usage

To use this project, follow these steps:

1. Clone the repository: `git clone <repository_url>`
2. Install the dependencies: `pip install -r requirements.txt`
3. Configure the necessary API keys and settings in the appropriate files.
4. Run the application: `python main.py`
5. Access the tool in your browser at `http://localhost:5000` (or the specified port).

## Contributing

If you want to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
