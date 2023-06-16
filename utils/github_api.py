import requests

def get_user_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repositories = response.json()
        return repositories
    else:
        raise Exception(f"Failed to fetch repositories. Status code: {response.status_code}")

