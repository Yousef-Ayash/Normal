# Normal

## Description

A web app inspired by Medium.com and Dev.to made with `Django` for users to write blogs/posts about a lot of topics and features.

## Features

-   Users:
    -   A user has a profile where anyone can go to the user's profile and see all of their posts.
    -   Write posts.
    -   Edit posts.
    -   Delete posts.
    -   Like posts.
    -   Comment on posts.
-   Posts:
    -   A post has a publisher, topic, comments and likes.
    -   The publisher can `Edit` their post and `Delete` their post and no one can do that other than the publisher.
    -   The post can be `Published` or be `Saved as a draft`.
    -   A drafted post cannot be viewed by other users than the publisher.

## Installation and Cloning

1. First of all, clone this repository to your machine.
2. Create a Virtual Environment.

    ```
    python -m venv env

    # If you have the virtualenv package
    virtualenv env
    ```

    or you can swap `env` to whatever you want.

3. Activate the created virtual environment in terminal with this command:

    ```
    # Windows
    env\scripts\activate

    # Linux/MacOS
    source env/bin/activate
    ```

4. Run the following command to download all the packages that are involved in the development of **`Normal`**
    ```
    pip install -r requirements.txt
    ```
5. To run the server just type:
    ```
    python manage.py runserver
    ```
6. Enjoy the **`Normal`** project.

## Running Normal in Production mode

The steps above are to clone the repo and use `Normal` in **`Debug`** mode, now if you want to try `Normal` in production just follow the steps below:

1. Create a `.env` file in the root of the project.
2. Add the following fields in the `.env` file:

    ```
    DEBUG=0

    # Change the values inside the <> according to what you have in your machine
    # that if you have postgresql in your machine.
    # if not, just don't type it and just use the sqlite db.
    DATABASE_URL=postgres://<db_username>:<db_password>@<db_hostname>:<db_port>/<db_name>
    ```

3. To run the server you have multiple options:
    1. The standard way:
        ```
        python manage.py runserver
        ```
    2. GUnicorn:
        ```
        # If you are running in a windows machine, use the 3th option.
        gunicorn Normal.wsgi:application
        ```
        > You installed `gunicorn` when you ran `pip install -r requirements.txt`
    3. Waitress:
        ```
        waitress-serve --listen=*:8000 Normal.wsgi:application
        ```
        To use `waitress` you need to install it with the following command:
        ```
        pip install waitress
        ```
4. Enjoy the **`Normal`** project in **`Production`** mode.

## Tweaking the project to your need

You have all the rights to clone, tweak, change, deploy and study this repo to your heart's content.

## Final notes

-   [Normal](https://normal-kjbk.onrender.com/) is live if you want to try it out without cloning it and do all the above things.
    that is if you tried it before **_8/8/2023_**.
-   If you want to connect with me... this is my [LinkedIn Profile](https://www.linkedin.com/in/yousefayash65/).
-   If you have any feedback or issues for the project, I hope to hear them out. Thank You!😃
