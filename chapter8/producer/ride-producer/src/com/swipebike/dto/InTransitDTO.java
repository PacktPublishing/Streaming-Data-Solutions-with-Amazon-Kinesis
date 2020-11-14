package com.swipebike.dto;

import com.amazonaws.services.kinesis.producer.KinesisProducer;
import com.amazonaws.services.kinesis.producer.KinesisProducerConfiguration;
import com.swipebike.StationServiceReader;
import netscape.javascript.JSObject;
import org.apache.log4j.Logger;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.nio.ByteBuffer;
import java.text.DateFormat;
import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Random;
import java.util.TimeZone;
import java.util.concurrent.atomic.AtomicInteger;

public class InTransitDTO {
    private static AtomicInteger inTransitCounter = new AtomicInteger(100);
    private static final Logger logger = Logger.getLogger(InTransitDTO.class);
    private TimeZone tz = TimeZone.getTimeZone("UTC");
    private DateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS"); // Quoted "Z" to indicate UTC, no timezone offset
    private Random rn = new Random();
    private int low = 120;
    private int high = 3600;
    DecimalFormat decFormat = new DecimalFormat("#.##");
    String kinesisStream = System.getenv().getOrDefault("KINESIS_STREAM", "defaultStreamName");
    String region = System.getenv().getOrDefault("AWS_REGION", "us-east-1");

    KinesisProducerConfiguration config = new KinesisProducerConfiguration()
            .setRecordMaxBufferedTime(2000)
            .setMaxConnections(5)
            .setRequestTimeout(60000)
            .setRegion(region);


    final KinesisProducer kpl = new KinesisProducer(config);

    {
        df.setTimeZone(tz);
    }

    public void dockBike(int stationId)  {
        JSONObject jo = new JSONObject();
        try {
            int tripDuration = rn.nextInt(high-low) + low;
            jo.put("stationId", stationId);
            jo.put("action", "DOCKED");
            jo.put("actionTime", df.format(new Date()));
            jo.put("tripDuration", tripDuration );
            jo.put( "price",  Double.parseDouble(decFormat.format(tripDuration/60.0)));
        } catch (JSONException e) {
            e.printStackTrace();
        }
        logger.info(jo.toString());
        sendToKinesis(jo);
        //logger.info(Thread.currentThread().getName() + " : " + inTransitCounter.getAndDecrement());
    }

    public void startUsingBike(int stationId) {
        JSONObject jo = new JSONObject();
        try {
            int tripDuration = rn.nextInt(high-low) + low;
            jo.put("stationId", stationId);
            jo.put("action", "RENTED");
            jo.put("actionTime", df.format(new Date()));
            jo.put("tripDuration", 0 );
            jo.put( "price",  0.00);

        } catch (JSONException e) {
            e.printStackTrace();
        }
        logger.info(jo.toString());
        sendToKinesis(jo);
        //logger.info(Thread.currentThread().getName() + " : " + inTransitCounter.getAndIncrement());
    }

    private void sendToKinesis(JSONObject jo){
        ByteBuffer data = null;
        data = ByteBuffer.wrap(jo.toString().getBytes());
        kpl.addUserRecord(kinesisStream, "bike", data);
    }
}
