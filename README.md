# Picture uploader

### Description
Application that allows manipulation with images. User can:
* download an image by name
* show metadata for the existing images by name
* upload an image
* delete an image by name
* get metadata for a random image

* subscribe an email for notifications and get a welcome message;
* unsubscribe an email from notifications;
* subscribed users get notifications about image uploading: 
    - an explanation that an image has been uploaded;
    - the image metadata (size, name, extension); 
    - a link to the web application endpoint for downloading the image


## TODO:
1. Add table (email + subscription_arn)
2. Remove get_settings() call
3. Credentials for AWS account !!!



#### Requirements

* [Docker](https://www.docker.com/) >= 18.06.0
* [Docker Compose](https://docs.docker.com/compose/install/) >= 1.23.0


#### Contribution Guide

You can find contribution guide [here](http://www.contribution-guide.org/).

Also you can read a very nice [guide about commit messages](https://m.habr.com/ru/post/416887/).

### How to run project in docker

```bash
# Build docker image
make build

# Run project => you can work with application at the http://127.0.0.1:8005/
make up

# Run logs
make logs

# Run migrations
make migrate
```

You can find more information about supportable command in the `Makefile`.


### How to work with project

1. Lock poetry dependencies:
    - Activate virtual env
    - Change `pyproject.toml` file
    - Generate `poetry.lock` file: ```poetry lock --no-update```
   
2. Run tests:
    - Run application tests using `make tests`
    - Check application test coverage using `make tests-coverage`

3. To run migrations use `make migrate` command

4. To enter inside containers use:
    - `make shell-app`
    - `make shell-db`

5. Linters:
    - `make lint` - run all linters checks:
        - `make format-check` - to check code formatting (black and isort)
        - `make flake8` - to check code formatting (flake8)
        - `make mypy-check` - to check code types using mypy
    - `make format` - to format code using black and isort
    
6. To load fixtures from `fixtures/` folder use: `make load-fixtures`

7. To check project source code metrics you can use [Radon](https://pypi.org/project/radon/): `make radon-check`

8. To check your tests quality you can use [mutmut](https://pypi.org/project/mutmut/): 
    - Enter `make mutmut-check`
    - You will get a report `mutmut-report.xml` 


## Environment variables

| name | type | required | default |
|------|------|----------|---------|
| IS_DEBUG | bool | false | false |
| POSTGRES_ALCHEMY_DRIVER | str | true | none |
| POSTGRES_HOST | str | true | none |
| POSTGRES_PORT | int | true | none |
| POSTGRES_WORK_DB | str | true | none |
| POSTGRES_WORK_USER | str | true | none |
| POSTGRES_WORK_USER_PASSWORD | str | true | none |
| SERVICE_LOGGER_LEVEL | int | false | 20 (logging.INFO) |
| PICTURE_UPLOADER_NUM_THREADS | int | false | 2 |
| PICTURE_UPLOADER_NUM_WORKERS | int | false | 2 |
| PICTURE_UPLOADER_PORT | int | false | 8000 |
| PICTURE_UPLOADER_RELOAD | bool | false | true |
