<?php
$connect = mysql_connect("mysql10.000webhost.com", "a8270938_spcr", "sportcrave2013");
if(!$connect){

die(mysql_error());

}

$select_db = mysql_select_db("a8270938_spcr", $connect);

if(!$select_db){

die(mysql_error());
}
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
        	
        	echo(";margin:5px; padding:5px;-webkit-border-radius: 20px;
-moz-border-radius: 20px;
border-radius: 20px;'>".$messages."</div></div>");
        	$color=$color+1;
        }
    ?>
