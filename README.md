# Streaming Data Solutions with Amazon Kinesis Code Examples 

<img src="https://user-images.githubusercontent.com/51995/111105043-6a16d780-8528-11eb-8a48-2275446b0a94.png" width="400" alt="Streaming Data Solutions with Amazon Kinesis book cover">

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




