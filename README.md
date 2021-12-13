# Chat Application

This is a **QUIZ Application** which gives information about CSE core subjects. First of all, every student should register on the registration page by using his/her name, unique username,email and password. After registering, they need to login every time to access their account. Here we provide the different subjects in the dashboard .In the dashboard menu there are subjects in which we can select among some subjects and for every test it contains 20 questions and marks will be allotted for the right one.


## Tech

This project uses a number of open source projects to work properly:

- [HTML](https://html.com/) - HTML for frontend.
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) - CSS to beautify the frotend.
- [Flask](https://flask.palletsprojects.com/en/2.0.x/) - For API Creation and Backend Processing.
- [SQLite](https://www.sqlite.org/) - SQLite DB for storing data.


## Getting Started

To run the Application, install the required dependencies.

```sh
pip install -r requirements.txt
python app.py
```

Visit http://localhost:8000


## Database 

To log into the sqlite3 database, run this command.

```sh
sqlite3 quiz.db
```

List all the tables in the sqlite3.
```sh
.tables
```

To list all the entries of particluar table.
```sh
select * from <Table Name>;
```

#### Running the Application

To run the Flask Application, run the following command:

```sh
python app.py
```

And in this way, the Applciation will be up and running at:
```
http://localhost:8000
```