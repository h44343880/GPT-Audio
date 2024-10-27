#!/bin/bash

# Usage: to start up GPT-Audio services

# Add the main server to the known hosts in the container
ssh-keyscan -H $MAIN_SERVER >> ~/.ssh/known_hosts

# SSH into the server and execute commands
sshpass -p "$SERVER_PASSWORD" ssh -o StrictHostKeyChecking=no -tt $USER@$MAIN_SERVER << EOF

    # Navigate to the packages directory
    cd $PACKAGES_PATH

    services=("GPT-Audio")

    echo "Running: bash ${CWD}/scripts/run_GPT-Audio.sh ${PACKAGES_PATH}/GPT-Audio python gpt.py"
    bash "${CWD}/scripts/run_GPT-Audio.sh" "${PACKAGES_PATH}/GPT-Audio" "python gpt.py" &
    # echo "Running: bash ${CWD}/scripts/run_GPT-Audio.sh ${PACKAGES_PATH}/GPT-Audio python real3d.py"
    # bash "${CWD}/scripts/run_GPT-Audio.sh" "${PACKAGES_PATH}/GPT-Audio" "python real3d.py" &

    wait
EOF