import os
from git import Repo, GitCommandError
import time

def push_file_to_git_branch(file_name, remote_url_with_token, base_branch='main'):
    try:
        # Get the absolute path of the file
        file_path = os.path.abspath(file_name)
        print(file_path)

        # Get the directory of the file
        repo_directory = os.path.dirname(file_path)

        # Initialize a new Git repository in the same directory as the file
        repo = Repo.init(repo_directory)

        # Check if the base branch already exists
        base_branch_exists = False
        for branch in repo.branches:
            if branch.name == base_branch:
                base_branch_exists = True
                break

        # If the base branch doesn't exist, create it
        if not base_branch_exists:
            repo.create_head(base_branch)
            repo.heads[base_branch].checkout()

        # Generate a unique branch name based on the current timestamp
        timestamp = int(time.time())
        branch_name = f"{base_branch}_branch_{timestamp}"

        # Check if the branch already exists
        branch_exists = False
        for branch in repo.branches:
            if branch.name == branch_name:
                branch_exists = True
                break

        # If the branch exists, switch to it
        if branch_exists:
            repo.heads[branch_name].checkout()
        else:
            # Create a new branch
            new_branch = repo.create_head(branch_name)
            new_branch.checkout()

            # Copy the file to the repository
            repo.git.add(file_path)

            # Commit the changes
            repo.index.commit(f"Initial commit for {file_path}")

            # Check if the remote 'origin' already exists
            origin_remote = None
            for remote in repo.remotes:
                if remote.name == 'origin':
                    origin_remote = remote
                    break

            # If 'origin' doesn't exist, create it
            if not origin_remote:
                repo.create_remote('origin', remote_url_with_token)
            else:
                # Update the remote URL
                origin_remote.set_url(remote_url_with_token)

            # Push the changes to the remote repository
            origin_remote = repo.remote('origin')
            origin_remote.push(branch_name)

            print(f"File '{file_path}' pushed to the Git branch '{branch_name}' at {remote_url_with_token}.")

    except GitCommandError as e:
        print(f"Error: {e}")
# # Example usage:
# file_path = "/path/to/your/file.txt"
# # Replace 'your_access_token' and 'your_username/your_repository.git' with your GitHub access token and repository
# remote_url_with_token = "https://your_access_token@github.com/your_username/your_repository.git"

# create_git_branch_and_push_with_token(file_path, remote_url_with_token)
