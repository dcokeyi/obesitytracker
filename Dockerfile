FROM python:3.8-buster


RUN pip3 install --upgrade virtualenv && \
    virtualenv /env -p python3


## Setting these environment variables are the same as running
## source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

#remember to link it to the virtual env
ADD requirements.txt /Obesity/requirements.txt
RUN pip install -r  /Obesity/requirements.txt



# Add the application source code.
ADD . /Obesity
#Name the workdir that we need.
WORKDIR /Obesity

EXPOSE 8080

CMD gunicorn --bind 0.0.0.0:8080 wsgi:app
