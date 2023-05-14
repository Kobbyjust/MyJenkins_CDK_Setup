import os.path

from aws_cdk.aws_s3_assets import Asset

from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    App, Stack
)

from constructs import Construct

dirname = os.path.dirname(__file__)


class EC2InstanceStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC
        vpc = ec2.Vpc(self, "VPC",
            nat_gateways=0,
            subnet_configuration=[ec2.SubnetConfiguration(name="public",subnet_type=ec2.SubnetType.PUBLIC)]
            )

        # AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux2(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
            )

        # Instance Role and SSM Managed Policy
        role = iam.Role(self, "MyJenkinsInstanceInstanceRole", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodePipelineCustomActionAccess"))

        # Security Group
        jenkins_sg = ec2.SecurityGroup(
            scope=self,
            id='jenkins-server-sg',
            vpc=vpc,
            allow_all_outbound=True,
            description='security group for a Jenkins Instance',
        )

        # Instance
        instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=amzn_linux,
            vpc = vpc,
            role = role,
            security_group = jenkins_sg,
            )
        
        jenkins_sg = ec2.SecurityGroup(
            scope=self,
            id='jenkins-server-sg',
            vpc=vpc,
            allow_all_outbound=True,
            description='security group for a Jenkins Instance',
        )

        jenkins_sg.add_ingress_rule(
            peer = ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(22),
            description='allow SSH access from anywhere',
        )
        jenkins_sg.add_ingress_rule(
        peer=ec2.Peer.any_ipv4(),
        connection=ec2.Port.tcp(80),
        description='allow HTTP traffic from anywhere',
        )
        jenkins_sg.add_ingress_rule(
        peer=ec2.Peer.any_ipv4(),
        connection=ec2.Port.tcp(443),
        description='allow HTTP traffic from anywhere',
        )
        jenkins_sg.add_ingress_rule(
        peer=ec2.Peer.any_ipv4(),
        connection=ec2.Port.tcp(8080),
        description='allow HTTP traffic from anywhere to Port 8080',
        )

        # Script in S3 as Asset
        asset = Asset(self, "Asset", path=os.path.join(dirname, "configure.sh"))
        local_path = instance.user_data.add_s3_download_command(
            bucket=asset.bucket,
            bucket_key=asset.s3_object_key
        )

        # Userdata executes script from S3
        instance.user_data.add_execute_file_command(
            file_path=local_path
            )
        asset.grant_read(instance.role)

app = App()
EC2InstanceStack(app, "ec2-instance")

app.synth()
