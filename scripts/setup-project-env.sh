#!/usr/bin/env bash --login

function set_dirs () {
    local SOURCE=${BASH_SOURCE[0]}
    while [ -L "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
        local DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
        SOURCE=$(readlink "$SOURCE")
        [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
    done
    CUR_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
    SCRIPT_DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
}

function usage () {
    echo "$0 <proj-name> <python-version>"
}

if [ -z "$1" ]; then
    usage
    exit 1
fi

if [ -z "$2" ]; then
    usage
    exit 1
fi

# provides CUR_DIR and SCRIPT_DIR variables
set_dirs
projDir="$(dirname "$SCRIPT_DIR")/projects/$1"

if [ ! -d $projDir ]; then
    echo "couldn't find the project directory @ $projDir"
fi

#envDir="$projDir/.conda"
envName="$(dirname $projDir | xargs basename $1)_env"
echo "project dir: $projDir"
#echo "Environment dir: $envDir"
echo "virtual environment: $envName"

envAvailable=1
if [ $(conda env list | grep $envName | wc -l) -eq 0 ]; then
    echo "creating conda environment"
    conda create -n $envName -y python=$2
    # conda create --prefix $envDir -y python=$2
    envAvailable=$? 
else
    envAvailable=0
fi

if [ $envAvailable -eq 0 ]; then
    conda activate $envName
    # conda activate $envDir
    if [ $? -eq 0 ]; then
        conda info --envs
        echo "pip @ $(which pip)"

        if [ ! -d "$projDir/dev-requirements.txt" ]; then
            pip install -r $projDir/dev-requirements.txt
        fi

        if [ ! -d "$projDir/requirements.txt" ]; then
            pip install -r $projDir/requirements.txt
        fi
    fi

    echo "Environment: $envName"
    echo "you can issue command 'conda activate $envName' to activate in the terminal"
fi


