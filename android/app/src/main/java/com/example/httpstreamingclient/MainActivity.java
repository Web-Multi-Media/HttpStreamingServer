package com.example.httpstreamingclient;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.TextView;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import com.google.gson.annotations.SerializedName;

import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.http.Query;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.Field;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Query;


//https://www.journaldev.com/13639/retrofit-android-example-tutorial

import java.util.List;

public class MainActivity extends AppCompatActivity {

    public static final String API_URL = "https:///streaming/the.ndero.ovh/streaming/";

    public static class VideoList {
        public final int count = 0;
        public final String next = "";
        public final String previous = "";

        public List<Video> results = null;

        public class Video  {

            @SerializedName("id")
            public Integer id;
            @SerializedName("name")
            public String name;

        }
    }

    public interface StreamingServerInterface {
        @GET("/videos?")
        Call<VideoList> doGetUserList(@Query("page") String page);
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        final TextView textView = (TextView) findViewById(R.id.text);
        // Create a very simple REST adapter which points the GitHub API.
        Retrofit retrofit =
                new Retrofit.Builder()
                        .baseUrl(API_URL)
                        .addConverterFactory(GsonConverterFactory.create())
                        .build();

        // Create an instance of our GitHub API interface.
        //GitHub github = retrofit.create(GitHub.class);
        StreamingServerInterface test = retrofit.create(StreamingServerInterface.class);





    }
}