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


class KdaAppStack(core.NestedStack):

    def __init__(self, scope: core.Construct, construct_id: str, iamRole: iam.Role, kdaAppName: str,  logGroup: log.LogGroup, logStream: log.LogStream, appConfig: kda.CfnApplicationV2.ApplicationConfigurationProperty, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        core.CfnOutput(self, "RoleNameFlinkIsUsing" , value= iamRole.role_name)
        core.CfnOutput(self, "KDA App Name" , value= kdaAppName)
        

        # The code that defines your stack goes here
        kdaApp = kda.CfnApplicationV2(self, "kda-flink-application", 
            runtime_environment= "FLINK-1_11", 
            service_execution_role= iamRole.role_arn, 
            application_description="KDA Flink app for BikeRides", 
            application_name=kdaAppName,
            application_configuration= appConfig, 
        )
        
        
        kda.CfnApplicationCloudWatchLoggingOptionV2(self, "FlinkLogging", 
            application_name= kdaApp.ref,
            cloud_watch_logging_option = kda.CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty(
                log_stream_arn="arn:aws:logs:{0}:{1}:log-group:{2}:log-stream:{3}".format(core.Aws.REGION, core.Aws.ACCOUNT_ID, logGroup.log_group_name , logStream.log_stream_name))
        )
