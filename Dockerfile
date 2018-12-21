
FROM python:3.6

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

RUN mkdir /buza-website

RUN apt-get update &&\
    apt-get install apt-transport-https &&\
	curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - &&\
    echo "deb https://dl.yarnpkg.com/debian/ stable main" >/etc/apt/sources.list.d/yarn.list &&\
    apt-get install -y python3-pip yarn


WORKDIR /buza-website

# Copy the current directory contents into the container
COPY . /buza-website

RUN pip install pipenv &&\
	yarn &&\
    cp -p .env.example .env  &&\
	pipenv install --system --deploy &&\
	pipenv run django-admin migrate
 EXPOSE 8000
