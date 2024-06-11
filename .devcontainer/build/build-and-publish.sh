#!/bin/sh


git add -A; git commit -m "updated docker builder image for devcontainer"; git push

podman build -t quay.io/godepict/devcontainer-ansible-module .

podman push quay.io/godepict/devcontainer-ansible-module:latest


