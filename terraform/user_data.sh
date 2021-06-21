#!/bin/bash

apt-get update
apt-get -y install apt-transport-https ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get -y install docker-ce docker-ce-cli containerd.io awscli


aws ecr get-login-password --region ${aws_region} | docker login --username AWS --password-stdin ${aws_registry_url}

docker pull ${aws_repo_url}

cat << EOF > .env
AWS_REGION_NAME=${aws_region}
AWS_ACCESS_KEY_ID=${aws_access_key_id}
AWS_SECRET_ACCESS_KEY=${aws_secret_access_key}
EOF

docker run --init -p ${server_port}:8000 --env-file .env -d ${aws_repo_url}
