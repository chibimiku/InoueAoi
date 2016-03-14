<?php 

if(!defined('AOICHAN_RUNNING')){
	exit('Access Denied');
}

//some common functions.
function getatlist($str, $atlist){
	$atlist_str = '';
	foreach($atlist as $atsingle){
		$atlist_str = $atlist_str.'@'.$atsingle.' ';
	}
	$final_str = $atlist_str.$str;
	return $final_str;
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