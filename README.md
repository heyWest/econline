# Project Name
> EC Online

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
<!-- * [License](#license) -->


## General Information
- EC Online is a web application that helps students create elections and vote online.
- It offers a free and safe way to vote online with ease for students.


## Technologies Used
- Python - version 3.7
- Flask - version 1.1.2


## Features
List the ready features here:
- Create and Monitor Elections
- Verification of Voter Details
- Secure Online Voting


## Setup
Install libraries

`pip install -r requirements.txt`

Initialize Database
` python run.py shell  `

` db.create_all() `

` exit() `



Add/Edit Environment Variables

Make and update migrations

` python run.py db stamp 7d52952abb12`

` python run.py db migrate `

` python run.py db upgrade `



## Usage
Start the application

`python run.py runserver`


## Project Status
Project is:  _complete_ 


## Room for Improvement

Room for improvement:
- Making custom ballots
- Making the ballot dynamic
- Improving the voting page
- General UI Improvement

To do:
- Custom and Dynamic Ballots


## Acknowledgements
Give credit here.
- This project was inspired by Miss Sena Gohoho-Apawu.
- Many thanks to GOD, Stackoverflow, Google and all my colleagues who helped out.


## Contact
- Created by [@averagewifisuer]
- Twitter: @joe_a_jnr
- Email: jjnracheampong@gmail.com

Feel free to contact me!


<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->
