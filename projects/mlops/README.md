# mlops commands

## Build Docker Image
```
docker build -t "mlops_lab:Dockerfile" .
```

## Set ENV variables
Add below lines to your source (~.zshrc for zsh, ~/.bashrc for bash) file
```
export IK_USER_AWS_PROFILE=<your-name>
export IK_USER_AWS_ACCESS_KEY=<get-key-from-aws>
export IK_USER_AWS_ACCESS_SECRET=<get-secret-from-aws>
```


## Run Docker Instance
After you run below commands, it should open up bash shell
```
DOCKER_IMG_ID=$(docker images | grep "/mlops_lab" | xargs echo $1 | cut -d ' ' -f 3)

[ ! -z "$DOCKER_IMG_ID" ] && docker run -it  $DOCKER_IMG_ID \
"AWS_PROFILE=$IK_USER_AWS_PROFILE" \
"AWS_ACCESS_KEY=$IK_USER_AWS_ACCESS_KEY" \
"AWS_ACCESS_SECRET=$IK_USER_AWS_ACCESS_SECRET"
```

## setup_dl_ec2_instance.sh
This script contains logic to check, clean & provision following resources to do deep learning
- key pair
- security group
- 1 ec2 instance

## check current active resources on aws
```
./scripts/setup_dl_ec2_instance.sh
```

## clean any active resource status on aws
```
./scripts/setup_dl_ec2_instance.sh --clean
```

## create resources on aws
```
./scripts/setup_dl_ec2_instance.sh --create
```

## ssh into EC2 instance
Make sure below command lists the EC2 instance and public dns before you do ssh
```
./scripts/setup_dl_ec2_instance.sh
```
```
ssh -i ~/.ssh/<KEYPAIR_NAME>.pem ubuntu@<PUBLIC_DNS_NAME>
```




