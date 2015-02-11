<?php
	ini_set('precision', 1000);
	$n = 1000000000;
	$variable1 = sin(deg2rad(360/$n));
	$variable2 = sin(deg2rad((180-(360/$n))/2));
	$pi = (($variable1/$variable2)*$n)/2;
	echo("My pi: &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$pi);
	echo("<br>");
	echo("Their pi: &nbsp; &nbsp; &nbsp; &nbsp; ".pi());
	echo("<br><br>");
	echo("I used a polygon of ".$n." sides.");
?>
<br>
Their pi is returned by PHP's pi() function.
<br><br><br>
How it works:<br><br>
I calculated the perimeter of a regular polygon (lets call him Fred) and then divided by 2.<br>
The more sides Fred has, the more accurate the pi.
<br><br><br>
Why it works:<br><br>
Pi is the ratio of the circumference of any circle to its diameter.<br>
Therefore, <b>pi = circumference/diameter.</b><br>
Since this is the same for every circle, let's just use one with a radius of 1 (easier that way).<br>
Now, the diameter is easy, just 2 times the radius. So 2.<br>
But how do you find the circumference?<br>
Well, you could use the formula 2 * pi * radius, of course, but that would defeat the purpose of calculating pi :P.<br>
So to figure this out, we figure out the circle.<br>
What is a circle really, but a polygon with infinite sides.<br>
Fred is trying to be that polygon, but alas, he cannot work with infinites.<br>
So Fred just has <i>a lot</i> of sides, rather than an infinite number.<br>
The more the merrier, of course.<br>
Now, Fred's perimeter is then pretty close to the circumference of a circle, isn't it?<br>
Of course it is! And that's what we're using as an approximation of the circumference.<br>
It's an approximation, but with so many sides, it's a <i>very good</i> approximation.<br>
So we divide Fred's perimiter by 2 (the diameter we got earlier), and we're golden.
<br><br><br><br>
The actual equation used:
<br><br>
pi = (((sin(360/n))/(sin((180-(360/n))/2)))*n)/2
<br><br>
Where n is the number of sides Fred has.<br>
This is, of course, in degrees.
