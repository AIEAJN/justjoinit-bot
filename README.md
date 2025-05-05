# JustJoinIT Bot

A Python bot that automates job searching and application process on justjoin.it. The bot uses Selenium to navigate the website and can automatically apply to jobs based on location and position criteria.

## Features

- Search jobs by location and position
- Automated job application process 
- Saves application history to CSV file
- User-friendly GUI interface built with Qt

## Prerequisites

- Python 3.8+
- Poetry package manager

## Installation
1. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install the dependencies:
   ```bash
   poetry install
   ```

3. Configure Python environment:
   ```bash 
   poetry env use python3.13
   ```

4. Activate the virtual environment:
   ```bash
   poetry shell
   ```
5. Execute the app.py file