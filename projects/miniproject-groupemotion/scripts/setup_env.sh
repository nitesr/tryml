#!/usr/bin/env bash --login

function usage () {
    echo "$0 <python-version>"
}
if [ -z "$1" ]; then
    usage
    exit 1
fi

projDir="$(dirname `pwd`)"
projName="$(basename $projDir)"
echo $projName
../../../scripts/setup-project-env.sh $projName $1