## Aladin Test

### Quick Start

Open your terminal and then make virtual env for Python 3.x:

```
$ python -m venv .venv
$ source .venv/bin/activate
```

Install requirements:

```
$ pip install -r requirements.txt
```

Setup database with Postgre or SQLite. Open file `aladin/settings.py` and change `name`, `user` and `password`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
    }
}
```

If you only SQLite (just for test), you can change `DATABASE` like this:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}
```

Back to terminal and migrate:

```
$ python manage.py migrate
```

Create superuser:

``` 
$ python manage.py createsuperuser
```

Create product fake:

```
$ python manage.py generate_products 100000000
```

Run server:

```
$ python manage.py runserver
```

Open `http://localhost:8000/`.

If you want to access admin site, open `http://localhost:8000/admin/`.



