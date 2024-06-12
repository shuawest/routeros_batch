FROM registry.redhat.io/ansible-automation-platform-24/ansible-python-toolkit-rhel9:latest

# Install oh-my-zsh as root
USER root
RUN microdnf install -y zsh wget vim bind-utils && microdnf clean all

# Create user
RUN mkdir -p /home/user && chmod ug+rwx /home/user
RUN groupadd -r user && useradd -r -g user -d /home/user -s /bin/zsh user
RUN chown user:user /home/user

# make working directories
RUN mkdir -p /opt/app-root && chmod ug+rwx /opt/app-root && chown user:user /opt/app-root
RUN mkdir /workspaces && chmod ug+rwx /workspaces && chown user:user /workspaces


# Install ansible testing python package
RUN pip3 install ansible-core molecule ansible-lint unittest2 pytest pytest-xdist pytest-forked ordereddict python-dotenv

# Install poetry
RUN pip3 install poetry && \
    poetry config virtualenvs.create false


# Switch to user
USER user

# Set default shell to zsh
ENV SHELL /bin/zsh

# Install and configure oh-my-zsh
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh 
COPY zshrc /home/user/.zshrc

# Create workspace dir used by VSCode
RUN mkdir -p /opt/app-root/src/workspace/ansible_collections/shuawest/routeros_batch/
WORKDIR /opt/app-root/src/workspace/ansible_collections/shuawest/routeros_batch/

ENTRYPOINT /bin/zsh

