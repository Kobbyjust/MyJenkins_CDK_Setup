
# Create EC2 Instance in new VPC with Jenkins, Docker Installed And Systems Manager enabled

This Project includes:

* Own VPC with public subnet (following AWS Defaults for new accounts)
* Creating Security with PORT 8080 enabled to access Jenkins
* Based on latest Amazon Linux 2
* System Manager replaces SSH (Remote session available through the AWS Console or the AWS CLI.)
* Userdata executed from script in S3 (`configure.sh`).
* Installing Jenkins, Docker and grant Jenkins user and Ubuntu user permission to docker deamon.

## Key Things To Note
Runnig this project Will create the about and bring you to the default Jenkins login page
You can access your Jenkins Server at
    `http://<ec2-instance-public-ip>:8080/`

ssh into you EC2 intances using Session Manager and Run the command below to obtain the Administrator password required
    `sudo cat /var/lib/jenkins/secrets/initialAdminPassword`

## Useful commands

 * `cdk bootstrap`   initialize assets before deploy
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `aws ssm start-session --target i-xxxxxxxxx` remote session for shell access
