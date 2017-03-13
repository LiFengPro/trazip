# Trazip

## What is Trazip
Trazip is trying to simplify the way to plan a trip. Get rid of comparing hotels price, 
deciding which view you'd like to visit or fly tickets. Just tell us the budget and time, 
we will handle rest part of it.

## To developers
Docker-compose is the recommended tool to deploy and test the website. 

Prerequisites:
1. Install docker. Read more about docker installation 
* [for mac](https://docs.docker.com/docker-for-mac/install/)
* [for windows](https://docs.docker.com/docker-for-windows/install/)

2. Install docker-compose. Read more on [docker-compose installation](https://docs.docker.com/compose/install/)

Command to run, just

    # workdirs: /path/to/trazip
    # build and pull images
    docker-compose build
    # start services
    docker-compose up
    # stop services
    docker-compose down

    # execute command in container.
    docker ps | grep <image-name>   # to find out container id.
    docker exec -it <container-name> bash   # to open a shell of container.

Links:
1. Docker tutorial. [A popular videa about docker](https://www.youtube.com/watch?v=UV3cw4QLJLs)


