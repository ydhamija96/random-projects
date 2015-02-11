<?php
$connect = mysql_connect("mysql10.000webhost.com", "a8270938_spcr", "sportcrave2013");
if(!$connect){

die(mysql_error());

}

$select_db = mysql_select_db("a8270938_spcr", $connect);

if(!$select_db){

die(mysql_error());
}
?>

<style>

@font-face
{
font-family: ooroot;
src: url('ooroot.ttf'), url('ooroot.eot');
}
body{
        padding:0;
        margin:0;
        font-family:ooroot;
        font-size:2em;
    }
.area{
        border:2px solid black;
        height:70%;
        width:90%;
        overflow:auto;
        font-family:ooroot;
        font-size:2em;
    }
    
    
</style>

<div class="area">
    <?php
         $result = mysql_query("SELECT * FROM chat ORDER BY id DESC");
    		$color=1;
    	while($row = mysql_fetch_array($result)){
        	$messages = $row['message'];
        	$from = $row['from'];
        	echo("<div style='height:100px; padding:10px;'><div style='color:red; float:left; margin:0;'>".$from."</div><div style='float:right; text-align:right; height:80px; overflow:auto;background-color:"); 
        	if($color&1){
        		echo("#DBE9FF; border:2px solid blue");
        		}
        		else{
        		echo("#FFF1DB; border:2px solid red");
        		}
        	
        	echo(";margin:5px; padding:5px;'>".$messages."</div></div>");
        	$color=$color+1;
        }
    ?>
</div>

<form name="form" style="position:absolute; height:50px; bottom:10px; width: 100%;">
    <input type="text" name="name" style="height:100%; width:200px; font-family:ooroot; font-size: 2em; border:2px solid black;" class="name">
    <input type="text" name="message" style="height:100%; width:450px; font-family:ooroot; font-size: 2em; border:2px solid black;" class="message">
    <input type="submit" class="submit" style="height:50px; width:150px; background:grey;">
</form>

<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js">
</script>
<script>
    
$(".submit").click(function(){
    var clientmsg = $(".message").val();
    var name = $(".name").val();  
    $.post("post.php", {text: clientmsg, from: name});                
    $(".message").val("");  
    return false;  
});  

$(document).ready(function () {
        setInterval(function () {
            $(".area").load("log.php");
        }, 2000);
    });
</script>
