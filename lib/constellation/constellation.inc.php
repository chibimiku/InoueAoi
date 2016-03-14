<?php 

//for test

//$result = bae_api_get(6);
//var_dump($result);
 
 //({"Xz":"巨蟹座","Gr":"no","Msg":"与人交流的机会多，会接触到各种类型的人。","Zy":"今天有机会发挥自己的沟通才能，期间会遇到一些脾气古怪的人，虽然让你有些莫名其妙，但对方的一言一行对你也颇有好的影响。单身者与个性独特的异性擦出爱情火花的机率高，想恋爱还需多了解对方。","Riqi":"2016年03月13日"}) 
 //return data like this.

 //from text to typeid.
function constellation_api_get($typeid){
	$url  = 'http://shxz.yiqibazi.com/Handler/GetXZYS.ashx?typeId='.$typeid;
	$ch = curl_init($url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_HTTPHEADER, array('User-Agent :Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'));
	echo "http request sent...";
	$content = curl_exec($ch);
	echo "http request got completed...";
	//remove '(' and ')'
	$content = substr($content, 1);
	$content = substr($content, 0, strlen($content)-1);
	//echo $content;
	return json_decode($content);
}

function constellation_gettypeid($str){
	$detectarray = array(
		'水瓶座' => 1,
		'双鱼座' => 2,
		'白羊座' => 3,
		'金牛座' => 4,
		'双子座' => 5,
		'巨蟹座' => 6,
		'狮子座' => 7,
		'处女座' => 8,
		'天秤座' => 9,
		'天蝎座' => 10,
		'射手座' => 11,
		'摩羯座' => 12,
	);
	foreach($detectarray as $key => $row){
		if(strpos($str, $key) !== false){
			return $row;
		}
	}
	return false;
}

?>