# flask-rest-boilerplate

##Setup
Instll packages:
```sh
$ pip install -r requirements.txt
```

##Configuration
### Config file
Path to the config file stores in environment variable "FLASK_REST_BOILERPLATE_SETTINGS"

```sh
$ export FLASK_REST_BOILERPLATE_SETTINGS =/path_to_project/flask-rest-boilerplate/settings/developers_name.py
```

Sample with export env variable using postactivate script:
```sh
$ cat ~/.Envs/pdl/bin/postactivate
#!/bin/zsh

export FLASK_REST_BOILERPLATE_SETTINGS=/path_to_project/flask-rest-boilerplate/settings/developers_name.py
cd /path_to_project/
```

###Database
Creating database and user in PostgreSQL:
```sh
CREATE DATABASE db_name;
CREATE USER user_name WITH password ‘password‘;
GRANT ALL ON DATABASE db_name TO user_name;
```

###Database migrations
For migrations ise alembic with flask-migrate  
Link to documentation - flask-migrate.readthedocs.org

Run migration
```sh
$ python app.py db upgrade
```

Creating migration's file(run only after creating new models or changing old)
```sh
$ python app.py db migrate
```

### Run dev server
```sh
$ python app.py runserver
```

##Создание кастомных команд
##Creating custom commands
http://flask-script.readthedocs.org  
Current custom commands:  
```sh
$ python app.py add_user
$ python app.py change_expire_user
$ python app.py change_password
```


##Debug using konch
Run konch console:
```sh
$ konch
```

https://github.com/sloria/konch
