#!/bin/bash

function usage () {
    echo 'docker run -it -e "AWS_PROFILE=<your-name-no-spaces>" -e "AWS_ACCESS_KEY=\$IK_USER_AWS_ACCESS_KEY" -e "AWS_ACCESS_SECRET=\$IK_USER_AWS_ACCESS_SECRET" [-e "AWS_REGION=us-east-1"] {IMAGE_ID}"'
    echo "make sure you set IK_USER_* properties in host environment"
}

function configure () {
    aws configure set aws_access_key_id $AWS_ACCESS_KEY $AWS_REGION
    aws configure set aws_secret_access_key $AWS_ACCESS_SECRET $AWS_REGION
    aws configure set region $AWS_REGION
    aws configure set output yaml
}

function print () {
    echo "---------------------------------------"
    echo "HOME = $(echo `pwd`)"
    aws configure list
    echo "---------------------------------------"
}

if [ -z "$AWS_PROFILE" ]; then
    echo 'AWS_PROFILE is not passed as -e argument! `e.g. -e AWS_PROFILE=john`'
    usage
    exit 1
fi

if [ -z "$AWS_ACCESS_KEY" ]; then
    echo 'AWS_ACCESS_KEY is not passed as -e argument! `e.g. -e AWS_ACCESS_KEY=key`'
    usage
    exit 1
fi

if [ -z "$AWS_ACCESS_SECRET" ]; then
    echo 'AWS_ACCESS_SECRET is not passed as -e argument! `e.g. -e AWS_ACCESS_SECRET=secret`'
    usage
    exit 1
fi

if [ -z "$AWS_REGION" ]; then
    export AWS_REGION=us-east-1
    echo "defaulting AWS_REGION to us-east-1"
fi

print
/bin/bash
