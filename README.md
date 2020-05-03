# Interactive Decision Trees

Build and maintain interactive troubleshooters and process flows with ZERO coding.

## Project Requirements:

In order to get the project running you need to install:

* docker

#### Install Docker:

Docker is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly.

[Get Docker](https://docs.docker.com/get-docker/).

## Setting the Project Locally:

#### Cloning the project:

Once you have all the needed requirements installed, clone the project:

``` bash
git clone git clone git@bitbucket.org:predict-a/treedecisioncreator-back.git
```

#### Configure .env file:

Before you can run the project you need to set the envirment varibles:

- .flaskenv
``` env
# Application env varibles
SECRET_KEY='\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

# JWT Config
JWT_SECRET_KEY='\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
#JWT_PUBLIC_KEY=~/jwt/jwt-key.pub
#JWT_PRIVATE_KEY=~/jwt/jwt

DATABASE_URL=bolt://host:password@db:7687

# Docker Env varibles
FLASK_APP=manage:application
FLASK_CONFIG=development
FLASK_DEBUG=1
```

- neo4jenv
``` env
NEO4J_ACCEPT_LICENSE_AGREEMENT=yes
...

```

#### Run the Project:

to run the project type:

``` bash
docker-compose up --build -d
```

Check 0.0.0.0:5000 on your browser!

That's it.
