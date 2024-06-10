FROM registry.redhat.io/ansible-automation-platform-22/ansible-builder-rhel8:latest

# Install oh-my-zsh as root
USER root
RUN microdnf install -y zsh wget vim bind-utils && microdnf clean all

# Install ansible testing python package
RUN pip3 install ansible-core ansible-test unittest2 pytest pytest-xdist pytest-forked ordereddict python-dotenv

# Install poetry
RUN pip3 install poetry && \
    poetry config virtualenvs.create false

# Create user
RUN groupadd -r user && useradd -r -g user -d /opt/app-root -s /bin/zsh user

# make working directories
RUN mkdir -p /opt/app-root && chmod a+rwx /opt/app-root && chown user:user /opt/app-root
RUN mkdir /workspaces && chmod a+rwx /workspaces && chown user:user /workspaces

# Switch to user
USER user

# Set default shell to zsh
ENV SHELL /bin/zsh

# Create workspace dir used by VSCode
RUN mkdir -p /opt/app-root/src/workspace/
WORKDIR /opt/app-root/src/workspace/

# Install and configure oh-my-zsh
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh 
COPY zshrc /opt/app-root/.zshrc

ENTRYPOINT /bin/zsh

