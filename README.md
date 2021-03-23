# Inter IIT Tech Meet Traffic Sign Recognition

Repo for code written for Bosch's Traffic Sign Recognition problem statement at Inter IIT Tech Meet 2020.

## Summary

  - [Getting Started](#getting-started)
  - [Authors](#authors)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)

## Getting Started

These instructions will get you a copy of the project up and running on
your local machine for development and testing purposes.

### Prerequisites

**Use black for formatting Python code and prettier (with config in web folder) before committing. If you are on Ubuntu (or any Linux) and follow the instructions given below, they should run automatically with every commit.**

Setup Python:
```sh
sudo apt install python3-virtualenv python3.8-venv python3-dev python3.8-dev python3-pip
sudo apt install libgl1-mesa-glx
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx completions
source ~/.zshrc
pipx completions
pipx install poetry
pipx install black
pipx install isort
pipx install flake8
```

Setup Node:
```sh
# First two lines install nvm and then node using nvm
# Feel free to skip if you have node installed
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
nvm install --lts
npm i -g prettier
```

You'll have to add the following to your .bashrc if you use nvm:
```
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
```

Setup Git hooks:
```sh
git config --local include.path ../.gitconfig
# git hooks will help with formatting and all
```

For mongo, follow instructions on Mongo website.

[REM] Remove hardcoded domain names for Auth0 from both web and server ends

### Installing

## Authors

## License

## Acknowledgments
- [Automold](https://github.com/UjjwalSaxena/Automold--Road-Augmentation-Library)
