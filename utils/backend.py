import re
import requests
from config import skip_files_extensions, skip_files_patterns, proper_file_names
import nbconvert
import tiktoken

from utils.gpt import generate_gpt_response

def fetch_repositories(username):
    # Make the API request to fetch repositories
    response = requests.get(f'https://api.github.com/users/{username}/repos')
    repositories = response.json()

    # Determine the most technically challenging repository
    most_complex_repo = None
    max_complexity = 0

    for repo in repositories:
        repo_name = repo['name']

        # Fetch files for the repository
        files_url = f"https://api.github.com/repos/{username}/{repo_name}/contents"
        files_response = requests.get(files_url)
        files = files_response.json()

        # Initialize variables for calculating average score
        total_score = 0
        num_chunks = 0
        reason = ''

        # Process each file and calculate score
        for file in files:
            file_path = file['path']
            file_name = file['name']
            print(file_path,'\n', file_name)

            # Exclude certain file types or directories if needed
            if file_name in proper_file_names or file_path.endswith(tuple(skip_files_extensions)) or any(file_path.startswith(pattern) for pattern in skip_files_patterns):
                print(file_name, 'being skipped')
                continue

            # Get the download URL
            download_url = file['download_url']
            print(download_url)
            try:
                code_response = requests.get(download_url)
                code_content = code_response.content.decode('utf-8')
                print(code_content)
            except requests.exceptions.RequestException:
                continue

            # Preprocess code into chunks
            code_chunks = preprocess_code(download_url)

            # Calculate score for each chunk
            for chunk in code_chunks:
                score, reason = generate_gpt_response(chunk)

                # Accumulate score and increment chunk count
                total_score += score
                num_chunks += 1

        # Calculate average score for the repository
        if num_chunks > 0:
            avg_score = total_score / num_chunks
        else:
            avg_score = 0

        # Update the most complex repository if necessary
        if avg_score > max_complexity:
            max_complexity = avg_score
            most_complex_repo = repo_name
            most_complex_reason = reason

    return most_complex_repo, reason


def preprocess_code(file_url, max_chunk_length=4096):
    # Make the API request to fetch the code from the file URL
    response = requests.get(file_url)
    file_content = response.text
    # Remove comments
    code = re.sub(r"#.*", "", code)
    
    # Remove blank lines
    code = "\n".join(line for line in code.splitlines() if line.strip())
    
    # Check if the file is a Jupyter notebook
    if file_url.endswith('.ipynb'):
        # Convert Jupyter notebook to Python code using nbconvert
        python_code = nbconvert.PythonExporter().from_notebook_node(nbconvert.reads(file_content, nbconvert.NO_CONVERT)).strip()
        code = python_code['code']
    else:
        code = file_content

    # Split the code into chunks
    chunks = []
    current_chunk = ''
    lines = code.splitlines()
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')

    for line in encoding:
        # Check if adding the line to the current chunk exceeds the maximum length
        if len(current_chunk) + len(line) + 2 <= max_chunk_length:  # Adding 2 for prompt lines
            current_chunk += line + '\n'
        else:
            # If the current chunk is not empty, add it to the list of chunks
            if current_chunk:
                chunk_with_prompt = encoding.encode(f'You are a code complexity analyser, you will go through the 1 file in piece of code chunks and analyse their complexity and provide me with a score out of 10, it can be upto 2 decimal places. i will provide you code chunks in multiple messages with "CONTINUED IN NEXT MESSAGE" written on end of 1 chunk with "END OF FILE" written when the file is completed. you will then start your analysis on the code and provide me with a score, reason. Say "lets start ayush" to get started\n{current_chunk.strip()}\nCONTINUED IN NEXT MESSAGE...\n')
                chunks.append(chunk_with_prompt)
            current_chunk = line + '\n'

    # Add the last chunk to the list if it's not empty
    if current_chunk:
        chunk_with_prompt = f'{current_chunk.strip()}\n \END OF FILE\n'
        chunks.append(chunk_with_prompt)

    # Prepend the file name to each chunk
    file_name = file_url.split('/')[-1]
    chunks = [f'File Name: {file_name}\n{chunk}' for chunk in chunks]

    return chunks
