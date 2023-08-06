#!/usr/bin/env bash

context_dir="./context"
dockerfile="sensormapgeo_ci.docker"
tag="sensormapgeo_ci:0.2.0"
gitlab_runner="sensormapgeo_gitlab_CI_runner"

echo "#### Build runner docker image"
sudo docker rmi ${tag}
sudo docker build -f ${context_dir}/${dockerfile} -m 20G -t ${tag} ${context_dir}

echo "#### Create gitlab-runner (daemon) container with tag; ${tag}"
sudo docker stop ${gitlab_runner}
sudo docker rm ${gitlab_runner}
sudo docker run -d --name ${gitlab_runner} --restart always \
-v /var/run/docker.sock:/var/run/docker.sock gitlab/gitlab-runner:latest

echo "#### Register container at gitlab, get token here https://gitext.gfz-potsdam.de/EnMAP/sensormapgeo/settings/ci_cd"
read -p "Please enter gitlab token: " token
echo ""
read -p "Please enter gitlab runner name: " runner_name
echo "New gitlab runner image will named  ${gitlab_runner}"
sudo docker exec -it ${gitlab_runner} /bin/bash -c "export RUNNER_EXECUTOR=docker && gitlab-ci-multi-runner register -n \
  --url 'https://gitext.gfz-potsdam.de/ci' \
  --registration-token '${token}' \
  --run-untagged=true \
  --locked=true \
  --tag-list  sensormapgeo_ci_client \
  --description '${runner_name}' \
  --docker-image '${tag}' "
ls
