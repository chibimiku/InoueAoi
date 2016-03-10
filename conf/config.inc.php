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
$weibo_key = '';

//filepath config
$imgpath = '/data/image/';

?>