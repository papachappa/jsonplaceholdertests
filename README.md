There are PyTest tests to check https://jsonplaceholder.typicode.com/ REST API fake data.

How to execute tests locally in Ubuntu 16.04/MacOS 10.13:

- install python3 (sudo apt-get update; sudo apt-get -y upgrade)
- install pip3 (sudo apt-get install -y python3-pip)
- install python3 virtualenv (sudo apt-get install -y python3-venv)
- mkdir ~/jsontests && cd ~/jsontests
- git clone https://github.com/papachappa/jsonplaceholdertests.git .
- create virtualenv (python3 -m venv venv)
- activate virtualenv (source venv/bin/activate)
- install dependencies (pip3 install -r requirements.txt)
- run PyTest tests from ~/jsontests (pytest -vv .)
