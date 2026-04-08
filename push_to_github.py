import sys
import subprocess
import urllib.request
import urllib.error
import json
import os

token = "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"
repo_name = "mundokids"

def make_request(url, method="GET", data=None):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Python/3.x"
    }
    encoded_data = None
    if data:
        encoded_data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
        
    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.read().decode()}")
        sys.exit(1)

print("Fetching username...")
user_data = make_request("https://api.github.com/user")
username = user_data["login"]
print(f"Authenticated as {username}")

print("Creating repository on GitHub...")
try:
    make_request("https://api.github.com/user/repos", method="POST", data={
        "name": repo_name,
        "private": True,
        "description": "Website Mundo Kids (Cloned)"
    })
    print(f"Repository {repo_name} created successfully.")
except SystemExit:
    print("Repo might already exist, continuing anyway...")

# Setup Git
def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=True)

os.environ["GIT_AUTHOR_NAME"] = "Eduardo"
os.environ["GIT_AUTHOR_EMAIL"] = "eduardo@example.com"
os.environ["GIT_COMMITTER_NAME"] = "Eduardo"
os.environ["GIT_COMMITTER_EMAIL"] = "eduardo@example.com"

# git init & commit
try:
    run_cmd("git init")
    run_cmd("git branch -M main || git switch -c main")
    run_cmd(f"git remote rm origin 2>/dev/null || true")
    run_cmd(f"git remote add origin https://{username}:{token}@github.com/{username}/{repo_name}.git")
    run_cmd("git add .")
    run_cmd('git commit -m "Initial commit"')
    print("Pushing to GitHub...")
    run_cmd("git push -u origin main")
    print(f"Success! URL: https://github.com/{username}/{repo_name}")
except subprocess.CalledProcessError as e:
    print(f"Git command failed: {e}")
