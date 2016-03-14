<?php 

//a simple reminder robot in php .
//design for weibo to make it seems not so alone.
//chibimiku@TSDM.net

define('AOICHAN_RUNNING', true);

//crontab runs under cli.
//just now use this entry.

//options area.
$shortopts = "";
$shortopts .= "a:";  // Required value
//$shortopts .= "v::"; // Optional value
//$shortopts .= "abc"; // These options do not accept values
$longopts = array(
	"required:", // Required value
	"optional::", // Optional value
	"option", // No value
	"opt", // No value
);
$options = getopt($shortopts, $longopts);

if(!isset($options['a'])){
	exit("AoiChan:ERROR, cannot find action.cli usage: php main.php -a actions \n");
}
$action = $options['a'];

require 'conf/config.inc.php';
//load library
require 'lib/libweibo-master/saetv2.ex.class.php';
require 'lib/constellation/constellation.inc.php';
require 'lib/common/aoi_common.inc.php';

switch($action){
	case 'timing':
		$showtime = date("Y-m-d H:i:s");
		$talkstr = "现在时间是 $showtime , 请注意保护眼睛，每个小时休息一下~ ";
		//echo $talkstr;
		sayaword($talkstr,array('天使动漫谐星战术研究院'));
		break;
	case 'refresh':
		mikulog('action is refresh...');
		$atlist = getmyatlist(false);
		mikulog('got atlist for '.count($atlist),'DEBUG');
		if(is_array($atlist) && count($atlist) > 0){
			$lastestpost = $atlist[0];
			mikulog('got the 1st atlist...', 'DEBUG');
			analy($lastestpost);
			//var_dump($atlist);
		}else{
			echo "nothing new.\n";
		}
		//get newest at.
		
		break;
	default:
		echo "available actions: \n";
		echo "timing. check in time and repo.\n";
		echo "refresh. find new atme post.\n";
		exit("AoiChan:ERROR, cannot find action.cli usage: php main.php -a actions \n");
}

//getmyatlist(false);
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
	mikulog('Entry core AI...', 'INFO');
	if(strpos($myatinfo['text'], '能收到吗') !== false){
		echo 'debug:got'.$myatinfo['idstr'];
		//repost($myatinfo['idstr'], '收到啦 ');
	}elseif(strpos($myatinfo['text'], '/233 ') !== false){
		mikulog('pick up 233.');
		repost($myatinfo['idstr'], '[哈哈]');
	}elseif(strpos($myatinfo['text'], '/转发抽奖 ') !== false){
		//repost and get award
		mikulog("debug: ot reward. repost..");
		repost($myatinfo['idstr'], WB_ID_REWEARD_USERNAME.' ,come');
	}elseif(strpos($myatinfo['text'], '/占卜 ') !== false){
		mikulog('pick up constellation','DEBUG');
		//find type from str.
		$typeid = constellation_gettypeid($myatinfo['text']);
		if(!$typeid){
			echo "cannot find typeid...";
			return false;
		}
		$predictword = '';
		mikulog('start to get constellation info for id:'.$typeid.' ...', 'TRACE');
		$remotedata = constellation_api_get($typeid);
		if(!is_array($remotedata)){
			mikulog('Remote API cannot hold.','ERROR');
			return false;
		}
		$predictword = '今天是'.$remotedata['Riqi'].'，'.$remotedata['Msg'].'[兔子]...'.$remotedata['Zy'];
		echo $predictword."\n";
		repost($myatinfo['idstr'], $predictword);
		//sayaword($predictword,array(WB_ID_MASTER_USERNAME));
	}else{
		echo "debug:nothing~\n got content: $myatinfo[text]";
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
		$getsince_id = file_get_contents(WB_FILE_SINCE_ID);
		if($getsince_id > 0){
			$since_id = $getsince_id;
		}
	}
	$o = new SaeTClientV2( WB_AKEY , WB_SKEY , WB_TOKEN);
	//$o->set_debug(true);
	$rs = $o->mentions(1,50,$since_id);
	$myatinfo = $rs['statuses'][0];
	if(is_array($myatinfo)){
		mikulog("got myatinfo, start to analy...",'DEBUG');
		analy($myatinfo);
		file_put_contents(WB_FILE_SINCE_ID, $myatinfo['idstr']);
	}else{
		return false;
	}
	//$debuginfo = var_export($rs);
	//file_put_contents('test.txt', $debuginfo);
	return $rs['statuses'];
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



?>