FROM python:3.13

RUN apt-get -qq -y update && apt-get -qq -y upgrade
RUN pip install pip-tools

COPY requirements.txt /bodsld/
WORKDIR /bodsld/
RUN pip install -r requirements.txt

CMD ["/bin/bash"]