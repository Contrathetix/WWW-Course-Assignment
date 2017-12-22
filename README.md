# WWW-Course-Assignment

This is just a repository housing my submission for an assignment required for completing a www applications course. The contents herein are probably not of any special quality and definitely not of any interest to anyone. The application is a simple imageshare system with comments, and no one should obviously try to make any actual use of it whatsoever. Thank you.

Documentation in Finnish for the assignent (related to submission) located at `misc\dokumentaatio.pdf`.

## Requirements

The following are required for running the application:
* Python 3.6+
* Flask 0.12+ (the Python web microframework)
* Passlib 1.7.1+ (for password hashing and salting)
* web browser, developed with Firefox 58

## Running the Thing

There exists no virtualenv for Python, unfortunately, as I installed Flask for my user account. The following should be sufficient for running the application (replace `python` with ``python3` on linux (at least on Ubuntu) because python by default points at python2). For installing Flask and Passlib for the current user account, not system-wide:
```
python -m pip install --user flask passlib
```
For cloning the repository and entering it:
```
git clone https://github.com/Contrathetix/WWW-Course-Assignment
cd WWW-Course-Assignment
```
For running the application:
```
python .\app.py
```
The application should start at `http://localhost:8080/` if everything works (everything should work).
