# Mercor Project

A Python-based tool which, when given a GitHub user's URL, returns the most technically complex and challenging repository from that user's profile. The tool will use GPT and LangChain to assess each repository individually before determining the most technically challenging one.

## Backend Logic

--------------

The main logic of this backend is to send the code in 'chunks' and concatenate them with prompts. The initial prompt used is:

`You are a code complexity analyser, you will go through the 1 file in piece of code chunks and analyse their complexity and provide me with a score out of 10, it can be upto 2 decimal places in the first line of your response. i will provide you code chunks in multiple messages with "CONTINUED IN NEXT MESSAGE" written on end of 1 chunk with "END OF FILE" written when the file is completed. you will then start your analysis on the code and provide me with a score, reason. Say "lets start ayush" to get started`

This approach allows for efficient processing and analysis of large code files, as the code can be broken down into manageable chunks and evaluated separately. The prompts also ensure that the model is aware of the context of each code chunk and can provide accurate feedback.


- `app/`: Contains the web application code.
  - `templates/`: Holds the HTML templates for the user interface.
  - `__init__.py`: Initializes the Flask application and defines routes.


- `utils/`: Holds utility functions or modules used in the project.
  - `backend.py`: For getting API data from Github, Preprocessing and returning most complex repository with reason
  - `gpt.py`: Functions for interacting with GPT and generating score and reason.

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

## License

This project is licensed under the [MIT License](LICENSE).
