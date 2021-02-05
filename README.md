# solution-challenge-backend
## Getting Started
### requirements
- git 1.8+
- Python 3.9.0

### Set up a Development Environment & Run Server
#### method1: Docker

`docker-compose -f docker-compose-dev.yaml up`

#### method2: Python - Built-in `venv`

Create your virtual environment:

`python3 -m venv venv`

And enable it:

`. venv/bin/activate`

### Install Dependencies

Use pip to install Python depedencies:

`pip install -r requirements.txt`


### Set up Local Environment Variables for Database

Settings are stored in environment variables via [django-environ](http://django-environ.readthedocs.org/en/latest/). The quickest way to start is to copy `local.sample.env` into `local.env`:

`cp src/backend/settings/local.sample.env src/backend/settings/local.env`

Default is sqlite3, you can change to connect `postgres`. Copy `local.sample.env` and change its parameters to your personal setting.
Then edit the `SECRET_KEY` line in `local.env`, replacing `{{ secret_key }}` into any [Django Secret Key](http://www.miniwebtool.com/django-secret-key-generator/) value. An example:

`SECRET_KEY=6lnjp^hc=k_v!xm$bl9wdn0=+r@u(2@l+4_4!c0cdzg$^8ydlw`


### Get Ready for Development

`cd` into the `src` directory:

`cd src`

#### Migrate the database:

`python manage.py migrate`

#### Create Super User

`python manage.py createsuperuser`

#### Compile localized translation

`python manage.py compilemessages`

Now you’re all set!

## Run the Development Server

`python manage.py runserver`
