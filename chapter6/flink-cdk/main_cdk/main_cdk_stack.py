from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_kinesis as kds,
    aws_kinesisfirehose as fh,
    aws_iam as iam,
    aws_kinesisanalytics as kda,
    aws_cloudwatch as cwatch,
    aws_logs as log
)
from kda_app.kda_app_stack import KdaAppStack

class MainCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # this could be parameter as well 
        kdaAppName = "kda-flink-application"
        
        # Our Flink Jar File
        kdaApplicationJar = core.CfnParameter(self, "kdaApplicationJar", type="String",
            description="The name of the Flink JAR File.",
            default="kda-flink-app-1.0-SNAPSHOT.jar")

        bucketNameParm = core.CfnParameter(self, "bucketNameParm", type="String",
            description="The name of the Amazon S3 bucket where Flink JAR File is.")
        
        inputStream = core.CfnParameter(self, "inputStream", type="String",
            description="The name of the Kinesis data stream for Input.",
            default="ProducerStream")
        
        outputStream = core.CfnParameter(self, "outputStream", type="String",
            description="The name of the Kinesis Firehose delivery steram.",
            default="AnalyticsOutput")

        region = core.CfnOutput(self, "region", value= self.region)
        account = core.CfnOutput(self, "account", value= self.account)

        # s3 bucket where JAR file is 
        s3Bucket = s3.Bucket.from_bucket_name(self, "sourceBucket", bucket_name=bucketNameParm.value_as_string)
        
        bucketPolicy = iam.PolicyStatement(
            sid="GrantS3Access", 
            actions=["s3:*"], 
            resources=[s3Bucket.bucket_arn, s3Bucket.bucket_arn+"/*"]
        )

        core.CfnOutput(self, "KDASourceBucketARN" , value= s3Bucket.bucket_arn)
        core.CfnOutput(self, "KDASourceBucketName" , value= s3Bucket.bucket_name)
        
         # KDA Role - will be assumed by KDA to load JAR as well as to read from input or write to sink
        kdaIAMRole = iam.Role(self, "kdaIAMRole", assumed_by=iam.ServicePrincipal('kinesisanalytics.amazonaws.com'), 
             description="Kinesis Analytics role for application " + kdaAppName)
        kdaIAMRole.add_to_policy(statement=bucketPolicy)

        # input Kinesis Data Stream 
        kdsStream = kds.Stream.from_stream_arn(self,id="kdsinputstream",  stream_arn= "arn:aws:kinesis:" + region.value+ ":" + account.value+ ":stream/" + inputStream.value_as_string)
        
        # output (sink) Firehose Delivery Stream
        fhDeliveryARN = "arn:aws:firehose:"+ region.value+ ":" + account.value + ":deliverystream/" + outputStream.value_as_string
        
        # Logs and CWatch 
        logGroup = log.LogGroup(self, kdaAppName+"LogGroup",retention= log.RetentionDays.ONE_DAY )
        core.CfnOutput(self, "LogGroupName" , value= logGroup.log_group_name)
        logStream = log.LogStream(self,  kdaAppName+"LogStream",log_group = logGroup)
    
        # grant permissions to KDA IAM role
        s3Bucket.grant_read(identity=kdaIAMRole)
        kdsStream.grant_read(grantee=kdaIAMRole)
        cwatch.Metric.grant_put_metric_data(grantee=kdaIAMRole)
        logGroup.grant_write(grantee=kdaIAMRole)
            
        kdaIAMRole.add_to_policy(
            iam.PolicyStatement( sid="DescribeLog", resources=["arn:aws:logs:{0}:{1}:log-group:*".format(core.Aws.REGION, core.Aws.ACCOUNT_ID)],
                actions = ["logs:DescribeLog*"]
            )
        )

        kdaIAMRole.add_to_policy(
            iam.PolicyStatement(sid="FullAccessToJARFile", resources= [s3Bucket.bucket_arn+ "/"+ kdaApplicationJar.value_as_string ] , actions= ['s3:*'])
        )

        kdaIAMRole.add_to_policy(
            iam.PolicyStatement(sid="WriteToFirehose", resources=[fhDeliveryARN ], actions=["firehose:*"])
        )
    
        # KDA Flink application Configuration
        snapshots = kda.CfnApplicationV2.ApplicationSnapshotConfigurationProperty( snapshots_enabled= False)
        codeContent = kda.CfnApplicationV2.ApplicationCodeConfigurationProperty( 
            code_content=kda.CfnApplicationV2.CodeContentProperty(
                s3_content_location = kda.CfnApplicationV2.S3ContentLocationProperty( 
                    bucket_arn=s3Bucket.bucket_arn, 
                    file_key=kdaApplicationJar.value_as_string
                )
            ), 
            code_content_type="ZIPFILE")
        appProperties = kda.CfnApplicationV2.EnvironmentPropertiesProperty(property_groups=
            [
                kda.CfnApplicationV2.PropertyGroupProperty(
                    property_group_id="ConsumerConfigProperties", 
                    property_map =  (
                        {"AWS_REGION" : region.value,
                        "INPUT_STREAM" : inputStream.value_as_string,
                        "flink.inputstream.initpos" : "LATEST"
                        }
                    )
                )
            ,
                kda.CfnApplicationV2.PropertyGroupProperty(
                    property_group_id="OutputConfigProperties",
                    property_map =  (
                        {
                        "AWS_REGION": region.value,
                        "OUTPUT_KDF": outputStream.value_as_string
                        }
                    )
                )
            ]
        )

        appConfig = kda.CfnApplicationV2.ApplicationConfigurationProperty(
            application_code_configuration= codeContent,
            application_snapshot_configuration= snapshots,
            environment_properties = appProperties
        )
        # call KDA APP stack to create KDA Flink Application
        KdaAppStack(self, "app-stack", iamRole=kdaIAMRole,
            kdaAppName= kdaAppName,
            logGroup = logGroup,
            logStream = logStream,
            appConfig=appConfig
        )
        
        