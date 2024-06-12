#!/bin/bash

# configuration
VENV_NAME=ansible2.9
ANSIBLE_VER=2.9
PYTHON_BIN=/usr/bin/python3

# default and derived 
VENV_HOME=~/dev/apps/python-venv
PYTHON_VER=$($PYTHON_BIN -V | awk '{print $2}')

echo "Using Python version $PYTHON_VER ($PYTHON_BIN)"

echo "Create and activate venv '$VENV_NAME' for python $PYTHON_VER and ansible $ANSIBLE_VER"
mkdir -p $VENV_HOME
pushd $VENV_HOME

$PYTHON_BIN -m venv $VENV_NAME
source $VENV_NAME/bin/activate

echo "New python3 default = $(python3 -V)"
python3 -V

echo "upgrade pip"
python3 -m pip install --upgrade pip

echo "Install ansible $ANSIBLE_VER"
python3 -m pip install ansible-core molecule ansible-lint unittest2 pytest pytest-xdist pytest-forked ordereddict python-dotenv

which ansible 

popd

echo 
echo "activate venv with: "
echo 
echo "   source $VENV_HOME/$VENV_NAME/bin/activate"
echo 




