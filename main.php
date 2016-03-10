<?php 

//a simple reminder robot in php .
//design for weibo to make it seems not so alone.
//chibimiku@TSDM.net

define('AOICHAN_RUNNING', true);

require 'conf/config.inc.php';
//load library
require 'lib/libweibo-master/saetv2.ex.class.php';

//sayaword('test');
echo "all task end.";

function sayaword($str, $atlist = array()){
	$atlist_str = '';
	foreach($atlist as $atsingle){
		$atlist_str = $atlist_str.'@'.$atsingle.' ';
	}
	$final_str = $atlist_str.$str;
	//request weibo update api.
	
	mikulog("Try to say a word.\n");
}

//get newest unread.
function getlist(){
	//just request weibo api here.
}

function mikulog($content, $level = 'INFO'){
	printerr('['.date('Y-m-d H:i:s').']['.$level.']'.$content."\n");
}

function printerr($str){
	$stderr = fopen('php://stderr', 'w');
	fwrite($stderr, $str);
	fclose($stderr);
}

?>