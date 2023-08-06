#!/usr/bin/env bash

context_dir="./context"
dockerfile="sicor_ci.docker"
tag="sicor_ci:0.14.2"
gitlab_runner_prefix="sicor_gitlab_CI_runner"

echo "Remove existing runners"
echo "Relevant containers:"
sudo docker ps --filter name=${gitlab_runner_prefix}
container=$(sudo docker ps -aq --filter name=${gitlab_runner_prefix})
for cnt in ${container[@]};
do
    read  -p "Do you want to stop old container Container id:$cnt [y|n]?" quest_rm
    if (( "${quest_rm}" == "y" ))
    then
        echo "Container id:$cnt -> stop ->su rm"
        sudo docker stop $cnt
        sudo docker rm $cnt
    fi
done

read  -p "Do you want to remove old sicor image and build new one? [y|n]?" quest_rm
if (( "${quest_rm}" == "y" ))
then
    echo "Clone SICOR and EnPT to context directory."
    cd $context_dir
    rm -rf sicor
    rm -rf EnPT
    read -p "Please enter gitlab username: " gl_un
    git clone https://${gl_un}@gitext.gfz-potsdam.de/EnMAP/GFZ_Tools_EnMAP_BOX/EnPT.git
    git clone https://gitext.gfz-potsdam.de/EnMAP/sicor.git --branch update_docker_image --single-branch sicor
    cd ..
    echo "#### Build runner docker image"
    sudo docker rmi ${tag}
    sudo docker build -f ${context_dir}/${dockerfile} -m 20G -t ${tag} ${context_dir} &> docker_build.log
fi

read -p "How many runners shall be created? Enter number:" n_runners

for ((i=1;i<=$n_runners;i++));
do
    gitlab_runner="${gitlab_runner_prefix}_$(date '+%Y%m%d_%H%M%S')"
    echo "#### Create gitlab-runner (daemon) container with tag; ${tag}"
    sudo docker run -d --name ${gitlab_runner} --restart always \
    -v /var/run/docker.sock:/var/run/docker.sock gitlab/gitlab-runner:latest

    echo "#### Register container at gitlab, get token here https://gitext.gfz-potsdam.de/EnMAP/sicor/settings/ci_cd"
    read -p "Please enter gitlab token: " token
    read -p "Please enter gitlab runner name: " runner_name

    #test that n_runners is positive integer, 0 is ok, then no runner will be created, but image will be build
    if ! [[ "$n_runners" =~ ^[0-9]+$ ]]
        then
            echo "Sorry integers only"
    fi

    echo "New gitlab runner image will named  ${gitlab_runner}"
    sudo docker exec -it ${gitlab_runner} /bin/bash -c "export RUNNER_EXECUTOR=docker && gitlab-ci-multi-runner register -n \
      --url 'https://gitext.gfz-potsdam.de/ci' \
      --registration-token '${token}' \
      --run-untagged=true \
      --locked=true \
      --tag-list  sicor_ci_client \
      --description '${runner_name}_${i}' \
      --docker-image '${tag}' "
done
