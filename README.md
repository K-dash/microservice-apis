
# Python Project Template for Rye

This is a template that can be used generically for projects.
As a package management tool, Rye is used.

## Prerequisites
Before using this template, please ensure the following software is installed:

[Rye: Package management tool.](https://github.com/mitsuhiko/rye)
The following command allows you to install Rye:
```
curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash
echo 'source "$HOME/.rye/env"' >> ~/.bashrc
source "$HOME/.rye/env"
```

The following dependencies will be automatically installed using Rye:
- Python 3.10.x (latest)
- Python Libraries
  -   The installed libraries are listed in the requirements.lock file.

## Repository Initialization
After cloning this template repository, you will need to initialize your project repository to remove the template's .git directory and start with a fresh history.

Follow these steps:

1. Navigate to the root of your cloned repository.
2. Remove the existing .git directory:
```bash
rm -rf .git
```

3. Initialize a new Git repository:
```bash
git init
```

4. Add all files to the new repository:
```bash
git add .
```

5. Commit the files to start your project with a clean slate:
```baah
git commit -m "Initial commit."
```

6. Now, you can add your remote repository and push your changes:
```bash
# Replace <your-repository-URL> with the URL of your new GitHub repository.
git remote add origin <your-repository-URL>
git push -u origin main
```

## Usage
### Install the required packages.

```bash
make install
```

### To test the functionality, execute main.py.

```bash
make run_main
```

### Execute pre-commit

```bash
make pre-commit
```
