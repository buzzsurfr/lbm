# lbm
Load Balancing Manager

Language: Python  
Framework: Django

A simple aggregator of objects from load balancing instances (currently only F5).  Data is collected using [F5 iControl API](https://devcentral.f5.com/wiki/iControl.HomePage.ashx) with the [bigsuds](https://pypi.python.org/pypi/bigsuds/) python wrapper.

## Installation

1. Verify that you have a compatible version of Python and pip.
1. Clone the repository locally.
1. Install the requirements using pip (`pip install -r requirements.txt`)
1. (Optional) Create a super user for the admin site (`python manage.py createsuperuser`).  Alternatively, you can use `python createsuperuser.py` to create the default username/password (admin/lbm).
1. Create your database using `python manage.py migrate`.  By default, this will use SQLite3 with the database file located at db/db.sqlite3.
1. Start the webserver.
  * For development, simply use `python manage.py runserver`.
  * For production, you will want to serve the static files from a central folder.  You can collect them from the app using the `python manage.py collectstatic --no-input --clear`.  lbm has been tested with both apache and nginx/uWSGI.
