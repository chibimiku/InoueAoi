<?php 

//a simple reminder robot in php .
//design for weibo to make it seems not so alone.
//chibimiku@TSDM.net

define('AOICHAN_RUNNING', true);

require 'conf/config.inc.php';
//load library
require 'lib/libweibo-master/saetv2.ex.class.php';

getmyatlist(false);
echo "all task end.\n";

//unit test set.

function test_post_normal(){
	//some testdata
	$f_array = array('天使动漫谐星战术研究院', '紫夜幻晴');
	sayaword('试试多人at是否正常~', $f_array);
}

function test_post_pic(){
	//some testdata
	$f_array = array('天使动漫谐星战术研究院');
	postapic('试着上传一张图片，以后发表情全靠它了呢', 'D:\images\cp\20150320_006.jpg');
}

//core ai set.
function analy($myatinfo){
	//get from getmyatlist.
	echo "\n";
	if(strpos($myatinfo['text'], '能收到吗') !== false){
		echo 'debug:got'.$myatinfo['idstr'];
		//repost($myatinfo['idstr'], '收到啦 ');
	}elseif(strpos($myatinfo['text'], '233') !== false){
		echo 'debug:23333';
	}else{
		echo 'debug:nothing~';
	}
}

//base actions set.
function repost($sid, $text = NULL, $is_comment = 0){
	$o = new SaeTClientV2( WB_AKEY , WB_SKEY , WB_TOKEN);
	$o->repost($sid, $text, $is_comment);
}

function getmyatlist($new = true){
	$since_id = 0;
	if($new){
		$getsince_id = intval(file_get_contents(WB_FILE_SINCE_ID));
		if($getsince_id > 0){
			$since_id = $getsince_id;
		}
	}
	
	$o = new SaeTClientV2( WB_AKEY , WB_SKEY , WB_TOKEN);
	$o->set_debug(true);
	$rs = $o->mentions(1,50,$since_id);
	$myatinfo = $rs['statuses'][0];
	if(is_array($myatinfo)){
		analy($myatinfo);
		file_put_contents(WB_FILE_SINCE_ID, $myatinfo['idstr']);
	}else{
		return false;
	}
	//$debuginfo = var_export($rs);
	//file_put_contents('test.txt', $debuginfo);
}

function postapic($str, $picpath, $atlist = array()){
	//post a weibo with picture.
	$final_str = getatlist($str, $atlist);
	//request weibo update api.
	$o = new SaeTClientV2( WB_AKEY , WB_SKEY , WB_TOKEN);
	$o->set_debug(false);
	$o->upload($final_str, $picpath);
	mikulog("Try to say a word.\n");
}

function sayaword($str, $atlist = array()){
	$final_str = getatlist($str, $atlist);
	//request weibo update api.
	$o = new SaeTClientV2( WB_AKEY , WB_SKEY , WB_TOKEN);
	$o->set_debug(true);
	$o->update($final_str);
	mikulog("Try to say a word.\n");
}

//get newest unread. is it should be placed into actions?
function getlist(){
	//just request weibo api here.
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