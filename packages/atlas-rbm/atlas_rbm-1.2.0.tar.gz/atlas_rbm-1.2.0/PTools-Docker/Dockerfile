# Use the Ubuntu Xenial (16.04) image as parent image
FROM ubuntu:xenial

# set shell
RUN export SHELL=/bin/bash

# Update
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get update
RUN apt-get install -y dialog apt-utils
RUN apt-get upgrade -y
RUN apt-get install -y htop inetutils-ping libxml2-dev libssl-dev libxpm-dev libxm4 python3

# Initiate the pathway tools server at runtime
CMD /opt/pathway-tools-22/pathway-tools -config && /opt/pathway-tools-22/pathway-tools -lisp -python-local-only
