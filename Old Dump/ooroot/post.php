<?php
$connect = mysql_connect("mysql10.000webhost.com", "a8270938_spcr", "sportcrave2013");
if(!$connect){

die(mysql_error());

}

$select_db = mysql_select_db("a8270938_spcr", $connect);

if(!$select_db){

die(mysql_error());
}

$text = $_POST["text"];
$from = $_POST["from"];

mysql_query("INSERT INTO `chat` (
`id` ,
`message` ,
`from`
)
VALUES (
NULL ,  '$text',  '$from'
);");


?>
