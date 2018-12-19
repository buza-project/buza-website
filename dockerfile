
FROM python:3.6

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

RUN mkdir /buza-website

RUN apt-get update
RUN apt-get install apt-transport-https

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

RUN apt-get install -y python3-pip yarn &&\
	apt-get update

WORKDIR /buza-website

# Copy the current directory contents into the container
ADD . /buza-website

RUN pip install pipenv &&\
	# RUN yarn &&\
    cp -p .env.example .env  &&\
	pipenv install --system --deploy &&\
	pipenv run django-admin migrate
 EXPOSE 8000
