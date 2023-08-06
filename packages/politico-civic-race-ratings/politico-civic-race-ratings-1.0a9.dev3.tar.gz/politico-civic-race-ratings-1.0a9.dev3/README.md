![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# politico-civic-race-ratings

TK TK TK, the POLITICO way.


## Quickstart

1. Install the app.

  ```
  $ pip install politico-civic-race-ratings
  ```

2. Add the app to your Django project settings.

  ```python
  INSTALLED_APPS = [
      # ...
      'rest_framework',
      'entity',
      'geography',
      'election'
      'government',
      'raceratings',
  ]
  ```

3. Migrate the database.

  ```
  $ python manage.py migrate
  ```


## Developing

### Running a development server

Move into the example directory, install dependencies and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv install
  $ pipenv run python manage.py runserver
  ```

### Setting up a PostgreSQL database

1. Run the make command to setup a fresh database.

  ```
  $ make database
  ```

2. Make a copy of the `example/.env.example` file and save it as `example/.env`.

  ```
  $ cp example/.env.example example/.env
  ```

3. Add a connection URL to `example/.env`.

  ```
  DATABASE_URL="postgres://localhost:5432/raceratings"
  ```

4. Run migrations from the example app.

  ```
  $ cd example
  $ pipenv run python manage.py migrate
  ```


## Configuration

The below configuration is automatically read from a `.env` file in the project's root during local development. When in production, these variables are read from environment variables on the server.

More details about what each variable does will be added shortly.

| Variable name | What it does | Default value |
|:--|:--|:--|
| `RACE_RATINGS_AUTH_DECORATOR` | Description TK. | `'django.contrib.auth.decorators.login_required' |
| `RACE_RATINGS_SECRET_KEY` | Description TK. | `""` |
| `RACE_RATINGS_AWS_ACCESS_KEY_ID` | Description TK. | `None` |
| `RACE_RATINGS_AWS_SECRET_ACCESS_KEY` | Description TK. | `None` |
| `RACE_RATINGS_AWS_REGION` | Description TK. | `None` |
| `RACE_RATINGS_AWS_S3_BUCKET` | Description TK. | `None` |
| `RACE_RATINGS_CLOUDFRONT_ALTERNATE_DOMAIN` | Description TK. | `None` |
| `RACE_RATINGS_S3_UPLOAD_ROOT` | Description TK. | `uploads/raceratings` |
| `RACE_RATINGS_AWS_S3_STATIC_ROOT` | Description TK. | `"https://s3.amazonaws.com"` |


## Copyright

&copy; 2019&ndash;present POLITICO, LLC
