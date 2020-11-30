# Game DB
#
A searchable games database with a game recommendation system.


## Setup Instructions

Install venv with: 
```
pip install virtualenv
```

Run the following commands in the project directory:

```
virtualenv venv

source venv/bin/activate
```

Now that you are in your virtual environment run the following command to install the dependencies:
```
pip install -r requirements.txt
```

With postgres installed and with a running postgresql database, run the following set of commands:
- ```createdb gamedb```
- ```psql gamedb < dbdump.sql```

~~Modify the database.py connection parameters for the db as you see fit.~~

After your tables are setup, create a ```.env``` file under ```/app``` with the following code:
```
DATABASE=gamedb
HOST=<optional depending on config, local database host>
PORT=<optional depending on config, local database port>
```

Use ```flask run``` while in the main folder to run the server. The server should be visable at http://localhost:5000/

When you are done with working on the project and want to escape out of the virtual environment, deactive venv by running:
```
deactivate
```

PostgreSQL database with a Flask server.
