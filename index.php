<?php
# This code is a compliment to "Covert lie detection using keyboard dynamics".
# Copyright (C) 2017  QianQian Li
# See GNU General Public Licence v.3 for more details.
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta content="yes" name="apple-mobile-web-app-capable">
        <meta name="viewport" content="width=device-width,height=device-height,inital-scale=1.0,maximum-scale=1.0,user-scalable=no;">
        <title>Welcome Page</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
        <link rel="Shortcut Icon" href="favicon.ico"/>
    </head>
    
        <div class="container-fluid">
            <div class="row-xs">
                <div class="col-xs-3 pull-left"><img alt="Unipd" src="images/unipd_1.jpg" class="img-responsive"></div>
                <div class="col-xs-3 pull-right"><img alt="HIT" src="images/HIT_logo_1.png" class="img-responsive"/></div>
            </div>
        </div>
        <table width="100" border="0" align="center" cellpadding="0" cellspacing="0">
          <tr>
            <td height="5"></td>
          </tr>
        </table>

        <?php
        if (isset($_POST["submitRegister"])){
            $formChoice=$_POST['formChoice'];
            if($formChoice == "True"){
                //attention: jump to the member.php, put sth into the session
                echo "<script>location='Questionnaire/index_questionnaire.php';</script>";
            }
            else{
                echo "<script>location='Review/index_review.php';</script>";
            }                  
        } 
        else{
        ?>
        <div class="col-xs-offset-1 col-xs-10">            
        <div align="center" bgcolor="#EBEBEB"><font color="#FF0000">*campo obbligatorio</font><br/></br/></div>   
           <form class="form-horizontal" action="" method="post" name="theForm" style="margin-bottom: 0px;" onsubmit="return chk(this)" autocomplete="off">     
            <div class="form-group">
                    <label for="formChoice" class="col-xs-3 control-label">Esperimento:<font color="#FF0000">*</font></label>
                    <div class="col-xs-9 ">
                    <label class="radio-inline">
                        <input name="formChoice" type="radio" id="0" value="True" checked="checked" /> Questionnaire</label>
                    <label class="radio-inline">
                        <input type="radio" name="formChoice" value="False" id="1" />Review</label>
                    </div>
            </div>                     
        <div class="col-xs-12">
         <input class="btn btn-info btn-lg col-xs-5" type="submit" name="submitRegister" id="submitRegister" value="Convalidare"></input>
         </div>
        </form>
        </div>
      <?php
        }
       ?>
    <table width="100" border="0" align="center" cellpadding="0" cellspacing="0">
        <tr>
          <td height="5"></td>
        </tr>
    </table>      
     <div class="col-xs-offset-1 col-xs-10 footer"id="footer">
            <div id="footnote">
                <div class="sectiona">@ 2015 TruthOrLie Test. All rights reserved.
                </div>
                <div class="sectionb"></div>
            </div>
        </div>
        <script src="js/jquery-1.11.3.js"></script>
        <!-- Latest compiled and minified JavaScript -->
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>      
    </body>
</html>