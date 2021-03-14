# Chapter 5: Amazon Kinesis Data Firehose
Chapter 5 of [Scalable Data Streaming with Amazon Kinesis](https://www.amazon.com/gp/product/1800565402) covers Kinesis Data Firehose. The JSON configuration files and the python code included with Chapter 5 in this repository can be used with the **Use Case example: Bikeshare Station data pipeline with KDF** section of the chapter. Follow the directions provided in the chapter to execute the example.

## Technical Requirements
* Amazon CLI V2: https://aws.amazon.com/cli/
* Python 3.8 or later

## Description of files
1. station_addresses.csv - Contains the address data for SmartCity bike stations in csv format.
2. loadDynamoDBStationAddresses.py - Python code to load the address data to a Amazon DynamoDB table.
3. TrustPolicyForLambda.json - Contains the trust policy for the role used with the Lambda transform in the KDF delivery stream.
4. KDFSmartCityLambdaPolicy.json - Contains the IAM policy for the role used with the Lambda transform in the KDF delivery stream.
5. KDFLookupAddressTransform.py - The Lambda function to lookup and transform incoming data in KDF to include station address data.
6. CreateLambdaKDFLookupAddressTransform.json - Contains the configuration to create the Lambda function.
7. SmartCityGlueTable.json - Contains the configuration to create the Glue table, whose schema is used by KDF for data format conversion to parquet.
8. TrustPolicyForFirehose.json - Contains the trust policy for the role used with KDF.
9. KDFSmartCityDeliveryStreamPolicy.json - Contains the IAM policy for the role used with KDF.
10. KDFCreateDeliveryStreamSmartCityBikes.json - Contains the configuration to create the KDF delivery stream.
