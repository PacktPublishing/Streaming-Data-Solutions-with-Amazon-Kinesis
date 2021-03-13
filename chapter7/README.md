# Chapter 7: Amazon Kinesis Video Streams
Chapter 7 of [Scalable Data Streaming with Amazon Kinesis](https://www.amazon.com/gp/product/1800565402) covers Kinesis Video Streams. This document provides examples, source code, and links to the examples used throughout that chapter.

## References
### Technical Requirements
* Amazon CLI V2: https://aws.amazon.com/cli/
* jq (command-line JSON processor): https://stedolan.github.io/jq/)
* Android Studio https://developer.android.com/studio/index.html
* VLC: https://www.videolan.org/
* Docker: https://www.docker.com/products/container-runtime#/download
* NodeJS: https://nodejs.org/en/download/



### External Documentation and Links
* WebRTC
  * Amazon Kinesis Video Streams WebRTC Developer Guide https://docs.aws.amazon.com/kinesisvideostreams-webrtc-dg/latest/devguide/kinesisvideo-dg.pdf
  * WebRTC SDK in JavaScript for Web Applications
https://docs.aws.amazon.com/kinesisvideostreams-webrtc-dg/latest/devguide/kvswebrtc-sdk-js.html
  * WebRTC SDK in C for Embedded Devices
https://docs.aws.amazon.com/kinesisvideostreams-webrtc-dg/latest/devguide/kvswebrtc-sdk-c.html
  * TURN https://www.ietf.org/rfc/rfc5766.txt
  * STUN https://www.ietf.org/rfc/rfc5389.txt
  * ICE https://www.ietf.org/rfc/rfc5245.txt
* AWS Kinesis Video Streams Documentation
  * Amazon Kinesis Video Streams API Reference 
https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/API_Reference.html
  * Amazon Kinesis Video Streams Developer Guide https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/kinesisvideo-dg.pdf 



## WebRTC Examples

### Create a Kineis Video Streams WebRTC Signaling Channel:

Use the AWS CLI to create a Kineis Video Streams WebRTC Signaling Channel with the name "myChannel":
```bash
aws kinesisvideo create-signaling-channel --channel-name "myChannel"
```
It will return a json document with the Channel ARN:

```json
{
    "ChannelARN": "arn:aws:kinesisvideo:us-east-1:************:channel/myChannel/1615658870269"
}
```


### AWS KVS WebRTC Test Page
AWS provides a simple web page that can be used to exercise the WebRTC functionality.  It's especially useful test WebRTC functionality as a master or a viewer.  It can be accessed here: https://awslabs.github.io/amazon-kinesis-video-streams-webrtc-sdk-js/examples/index.html

To run it locally, you'll need to have nodeJS installed. Execute teh following commands:

```bash
git clone https://github.com/awslabs/amazon-kinesis-video-streams-webrtc-sdk-js.git
cd amazon-kinesis-video-streams-webrtc-sdk-js/
npm install
npm run develop
```
It will be accessible at http://localhost:3001

### AWS Javascript WebRTC view

The **[viewer.html](viewer.html)** file in this directory provides a simple implementation of an html page that uses the [AWS Javascript SDK](https://aws.amazon.com/sdk-for-javascript/) and the [AWS Kinesis Video Streams WebRTC Javascript SDK](https://docs.aws.amazon.com/kinesisvideostreams-webrtc-dg/latest/devguide/kvswebrtc-sdk-js.html).  

You will need to set the config at the top to speicfy the **channelName**, e.g. `myChannel`, ensure the **region** is correct, currently set to `us-east-1`, and set the `accessKeyId` and `secretAccesKey`. 

**Note: This is only for local testing, do not ever put your accessKeyID or secretAccessKey in code or anywhere a client can access it.**
```javascript
     let config = {
        role: KVSWebRTC.Role.VIEWER,
        channelName: "XXXXXXXXXX",
        channelARN: 'NOT SET YET', 
        channelEndpoint:'NOT SET YET',
        region: 'us-east-1',
        clientId: 'HCCTTKPGE81', //made up ID 
        credentials: {
          accessKeyId:'XXXXXXXXXXXXXXXXXXX',                            
          secretAccessKey:'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        }
      }
```
## Kinesis Video Streams (KVS Examples)

The follwing examples for Kinesis Video Streams will primarily be focused on the CLI and on Docker.

### CLI 
The AWS CLI provides simple interface to create and access data from KVS.  We'll start by showing how to get data out of the stream, then how to get data into it.  

For the consumption CLI API calls you will first need to get endpoints, described in detail here: [Get Data Endpoint](https://docs.aws.amazon.com/cli/latest/reference/kinesisvideo/get-data-endpoint.html).  The examples below always get the endpoint, create the fragment, and then fetch the data.

#### Create Stream
The following command will create a stream named *myStream* with a data retention period of *24* hours:

```bash
aws kinesisvideo create-stream --stream-name "myStream" --data-retention-in-hours "24"
```

#### GetClip
The GetClip API call requires a **Stream Name**, a fragment **Start Time** and ** End Time**, and the name of the file, e.g. "myvideo.mp4".  The example below will data down from the stream, you will need to update the start time and end time to a time when your stream has data. After this CLI sample, we have a small script that will create a fragment that captuers the last 5 minutes.  This command will downlaod the file as "myvideo.mp4".
```bash
STREAM_NAME="<STREAM NAME>"
API_NAME="GET_CLIP"
ENDPOINT_JSON=$(aws kinesisvideo get-data-endpoint --stream-name $STREAM_NAME --api-name $API_NAME)
ENDPOINT=$(jq -r '.DataEndpoint' <<< $ENDPOINT_JSON)
FRAGMENT="FragmentSelectorType=SERVER_TIMESTAMP,TimestampRange={StartTimestamp=2021-01-01T05:58:00,EndTimestamp=2021-01-01T05:59:00}"
aws kinesis-video-archived-media get-clip --stream-name $STREAM_NAME --clip-fragment-selector $FRAGMENT --endpoint-url $ENDPOINT myvideo.mp4

```

##### Fragment - last 5 minutes
The following shell script will help create a fragment that will can be used to get the last 5 minutes
```
DATE=$(date -u  "+%Y-%m-%dT%H:%M:%S")
START_DATE=$(date -v-5M -ujf "%Y-%m-%dT%H:%M:%S" "+%Y-%m-%dT%H:%M:%S" "${DATE}")
FRAGMENT="FragmentSelectorType=SERVER_TIMESTAMP,TimestampRange={StartTimestamp=${START_DATE},EndTimestamp=${DATE}}"

echo $FRAGMENT 
```

#### Get DASH Stream
The [DASH URL CLI](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/kinesis-video-archived-media/get-dash-streaming-session-url.html) will create a URL for the fragment specified:

```bash
STREAM_NAME="<STREAM NAME>"
API_NAME="GET_DASH_STREAMING_SESSION_URL"

ENDPOINT_JSON=$(aws kinesisvideo get-data-endpoint --stream-name $STREAM_NAME --api-name $API_NAME)
ENDPOINT=$(jq -r '.DataEndpoint' <<< $ENDPOINT_JSON)
EXPIRES=4000
PLAYBACK_MODE="ON_DEMAND"
FRAGMENT="FragmentSelectorType=SERVER_TIMESTAMP,TimestampRange={StartTimestamp=2021-01-01T05:58:00,EndTimestamp=2021-01-01T05:59:00}"
aws kinesis-video-archived-media get-dash-streaming-session-url --stream-name $STREAM_NAME --playback-mode $PLAYBACK_MODE --expires $EXPIRES --endpoint-url $ENDPOINT --dash-fragment-selector $FRAGMENT  

```
It returns:
```json
{
    "DASHStreamingSessionURL": "https://XXXXXXXXX.kinesisvideo.us-east-1.amazonaws.com/dash/v1/getDASHManifest.mpd?SessionToken=CiCSKbC-1CylV2GEK6g8VRdo9HBWNbANgq891D63VAAgshIQV1S0hbQmlEQM5nr2NFaMoRoZzVImpdI4gvqY4suc5QeqvIDjahO_40qITiIgVe9cBGFzcsJnLYobfxnvoAk0YQfzpAhfeXe7N2Ji-2w~"
}
```

This URL can then be opened in VLC to view the KVS stream.

#### Get HLS Stream
The [HLS URL CLI](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/kinesis-video-archived-media/get-hls-streaming-session-url.html) functions in the exact same was as the DASH URL CLI.  Though in this exmaple we've changed the **Plabyack Mode** to **LIVE** so it will show the frames as they're added.
```bash
STREAM_NAME="<STREAM NAME>"
API_NAME="GET_HLS_STREAMING_SESSION_URL"   

ENDPOINT_JSON=$(aws kinesisvideo get-data-endpoint --stream-name $STREAM_NAME --api-name $API_NAME)
ENDPOINT=$(jq -r '.DataEndpoint' <<< $ENDPOINT_JSON)

EXPIRES=40000 
PLAYBACK_MODE="LIVE"

aws kinesis-video-archived-media get-hls-streaming-session-url --stream-name $STREAM_NAME --expires $EXPIRES --playback-mode $PLAYBACK_MODE --endpoint-url $ENDPOINT  
```

It will return a URL that can then be displayed in VLC like the DASH example.

####

### Docker
AWS provides docker images with Gstreamer and the AWS producer SDK already configured, this is the easiest and quickest way to get data into Kinesis Video Streams.  For more details go here: https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/examples-gstreamer-plugin.html

1. The docker images private and so you must authenticate Docker with AWS:
```bash
aws ecr get-login-password –region us-west-2 | docker login –username AWS –password-stdin 546150905175.dkr.ecr.us-west-2.amazonaws.com
```

2. Pull down the docker image:
```bash
sudo docker pull 546150905175.dkr.ecr.us-west-2.amazonaws.com/kinesis-video-producer-sdk-cpp-amazon-linux:latest
```

3. Run the docker image, note the following command is mounting `/Users/$USER/data` to `/mnt/data`.  It's important to change that to the proper path for your username.
```bash
sudo docker run -v /Users/$USER/data:/mnt/data -it --network="host" 546150905175.dkr.ecr.us-west-2.amazonaws.com/kinesis-video-producer-sdk-cpp-amazon-linux /bin/bash
```

4. Test that KVS is properly configured, if you see a bunch of optons it's configured correctly.  If you see `No such element or plugin 'kvssink'` then there something isn't configured correctly.
```bash
gst-inspect-1.0 kvssink
```

5. Inside of docker we'll download a sample video that we can stream to KVS.  
```
wget https://github.com/Matroska-Org/matroska-test-files/blob/master/test_files/test2.mkv
```

6. The following script can be executed to stream the file.  Note that you need to include the **Stream Name**, **Access Key**, **Secret Access Key**, **Region**, and the path to the file for instance `/mnt/mydata/test2.mkv`.

```bash
STREAMNAME="myStream"
ACCESSKEY="********************"
SECRETKEY="****************************************"
REGION="us-east-1"

gst-launch-1.0 -v filesrc location="/mnt/mydata/test2.mkv" ! matroskademux name=demux ! queue ! h264parse ! kvssink name=sink aws-region=$REGION stream-name=$STREAMNAME  access-key=$ACCESSKEY secret-key=$SECRETKEY streaming-type=offline demux. ! queue ! aacparse ! sink.
```

7. **OPTIONAL:** If you have an IP Camera or other camera with an RTSP url, you can use the following command to stream it KVS.
```bash
STREAMNAME="kvstream"
ACCESSKEY="********************"
SECRETKEY="****************************************"
REGION="us-east-1"
URI="rtsp://username:pass@192.168.1.22/live"

gst-launch-1.0 rtspsrc location=$URI short-header=TRUE ! rtph264depay ! video/x-h264, format=avc,alignment=au ! kvssink storage-size=512 aws-region=$REGION stream-name=$STREAMNAME  access-key=$ACCESSKEY secret-key=$SECRETKEY
```

### Android

To build the Android example, follow the instructions on this page:
https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/producer-sdk-android.html


### Rekognition

1. Create the faces collection in Rekognition
```bash
aws rekognition create-collection --collection-id faces 
```

2. Add faces to the collection using [Index Faces](https://docs.aws.amazon.com/cli/latest/reference/rekognition/index-faces.html).  Note, we are adding one image at a time, repalce the **IMAGE_NAME** with the an ID, e.g. "danny-1", and the **PATH_TO_FILE** with a path, e.g. "photos/danny-1.jpg".
```bash
aws rekognition index-faces --collection-id faces --external-image-id IMAGE_NAME --image-bytes fileb://PATH_TO_FILE
```

3. Create Kinesis Data Stream for Rekognition Output
```bash
aws kinesis create-stream --stream-name kvs-ml --shard-count 1 
```

3. Create the stream processor and connect it to Kinesis.  Note the ARNs need to be set for the KVS stream, the KDS Stream, the IAM Role, and match the collection name we created above, in this case it's 'faces'.

```bash
aws rekognition create-stream-processor --name kvsprocessor \
 --input '{"KinesisVideoStream":{"Arn":"arn:aws:kinesisvideo:us-east-1:XXXXXXXXXXXX:stream/demo-stream/1609995253290"}}' \
 --stream-processor-output '{"KinesisDataStream":{"Arn":"arn:aws:kinesis:us-east-1:XXXXXXXXXXX5:stream/kvs-ml"}}'\
 --role-arn arn:aws:iam::XXXXXXXXXXXX:role/test-kvs \
 --settings '{"FaceSearch":{"CollectionId":"faces","FaceMatchThreshold":85.5}}' \
```

4. To list the stream processors run this command:
```bash
aws rekognition list-stream-processors
```

5. To start the stream processor:  
```bash
aws rekognition start-stream-processor --name kvsprocessor 
```

6. To stop the stream processor:
```bash
aws rekognition stop-stream-processor --name kvsprocessor
```

