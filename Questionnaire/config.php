<?php

# This code is a compliment to "Covert lie detection using keyboard dynamics".
# Copyright (C) 2017  QianQian Li
# See GNU General Public Licence v.3 for more details.


 $hostname="localhost"; //mysql Address
 $basename="phpmyadminuser"; //mysql username
 $basepass="password"; //mysql password
 $database="truth_or_lie"; //mysql database

 $conn=mysqli_connect($hostname,$basename,$basepass)or die("Can not connect to the mysql database"); //connect to mysql
 $classifier="SVM";//RandomForest, SVM, Logistic
 mysqli_select_db($conn, $database); // choose mysql database
 mysqli_query($conn, "set names 'utf8'");//mysql encoding
?>
