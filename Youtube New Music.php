<?php
	$videos = array();
	$arguments = 'sort=top&t=week';
	$json = file_get_contents('http://www.reddit.com/r/listentothis/top/.json?' . $arguments);
	$obj = json_decode($json);
	foreach($obj->data->children as $single){
		if(strpos($single->data->domain,'youtube') !== false){
			$ar = preg_split('/watch\?v=/', $single->data->secure_media->oembed->url);
			$ar = preg_split('/\//', $ar[1]);
			array_push($videos, $ar[0]);
		}
	}
?>

<div id="playerContainer">
	<div id="player"></div>
	<div id="myControls">
		<div id="currentlyPlaying"></div>
		<button style="margin-top:10px;" onClick="previous()">Previous!</button>
		<button style="margin-top:10px;" onClick="next()">Next!</button>
	</div>
</div>

<script>
	videos = <?php echo json_encode($videos); ?>;
	var tag = document.createElement('script');
	tag.src = "https://www.youtube.com/iframe_api";
	var firstScriptTag = document.getElementsByTagName('script')[0];
	firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
	var player;
	function onYouTubeIframeAPIReady() {
	player = new YT.Player('player', {
		height: '390',
		width: '640',
		videoId: videos[0],
		events: {
		'onReady': onPlayerReady,
		'onStateChange': onPlayerStateChange,
		'onPlaybackQualityChange' : onPlayerPlaybackQualityChange,
		'onError' : onPlayerError
		}
	});
	}
	function onPlayerReady(event) {
	}
	current = 1;
	manualQuality = false;
	document.getElementById("currentlyPlaying").innerHTML = 'Currently Playing: 1 of ' + videos.length;
	function onPlayerStateChange(event) {
	  	if (event.data == YT.PlayerState.ENDED) {
			player.loadVideoById({
				videoId: videos[current],
				startSeconds: 0
			});
			player.playVideo();
	    	document.getElementById("currentlyPlaying").innerHTML = 'Currently Playing: ' + (current+1) + ' of ' + videos.length;
			++current;
			if(current >= videos.length){
				current = 0;
			}
	    }
	    if (event.data == YT.PlayerState.BUFFERING && !manualQuality) {
	        event.target.setPlaybackQuality('hd1080');
	    }
	}
	function onPlayerPlaybackQualityChange(event){
		if(player.getCurrentTime() > 1){
			manualQuality = true;
		}
  	}
	function stopVideo() {
		player.stopVideo();
	}
	function next(){
		player.seekTo(player.getDuration());
	}
	function previous(){
		--current;
		--current;
		if(current < 0){
			current = videos.length-1;
		}
		player.seekTo(player.getDuration());
	}
	function onPlayerError(){
		player.loadVideoById({
			videoId: videos[current],
			startSeconds: 0
		});
		player.playVideo();
	    document.getElementById("currentlyPlaying").innerHTML = 'Currently Playing: ' + (current+1) + ' of ' + videos.length;
		++current;
		if(current >= videos.length){
			current = 0;
		}
	}
</script>