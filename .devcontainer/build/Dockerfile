FROM registry.access.redhat.com/ubi9/python-39:latest

# Install oh-my-zsh
USER root
RUN yum install -y yum-utils && \
    yum-config-manager \
    yum -y install zsh && \
    wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh

USER 1001

# Install poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Set default shell to zsh
ENV SHELL /bin/zsh

# Create workspace dir used by VSCode
RUN mkdir /opt/app-root/src/workspace/

# Expose ports
EXPOSE 4000
