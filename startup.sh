#install virtualenv if not installed
sudo pip install virtualenv

#setup venv
virtualenv venv
source venv/bin/activate

#install python packages
pip install -r requirements.txt

#start the server
nohup python runserver.py &

#install node if not already present
brew install node

#start node server for front end
cd ./frontend/spidy
nohup node app.js &

