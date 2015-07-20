<?php
require "conf.php";

header("Access-Control-Allow-Origin: *");

echo $test;

if( isset($_GET["mode"]) ){

    if( $_GET["mode"] == "pux" ){

        $contents = file_get_contents("php://input");
        $contents = str_replace("data:image/jpeg;base64,","",$contents);
        $contents = urlencode($contents);
        $contents = "inputBase64=".$contents;
        $apiUrl = "https://api.apigw.smt.docomo.ne.jp/puxImageRecognition/v1/faceDetection?facePartsCoordinates=0&blinkJudge=0&enjoyJudge=1&response=json&APIKEY=".$puxkey;
        $curl = curl_init($apiUrl);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "POST");
        curl_setopt($curl, CURLOPT_HTTPHEADER, [
          'Content-Type: application/x-www-form-urlencoded'
          ]);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $contents);

        //echo $contents;
        curl_exec($curl);

        curl_close($curl);
    }

    if( $_GET["mode"] == "tts" ){

        $text = $_GET["text"];
        echo $text;
        $apiUrl = "https://api.apigw.smt.docomo.ne.jp/virtualNarrator/v1/textToSpeech?APIKEY=".$ttskey;

        $data = [
            "Command"=>"AP_Synth",
            "TextData"=>$text
        ];
        $data = http_build_query($data,"","&");
        $header = [
            "Content-Type: application/x-www-form-urlencoded",
            "Content-Length: ".strlen($data)
        ];
        $context = [
            "http"=>[
                "method"=>"POST",
                "header"=>implode("¥r¥n",$header),
                "content"=>$data
            ]
        ];

        $response = file_get_contents($apiUrl,false,stream_context_create($context));
        echo '<audio autoplay src="data:audio/wav;base64,'.base64_encode($response).'"/>';
        echo $response;
    }

    exit();
}

?>
