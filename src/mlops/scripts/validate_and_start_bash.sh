#!/bin/bash

function usage () {
    echo 'docker run -it -e "AWS_PROFILE=<your-name-no-spaces>" -e "AWS_ACCESS_KEY_ID=\$IK_USER_AWS_ACCESS_KEY_ID" -e "AWS_SECRET_ACCESS_KEY=\$IK_USER_AWS_SECRET_ACCESS_KEY" [-e "AWS_REGION=us-east-1"] {IMAGE_ID}"'
    echo "make sure you set IK_USER_* properties in host environment"
}

if [ -z "$AWS_PROFILE" ]; then
    echo 'AWS_PROFILE is not passed as -e argument! `e.g. -e AWS_PROFILE=john`'
    usage
    exit 1
fi

if [ -z "$AWS_ACCESS_KEY_ID" ]; then
    echo 'AWS_ACCESS_KEY_ID is not passed as -e argument! `e.g. -e AWS_ACCESS_KEY_ID=key`'
    usage
    exit 1
fi

if [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo 'AWS_SECRET_ACCESS_KEY is not passed as -e argument! `e.g. -e AWS_SECRET_ACCESS_KEY=secret`'
    usage
    exit 1
fi

if [ -z "$AWS_REGION" ]; then
    aws configure set region us-east-1 --profile $AWS_PROFILE
    echo "defaulting AWS_REGION to us-east-1"
fi

/bin/bash
