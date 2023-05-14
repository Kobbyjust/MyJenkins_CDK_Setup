#!/bin/sh
# Use this to install software packages

sudo yum update –y

# Add the Jenkins repo using the following command:
sudo wget -O /etc/yum.repos.d/jenkins.repo \
    https://pkg.jenkins.io/redhat-stable/jenkins.repo

# Import a key file from Jenkins-CI to enable installation from the package:
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

sudo yum upgrade

# Install Java (Amazon Linux 2):
sudo amazon-linux-extras install java-openjdk11 -y

# Install
sudo yum install jenkins -y

# Start Jenkins as a service
sudo systemctl start jenkins
