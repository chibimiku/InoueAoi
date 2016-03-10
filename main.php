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

function sayaword($str){
	mikulog('Try to say a word.');
}

//get newest unread.
function getlist(){
	
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