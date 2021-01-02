from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_kinesis as kds,
    aws_kinesisfirehose as fh,
    aws_iam as iam,
    aws_ec2 as ec2,
)

with open("./user_data/user_data.sh") as f:
    user_data_file = f.read()

class ProducerCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        kda_src_bucket_name = core.CfnParameter(self, "kda_src_bucket_name", type="String",
            description="The name of the Amazon S3 bucket where uploaded files will be stored.")

        kda_output_bucket_name = core.CfnParameter(self, "kda_output_bucket_name", type="String",
            description="The name of the Amazon S3 bucket KDA output via Firehose will be stored.")

        sourceStreamName = core.CfnParameter(self, "sourceStreamName", type="String",
            description="The name of the Kinesis Data Stream.", default="BikeRideGenerator")
        
        deliveryStreamName = core.CfnParameter(self, "deliveryStreamName", type="String",
            description="The name of the Kinesis Firehose output stream.", default="BikeAnalyticsOutput")

        
        # Create S3 buckets
        kda_src_bucket = s3.Bucket(self, "kda_src_bucket", bucket_name=kda_src_bucket_name.value_as_string , versioned=False, removal_policy=core.RemovalPolicy.DESTROY)
        kda_output_bucket = s3.Bucket(self, "kda_output_bucket", bucket_name=kda_output_bucket_name.value_as_string, versioned=False, removal_policy=core.RemovalPolicy.DESTROY)

        # create Kinesis Source Stream
        sourceStream = kds.Stream(self, "sourceStream", stream_name = sourceStreamName.value_as_string, shard_count= 10)

        # Firehose Role aws_cdk.aws_iam.CfnRole
        fhIAMRole = iam.Role(self, "fhIAMRole", assumed_by=iam.ServicePrincipal('firehose.amazonaws.com'), 
            role_name="BikeRideFirehoseDeliveryRole", description="FireHose Delivery S3 Role" )

        fhIAMRole.add_to_policy(
            iam.PolicyStatement(resources= [kda_output_bucket.bucket_arn] , actions= ['s3:*'])
        )

        # create Firehose delivery stream
        fhS3Delivery = fh.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty ( 
            bucket_arn=kda_output_bucket.bucket_arn, role_arn=fhIAMRole.role_arn )
        
        deliveryStream = fh.CfnDeliveryStream(self, "deliveryStream", delivery_stream_name = deliveryStreamName.value_as_string,
            extended_s3_destination_configuration=fhS3Delivery)

        # ec2 instance 
        # VPC
        vpc = ec2.Vpc(self, "KDA-VPC",
            nat_gateways=0,
            subnet_configuration=[ec2.SubnetConfiguration(name="public",subnet_type=ec2.SubnetType.PUBLIC)]
        )

        # AMI 
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        # Instance Role and SSM Managed Policy
        ec2role = iam.Role(self, "InstanceSSM", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        ec2role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEC2RoleforSSM"))

        ec2role.add_to_policy(
            iam.PolicyStatement(resources= [sourceStream.stream_arn] , actions= ['kinesis:*'])
        )
        user_data = "#!/bin/bash\n"
        user_data += "echo export KINESIS_STREAM=" + sourceStreamName.value_as_string +" | sudo tee -a /etc/profile\n"
        user_data += "source /etc/profile\n"
        user_data += user_data_file
        
        
        # Instance
        instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t3.small"),
            machine_image=amzn_linux,
            vpc = vpc,
            role = ec2role,
            user_data=ec2.UserData.custom(user_data)
        )


        
