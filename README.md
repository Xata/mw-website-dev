# mw-website-dev

Welcome to the GitHub repository for my personal portfolio website! This repository contains all the necessary files to build and deploy my static portfolio website built with Pelican.

![GitHub top language](https://img.shields.io/github/languages/top/Xata/mw-website-dev?style=for-the-badge)
![GitHub Last Commit](https://img.shields.io/github/last-commit/Xata/mw-website-dev?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/Xata/mw-website-dev?style=for-the-badge)

## Overview

This portfolio website serves as a central hub for showcasing my projects, experience, and professional skills. Sections included are:

- Blog: Posts I have written. These include guides about technologies I use.
- Resume: Details about my professional experience, including roles and responsibilities.

### Project Info

The following was used to create the website:

[![Pelican](https://img.shields.io/static/v1?style=for-the-badge&message=pelican&color=14A0C4&logo=Pelican&logoColor=FFFFFF&label=)](https://github.com/getpelican/pelican)
[![pelican-plugins](https://img.shields.io/static/v1?style=for-the-badge&message=pelican-plugins&color=14A0C4&logo=GitHub&logoColor=FFFFFF&label=)](https://github.com/getpelican/pelican-plugins/tree/master)
[![pelican-themes](https://img.shields.io/static/v1?style=for-the-badge&message=pelican-themes&color=14A0C4&logo=GitHub&logoColor=FFFFFF&label=)](https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)](https://daringfireball.net/projects/markdown/)
![Github Pages](https://img.shields.io/badge/github%20pages-121013?style=for-the-badge&logo=github&logoColor=white)

### Setting up the project 

To run the website. Follow the steps below:

##### Windows 11
⚠️ On Windows 11 you may need to execute the following command first:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Now create a new virtual environment for Python:
```powershell
python -m venv .venv
```

Execute the following script to activate the virtual environment:
```powerhsell
.venv\Scripts\Activate.ps1
```

##### MacOS
Create a virtual environment for Python:
```zsh
python -m venv .venv
```

Activate the virtual environment:
```zsh
source .venv/bin/activate
```

#### Run the test website
Now navigate back to the root directory and run the following command:
```powershell
pip install -r requirements.txt
```

There you go! You should now be able to preview the project with Pelican by running this command:
```python
pelican content
pelican --listen
```


