#FROM registry.access.redhat.com/ubi9/python-39:latest
FROM registry.redhat.io/ansible-automation-platform-22/ansible-builder-rhel8:latest

# Install oh-my-zsh as root
USER root
RUN microdnf install -y zsh wget vim bind-utils && microdnf clean all

# Install ansible testing python package
RUN pip3 install ansible-core ansible-test unittest2 pytest pytest-xdist pytest-forked ordereddict python-dotenv

# Install poetry
RUN pip3 install poetry && \
    poetry config virtualenvs.create false

RUN mkdir -p /opt/app-root && chmod a+rwx /opt/app-root

# Switch to user
RUN groupadd -r user && useradd -r -g user -d /opt/app-root -s /bin/zsh user 
USER user
#USER 1001

# Set default shell to zsh
ENV SHELL /bin/zsh

# Create workspace dir used by VSCode
RUN mkdir -p /opt/app-root/src/workspace/
WORKDIR /opt/app-root/src/workspace/

# Install and configure oh-my-zsh
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh 

#RUN echo -e "export ZSH=\"\$HOME/.oh-my-zsh\"\nZSH_THEME=\"robbyrussell\"\nplugins=(git rust golang 1password aws gcloud helm kubectl mvn oc pip vault vscode ansible)\nsource \$ZSH/oh-my-zsh.sh" > /opt/app-root/.zshrc
COPY zshrc /opt/app-root/.zshrc

ENTRYPOINT /bin/zsh

