FROM tensorflow/tensorflow:latest-py3
WORKDIR /home/user
RUN apt-get update && apt-get install -y \
git \
python3 \
python3-pip \
sudo \
firefox \
wget
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz && \
tar -xzvf geckodriver-v0.23.0-linux64.tar.gz > /usr/bin/geckodriver && \
chmod 755 /usr/bin/geckodriver
RUN mkdir recaptcha-solver
COPY * /home/user/recaptcha-solver/
RUN cd /home/user/recaptcha-solver && python3 -m pip install -r requirements.txt
LABEL org.label-schema.name=recaptcha-solver
