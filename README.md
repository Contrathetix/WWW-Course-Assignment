## WebApplicationsCourseProject

This is just a repository housing my submission for an assignment required for completing a web applications course. The contents herein are probably not of any special quality and definitely not of any interest to anyone. The application is a simple imageshare system with comments, and no one should obviously try to make any actual use of it whatsoever. Thank you.

### Requirements

The following are required for running the application:
* Python 3.6+
* Flask 0.12+ (the Python web microframework)
* Passlib 1.7.1+ (for password hashing and salting)
* web browser, developed with Firefox 58

### Running the Thing

There exists no virtualenv for Python, unfortunately, as I installed Flask for my user account. The following should be sufficient for running the application. For installing Flask and Passlib for the current user account, not system-wide:

    python -m pip install --user flask passlib

For cloning the repository and entering it:

    git clone https://github.com/Contrathetix/WebApplicationsCourseProject
    cd WebApplicationsCourseProject

For running the application:

    python3 .\app.py

The application should start at `http://localhost:8080/` if everything works (everything should work).
