# kibanarec
A Tool to Extract Open Kibana Instances on Internet and Map them to their Corresponding Organizations for Bug Bounty.

## Installation
Requirements:
- Python3 
- Shodan API Key

Steps to install:
- Replace SHODANAPIKEY in .env file with your SHODAN API KEY.
- Run `pip3 install -r requirements.txt` to install dependencies.
- Run `python3 kibanarec.py -o file.txt` where `file.txt`is the output file.

## How it works?
The script gets the data from Shodan. It will output a file in comma-seperated format in which you will find *open* Kibana instances and their corresponding organizations based on SSL certificates.
