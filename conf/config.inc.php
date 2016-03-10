<?php 

//a simple reminder robot in php .
//design for weibo to make it seems not so alone.
//chibimiku@TSDM.net

if(!defined('AOICHAN_RUNNING')){
	exit('Access deined');
}

//common set.
date_default_timezone_set('Asia/Shanghai');

//config area.
$mysql_username = 'root';
$mysql_password = '';

//weibo config
define( "WB_AKEY" , 'xxxxxxxxxx' );
define( "WB_SKEY" , 'xxxxxxxxxxxxxxxxxxxxxxxxx' );
define( "WB_CALLBACK_URL" , 'http://xxxxxxxxxxxx/callback.php' );

//filepath config
$imgpath = '/data/image/';


?>