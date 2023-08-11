## Chess Tournament Platform


## Description
The Chess Tournament Platform is a software  designed to manage chess tournaments.
It includes functionalities for creating and managing tournaments, rounds, matches, and players.

## Features
Tournaments Management: Create, update, and manage chess tournaments.
Rounds Handling: Manage different rounds within a tournament, including the start and end times.
Matches Generation: Automatically or manually generate matches between players, ensuring unique pairings.
Player Management: Maintain player information such as Chess ID, first name, last name, and scores.
Time Handling: Record and format the start and end times of rounds.
Data Serialization: Load and save tournament information through dictionaries, using classes like Round, and functions like to_dict() and from_dict().

Classes and Methods
Round
The Round class is responsible for handling individual rounds in a tournament. Some key methods include:

add_match(match): Adds a match to the current round.
get_match(match_id): Searches for a match with the provided match_id.
end_round(): Sets the end time for the current round.
to_dict(): Converts the current round object into a dictionary representation.
from_dict(source): A static method that creates a new Round object from a dictionary source.

### Coding Standards
The code adheres to PEP 8 conventions, ensuring readability and maintainability.

### Requirements
Python : **Python version 3.10.5**

## How to run this project
***

### -Open your terminal

### -Create a folder 

 'mkdir chess_platform'

### -Change directory

'cd chess_platform'

### -Install Virtual Environment:

 'pip install virtualenv'
 
#### -Create Virtual Environment
 'python3 -m venv env'
 
### -Activate Virtual Environment
'source env/bin/activate'

### -Clone the project by running the following command
'git clone https://github.com/Toufik-CHAARI/chess_platform.git'

### -Install the project dependencies 

'pip install -r requirements.txt'

### -run the code with the command
python3 main.py

### -follow the interface menu in order use the softwear
python3 main.py

***
## PEP8 Code compliance Report

## In order to generate each report, please use the following commands :

### flake8 --format=html --htmldir=flake-report_models models
### flake8 --format=html --htmldir=flake-report_views views  
### flake8 --format=html --htmldir=flake-report_controllers controllers
### flake8 --format=html --htmldir=flake-report_main main.py  

### display the report via the html file in the folder flake-report



