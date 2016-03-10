<?php 

//actionset. 

class aoi_actions{
	
	var $friends = array('天使动漫谐星战术研究院');
	
	function joke(){
		//从数据库里取个笑话~
		//库名还是硬编码不要吐槽了真的不要吐槽了再吐槽人家会生气的
		$result = DB::fetch('SELECT * FROM aoi_jokelib ORDER BY RAND() LIMIT 1'); //不是fetch的话稍后改一下，忘了
		sayaword(lang('aoi_joke_tip '.$result['content']), $this->$friends);
	}
	
	function clickrespon(){
		//像rts一样点击后的应答
		$responseindex = rand(0,5);
		sayaword(lang('aoi_response_'.$responseindex), $this->$friends);
	}
	
	function greet(){
		//TODO：获取时间改变不同的greet方式.
		sayaword(lang('aoi_awake_greet_1'), $this->$friends);
	}
	
	function awake_ping(){
		//first action of aoi chan.
		sayaword(lang('aoi_awake_ping'), $this->$friends);
	}
	
	//common_function
	
	function lang($index){
		$langdata = array(
			'aoi_awake_ping'  => 'ping',
			'aoi_awake_greet_1' => 'Hello, it\'s Aoi. How about this day?',
			'aoi_response_0' => '',
			'aoi_response_1' => '',
			'aoi_response_2' => '',
			'aoi_response_3' => '',
			'aoi_response_4' => '',
			'aoi_response_5' => '',
		);
		if(!isset($langdata[$index])){
			return '!'.$index.'!';
		}else{
			return $langdata[$index];
		}
	}
	
	function getsmilepic($smilename){
		//TODO：表情路径从数据中读取.硬编码sucks.
		$smileimgs = array(
			'happy' => 'happy.jpg',
		);		
		
		if(!isset($smileimgs[$smilename])){
			return $smileimgs['default'];
		}else{
			return $smileimgs[$smilename];
		}
	}
	
}



?>