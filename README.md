# Django Newspaper

Website that allows to read posts/news from different users, uses server site rendering with Django to show the news and you as an user (with an account) can add new articles and comment to the different news.

The project has:

* UI in many templates
* Many routes rendered in backend
* Models a CustomUsers, NewsPost and their comments
* User Account management
* CRUD operations in models after metioned
* Pagination in Newspaper and Comments Sections

## Local Development

Follow every command below to put it running in your machine

1. Setting Repository

    ```CMD
    git clone https://github.com/Rvjonh/django_news.git     # clone the repository in the actual dir
    py -m venv .venv    # creates a python environment
    .venv\Scripts\activate.bat  # activate the environment
    pip install -r requirements. txt     # install dependencies for the project (ej. django)
    ```

2. Configure your local variables (Windows)

    ```.ENV
    copy .env-copy .env     # Make a copy of the file
    You need to fill all the variables ...
    ```

3. Start the development server

    ```CMD
    py manage.py makemigrations
    py manage.py migrate
    py manage.py runserver
    ```

4. Visit your server website url for development (Example)

    ```CMD
    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    January 25, 2023 - 20:35:32
    Django version 4.1.5, using settings 'django_project.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.
    ```

## Generate Secrect Key

> To create a new Secreat Key for django.settings

```Python
python -c "import secrets; print(secrets.token_urlsafe())"
```
