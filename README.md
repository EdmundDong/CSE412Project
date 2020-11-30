# Game DB
#
A searchable games database with a game recommendation system. 
Built with PostgreSQL and Flask.


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
```
createdb gamedb
psql gamedb < gamedbdump.sql
```

After your tables are setup, create a ```.env``` file under ```app/``` with the following code:
```
DATABASE=gamedb
HOST=<optional depending on postgres config, local database host>
PORT=<optional depending on postgres config, local database port>
PASS=<optional depending on postgres config, local database password>
```

Run the command ```flask run``` while in the project root directory to start the server. The server should now be visible at http://localhost:5000/.

When you are done with working on the project and want to exit the virtual environment, deactive venv by running:
```
deactivate
```
