# Scalable Data Streaming with Amazon Kinesis

<a href="https://www.packtpub.com/product/scalable-data-streaming-with-amazon-kinesis/9781800565401?utm_source=github&utm_medium=repository&utm_campaign=9781800565401"><img src="https://static.packt-cdn.com/products/9781800565401/cover/smaller" alt="Scalable Data Streaming with Amazon Kinesis" height="256px" align="right"></a>

This is the code repository for [Scalable Data Streaming with Amazon Kinesis](https://www.packtpub.com/product/scalable-data-streaming-with-amazon-kinesis/9781800565401?utm_source=github&utm_medium=repository&utm_campaign=9781800565401), published by Packt.

**Design and secure highly available, cost-effective data streaming applications with Amazon Kinesis**

## What is this book about?
Amazon Kinesis is a collection of secure, serverless, durable, and highly available purpose-built data streaming services. This data streaming service provides APIs and client SDKs that enable you to produce and consume data at scale.
Scalable Data Streaming with Amazon Kinesis begins with a quick overview of the core concepts of data streams, along with the essentials of the AWS Kinesis landscape. You'll then explore the requirements of the use case shown through the book to help you get started and cover the key pain points encountered in the data stream life cycle.

This book covers the following exciting features: 
* Get to grips with data streams, decoupled design, and real-time stream processing
* Understand the properties of KFH that differentiate it from other Kinesis services
* Monitor and scale KDS using CloudWatch metrics
* Secure KDA with identity and access management (IAM)
* Deploy KVS as infrastructure as code (IaC)
* Integrate services such as Redshift, Dynamo Database, and Splunk into Kinesis

If you feel this book is for you, get your [copy](https://www.amazon.com/dp/1800565402) today!

<a href="https://www.packtpub.com/?utm_source=github&utm_medium=banner&utm_campaign=GitHubBanner"><img src="https://raw.githubusercontent.com/PacktPublishing/GitHub/master/GitHub.png" alt="https://www.packtpub.com/" border="5" /></a>

## Instructions and Navigations
All of the code is organized into folders. For example, chapter02.

The code will look like the following:
```
aws glue create-database --database-input 
"{\"Name\":\"smartcitybikes\"}"
aws glue create-table --database-name smartcitybikes --table-
input file://SmartCityGlueTable.json
```

**Following is what you need for this book:**
This book is for solutions architects, developers, system administrators, data engineers, and data scientists looking to evaluate and choose the most performant, secure, scalable, and cost-effective data streaming technology to overcome their data ingestion and processing challenges on AWS. Prior knowledge of cloud architectures on AWS, data streaming technologies, and architectures is expected.	

With the following software and hardware list you can run all code files present in the book (Chapter 1-12).

### Software and Hardware List

| Chapter  | Software required                   | OS required                        |
| -------- | ------------------------------------| -----------------------------------|
| 1-12	   | AWS account                         | Windows, Mac OS X, and Linux (Any) |
| 1-12     | AWS Java SDK version 1.11           | Windows, Mac OS X, and Linux (Any  |
| 1-12     | AWS CLI v2                          | Windows, Mac OS X, and Linux (Any  |
| 1-12     | Python 3 Interpreter                | Windows, Mac OS X, and Linux (Any  |

This is a repository for the book [Scalable Data Streaming with Amazon Kinesis](https://www.amazon.com/gp/product/1800565402) covering: 
* [Kinesis Data Streams (Chapter 4)](chapter4)
* [Kinesis Data Firehose (Chapter 5)](chapter5)
* [Kinesis Data Analytics (Chapter 6)](chapter6)
* [Kinesis Video Streams (Chapter 7)](chapter7)
* [Integrations (Chapter 8)](chapter8)

## AWS Messaging Service Comparison Table (chapter 2)

| | Amazon Kinesis Data Strams (KDS)| Amazon Kinesis Data Firehose (KDF) | Amazon Kinesis Data Analysis for KDA SQL | Amazon Kinesis Data Analytics for Fink | Amazon KinesisVideo Streams (KVS)| Amazon Managed Streaming for Apache Kafkfa (MSK) | Amazon Simple Queue Service (Amazon SQS) | Amazon SQS (FIFO) | Amazon SNS | IoT Core | Event Engine |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|AWS Managed | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
|Strengths|Low Latency with replay|Pre-built integrated  consumers|  Real-time data analytics with  ANSI 2011 SQL code | Real-time data analytics Open source compatibility, pre-built operators | Streaming video analysis |  Low latency open source compatibility with replay | Easy setup, deduplication, parallel processing | Easy setup, FIFO | Notification message types | IoT device message data| 
|Trade Offs|Customized consumers are required| Higher latency/limited destinations |Limited capabilities | Limited Flink configurations and REST APIs | Purpose built for video |  Manual scaling |  No order guarantee/no replay | Performance | Data retention duration | Data retention |
|Protocols|AWS REST API| AWS REST API |AWS REST API | AWS REST API | AWS REST API, HLS, DASH, Web-RTC |  TCP | Rest API | Rest API | Rest API, SMTP, SMS, HTTPS | MQTT, AWS Rest API |
|Guaranteed Ordering|Yes| No | Yes | Yes | Yes |  Yes | No | Yes | Yes | No |
|Delivery (deduping)|At least once| At least once |At least once Exactly Once | | At least/At most/exactly once | At least once | Exactly once | No | (Yes with FIFO) | At least once / at most once | 
|Data Retention Period (Max)|365 days| 24 hours | Limited by KPU total memory | Limited by KPU total storage | 10 Years | Configurable | 14 days | 14 days | Retries over days | 1 hour |
|Availability|Three AZ| Three AZ|Three AZ|Three AZ|Three AZ | Configurable | Three AZ | Three AZ | Three AZ | Three AZ |
|Scale/Throughput| No limit /~ shards|  No limit /automatic |Amazon Kinesis Processing Units (KPU) |Amazon Kinesis Processing Units (KPU)| 12.5 MB per second per stream |  25 Soft limit | No limits/automatic | 3000 TPS / API action | 300 TPS or 10 MB per second, per topic | No limits /automatic |
| Multiple consumers | Yes| No| 3 destination per application | Yes – up to 50 | Yes|  Yes | No | No | Yes | No | 
|Row/object size | 1 MB | Destination row/object size | 512 KB | Configurable | 1 second|  1MB default Configurable | 256 KB | 256 KB | 256 KB | 256 KB |

*Note: AWS is constantly releasing new services and features and this table may not be accurate.*

Based on:
* https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html
* https://docs.aws.amazon.com/general/latest/gr/ka.html
* https://docs.aws.amazon.com/general/latest/gr/akv.html
* https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/producer-sdk-limits.html


We also provide a PDF file that has color images of the screenshots/diagrams used in this book. [https://static.packt-cdn.com/downloads/9781800565401_ColorImages.pdf]


### Related products <Other books you may enjoy>
* Mastering Machine Learning on AWS [[Packt]](https://www.packtpub.com/product/mastering-machine-learning-on-aws/9781789349795) [[Amazon]](https://www.amazon.com/dp/1789349796)

* Learn Amazon SageMaker [[Packt]](https://www.packtpub.com/product/learn-amazon-sagemaker/9781800208919) [[Amazon]](https://www.amazon.com/dp/180020891X)

## Get to Know the Authors

**Tarik Makota**
hails from a small town in Bosnia. He is a Principal Solutions Architect with Amazon WebServices, builder, writer, and the self-proclaimed best fly fisherman at AWS. Never a perfect student, he managed to earn a Master of Science in Software Development and Management from RIT. When he is not “doing the cloud” or writing, Tarik spends most of his time flying fishing to pursue slippery trout. He feeds his addiction by spending summers in Montana. Tarik lives in New Jersey with his family, Mersiha, Hana, and two exceptionally perfect dogs.

**Brian Maguire** 
is a Solution Architect at Amazon Web Services, where he is focused on helping customers build solutions in the cloud. He is a technologist, writer, teacher, and student who loves learning. Brian lives in New Hope, Pennsylvania, with his family Lorna, Ciara, Chris, and several cats.

**Danny Gagne** 
is a Solutions Architect at Amazon Web Services. He has extensive experience in the design and implementation of large-scale high-performance analysis systems. He lives in New York City.

**Rajeev Chakrabarti**
is a Principal Developer Advocate with the Amazon Kinesis and the Amazon MSK team. He has worked for many years in the Big Data and Data Streaming space. Before joining the Amazon Kinesis team, he was a streaming Specialist Solution Architect helping customers build streaming pipelines. He lives in New Jersey with his family, Shaifalee and Anushka.

### Suggestions and Feedback
[Click here](https://docs.google.com/forms/d/e/1FAIpQLSdy7dATC6QmEL81FIUuymZ0Wy9vH1jHkvpY57OiMeKGqib_Ow/viewform) if you have any feedback or suggestions.

