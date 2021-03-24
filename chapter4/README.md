# Chapter 4: Amazon Kinesis Data Streams
Chapter 4 of [Scalable Data Streaming with Amazon Kinesis](https://www.amazon.com/gp/product/1800565402) covers Kinesis Data Streams. This document provides examples, source code, and links to the examples used throughout that chapter.

## References
### Technical Requirements
* Amazon CLI V2: https://aws.amazon.com/cli/
* jq (command-line JSON processor): https://stedolan.github.io/jq/)
* Python 3.8 or later

### External Documentation and Links
* Producers
  * Amazon Kinesis Agent https://github.com/awslabs/amazon-kinesis-agent
  * Kinesis Producer Libarary (KPL)
https://github.com/awslabs/amazon-kinesis-producer
* Consumers
  * Kinesis Consumer Library https://github.com/awslabs/amazon-kinesis-client
  * Building Enhanced Fan-Out Consumers https://docs.aws.amazon.com/streams/latest/dev/building-enhanced-consumers-api.html
* AWS Kinesis Data Streams Documentation
  * Amazon Kinesis Data Streams API Reference 
https://docs.aws.amazon.com/kinesis/latest/APIReference/Welcome.html
  * Amazon Kinesis Data Streams Developer Guide https://docs.aws.amazon.com/streams/latest/dev/kinesis-dg.pdf
* Kinesis Solutions and Pattern Examples
  * AWS Streaming Data Solution for Amazon Kinesis and AWS Streaming Data Solution for Amazon MSK https://github.com/awslabs/aws-streaming-data-solution-for-amazon-kinesis-and-amazon-msk
* Scaling Kinesis Data Streams
  * Kinesis Scaling Utility https://github.com/awslabs/amazon-kinesis-scaling-utils  


### Commands Used in the Chapter

aws kinesis register-stream-consumer \
    --stream-arn <your-stream-arn-here>  \
    --consumer-name KinesisConsumerApplication

### Known issues
