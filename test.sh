#!/bin/bash

set -e
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

CLN_DIR=$SCRIPT_DIR/ansible_collections/shuawest/routeros_batch

pushd $CLN_DIR

#ansible-test units
ansible-test integration

popd 

