#!/bin/bash

tar xvf test-app-java.tar
./gradlew build
sudo docker build -t system-tests/local .
sudo -E docker-compose -f docker-compose-agent-prod.yml up -d datadog
sleep 20
sudo -E docker-compose -f docker-compose.yml up -d test-app-java
sudo docker-compose logs
echo "RUN DONE"
