#!/bin/bash


increment_version () {
    echo "$1" | awk -F. '{$NF = $NF + 1;} 1' OFS=.
}

if [ -z "$GALAXY_API_KEY" ]
then
    echo "This script will publish the collection to galaxy.ansible.com"
    echo "Please ensure you have set the GALAXY_API_KEY environment variable"
    echo "     export GALAXY_API_KEY=<set me in .bashrc or directly>"
    echo "     "
    echo "Environment variable GALAXY_API_KEY is not set. Please set it before running this script."
    exit 1
fi

# Check for uncommitted changes
if ! git diff --quiet
then
    echo "There are uncommitted changes. Please commit them before running this script."
    exit 1
fi

# Check for untracked files
if [ -n "$(git status --porcelain)" ]
then
    echo "There are untracked files. Please add and commit them before running this script."
    exit 1
fi

set -e
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

CLN_DIR=$SCRIPT_DIR/ansible_collections/shuawest/routeros_batch

pushd $CLN_DIR

CLN_VERSION=$(grep 'version:' galaxy.yml | awk '{print $2}')
CLN_FILE=shuawest-routeros_batch-$CLN_VERSION.tar.gz

echo "Clean prior collection build"
rm $CLN_FILE || true

echo "Building collection"
ansible-galaxy collection build

echo "Publishing collection"
ansible-galaxy collection publish $CLN_FILE --api-key=$GALAXY_API_KEY

NEW_CLN_VERSION=$(increment_version $CLN_VERSION)

echo "Updating version to $NEW_CLN_VERSION"
sed -i "s/version: $CLN_VERSION/version: $NEW_CLN_VERSION/" galaxy.yml

git add galaxy.yml
git commit -m "Increment version to $NEW_CLN_VERSION"
git tag -a v$NEW_CLN_VERSION -m "Release version $NEW_CLN_VERSION"
git push origin v$NEW_CLN_VERSION

popd 

