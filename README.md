# Trazip

## What is Trazip
Trazip is trying to simplify the way to plan a trip. Get rid of comparing hotels
 price, deciding which view you'd like to visit or fly tickets. Just tell us the
  budget and time, we will handle rest part of it.

## To developers
Docker-compose is the recommended tool to deploy and test the website. 

### Prerequisites
1. Install docker. Read more about docker installation 
* [for mac](https://docs.docker.com/docker-for-mac/install/)
* [for windows](https://docs.docker.com/docker-for-windows/install/)

2. Install docker-compose. 
Read more on [docker-compose installation](
    https://docs.docker.com/compose/install/)


### What will be deployed

1. A postgres database will be set up. If it is the very first time, a user
 will be created as POSTGRES_USERNAME/POSTGRES_PASSWORD. And a database will
  be created named as POSTGRES_DATABASE
2. The django website will be set up. The setup includes following steps.

    1. Migrating database changes.
    2. Creating superuser if it's the first time to run compose.
    3. Generating data to database if it's the first time to run compose.
    4. Running the website by gunicorn.
3. A nginx proxy will be set up and listen on port 8000.


### Command to run

    # workdirs: /path/to/trazip
    # build and pull images
    docker-compose build
    # start services
    docker-compose up
    # After logs like 'Listening at: http://0.0.0.0:80' shows, you should be 
    # able to access the site on http://localhost:8000
    # If you are using virtual marchine, then replace localhost with the ip 
    # of vm. (Please make sure the network setting is correct.)
    # Run docker-compose as deamon
    docker-compose up -d

    # stop services
    docker-compose down

    # execute command in container.
    docker ps | grep <image-name>   # to find out container id.
    docker exec -it <container-name> bash   # to open a shell of container.
    # check logs for container
    docker logs -f <container-id>

## Links:
1. Docker tutorial. [A popular videa about docker](
    https://www.youtube.com/watch?v=UV3cw4QLJLs)


