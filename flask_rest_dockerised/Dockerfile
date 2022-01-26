# this is an official Python runtime, used as the parent image
FROM python:3.9.1

# set the working directory in the container to /api
WORKDIR /api

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /api/requirements.txt

# add the current directory to the container as /api
ADD . /api

# execute everyone's favorite pip command, pip install -r
RUN pip install -r requirements.txt

# unblock port 80 for the Flask app to run on
EXPOSE 5000

# execute the Flask app
ENTRYPOINT ["python"]
CMD ["app.py"]