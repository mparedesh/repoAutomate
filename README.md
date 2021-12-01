# Github Reports Generator
This repository contents the code to generate reports from Github:
- Repositories
    - repos.py
- Teams
    - teams.py
- Users
    - users.py


# Settings

To configurate the scripts it's necessary to set the next variables, in config.py file:

| Name | Description | Where |
| --------------- | --------------- |
| ORG | Name of the organization to be consulted |
| API_TOKEN | Github API token with read permissions |
 

# Pre-requisites required version

- Python 3
- pip install openpyxl
- pip install request
- pip install boto3


## Highlights

When you authenticate through the API TOKEN you can execute 5.000 request per hour; the script validate and shows remaining request until reach the limit, then delays the next requests.


# Run scripts

- python users.py
- python repos.py
- python teams.py
