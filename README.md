# Social Network

## Introduction
**Social Network** is the API of an application where users can share posts and like/unlike posts by other users. For testing purposes, the project is structured using microservices architecture.

## Key Application features  
* Users can create account and log in
* Authenticated users can view posts
* Authenticated users can edit and delete posts they submitted
* Authenticated users can view a list of posts
* Authenticated user can log out
* Authenticated user can like and unlike posts

## Technologies and tools used
* <a href = "https://www.djangoproject.com/">Django: </a>A Python framework for web development
* <a href ="https://www.django-rest-framework.org/">Django REST Framework: </a> A Python framework for quick and clean creation of RESTful APIs
* <a href ="https://docs.docker.com/">Docker: </a>A container-based virtualization technology
* <a href ="https://requests.readthedocs.io/">Requests: </a>A Python package for making HTTP calls.

## Installing the application 
* Install Python3 on your system
* Set up Docker and Docker-compose on your system
* Clone the application to your local system
```Sh
> $ `git clone https://github.com/Victoradukwu/SocialNetwork.git`
```
* Change the directory on your local system
```Sh
> $ `cd SocialNetwork`
```
* Install all dependencies--to enable testing on the local hosts
```Sh
> $ `pip install -r requirements.txt`
```
* create a .env file at your project root and populate t with the content of `sample.env` file.

* Activate the virtual environment and run migrations

```Sh
> $ `source ./venv/bin/activate `
> $ `python manage.py migrate`
```
* Start the application
```sh
> $ python manage.py runserver
> $ python bot/main.py  
```
## Testing in a docker environment
* Create a `.env.docker` file in the project root directory and populate it with the appropriate values of the content of `sample.env`
* Spin up the Docker containers, using docker-compose and test the endpoints

```sh
> $ docker-compose up
```

## The Bot Component
* The bot component is used to automate the API testing.
* To use it, the Discord channel link is needed(contact the author or this project)
* Log into the Discord channel and send a message to test the API
* Send the message `$social`

## Automated Code Testing
* Run Test `$ pytest`
