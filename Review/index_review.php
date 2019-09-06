<?php
# This code is a compliment to "Covert lie detection using keyboard dynamics".
# Copyright (C) 2017  QianQian Li
# See GNU General Public Licence v.3 for more details.
session_start();
require_once ('config_review.php'); 
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
    
    <body onload="FocusOnInput()">
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
            //generate the sequence of quesitons          
            $question_Sequence = range(0,1);
            //convert an array to string
            $string_Sequence = implode(",",$question_Sequence);
            //create the starttime of session
            date_default_timezone_set('Europe/Rome');
            $date_CreateSession = date('Y/m/d H:i:s', time());
            // check information of devices
            $useragent=$_SERVER['HTTP_USER_AGENT'];
            if(!preg_match('/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i',$useragent)||preg_match('/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i',substr($useragent,0,4)))
            {
                $devices = "computer"; 
            }
            else{
                $devices = "smartphone";
            }
            $sql_Register=mysqli_query($conn, "insert into sessions_long(mind_condition,device_info,question_ids_sequence,current_question_index,completed,start_time) values('".$_POST['subjectCondition']."','".$devices."','".$string_Sequence."','0','0','". $date_CreateSession."')");           
            $last_id = mysqli_insert_id($conn);
            $_SESSION['subject']=$last_id;
            if($sql_Register){
                //attention: jump to the member.php, put sth into the session
                echo "<script>location='Inf_realtest_review.php';</script>";
                mysqli_close($conn);
            }
            else{
                echo "<script>alert('Fail to login the website.');location='index.php';</script>";
                mysqli_close($conn);           
            }       
        } 
        else{
        ?>
        <div class="col-xs-offset-1 col-xs-10">            
        <div align="center" bgcolor="#EBEBEB">
	Test b(fake review) <br>
	We will ask participants to write a review, to be completed through their smartphone, by filling in a form that replicates the Amazon review one. The three scenarios involved in this second test are the following ones: one-third of the participants will be asked to think about the latest product they bought online and to compile the form by providing a true review (scenario b1); one-third of the participants will have to think about the latest product they bought online and then provide a fake review (scenario b2); one-third of the participants will be shown a product, that is unlikely they have bought before, and they will have to provide a fake review (scenario b3). For the experiment, please keep the phone in your hand (not on the table). <br>
	The experiment works only with Chrome, if you are using an iPhone, please go to Settings > Safari > Privacy and Security and put the Motion & Orientation Access toggle on. Good luck!<font color="#FF0000">*campo obbligatorio</font><br/></br/></div>   
           <form class="form-horizontal" action="" method="post" name="theForm" style="margin-bottom: 0px;" onsubmit="return chk(this)" autocomplete="off">     
            <div class="form-group">
                    <label for="subjectCondition" class="col-xs-3 control-label">Condizione:<font color="#FF0000">*</font></label>
                    <div class="col-xs-9 ">
                    <label class="radio-inline">
                        <input name="subjectCondition" type="radio" id="0" value=0 checked="checked" />Sincero</label>
                    <label class="radio-inline">
                        <input type="radio" name="subjectCondition" value=1 id="1" />Mentitore (conoscere il prodotto)</label>
                    <label class="radio-inline">
                        <input type="radio" name="subjectCondition" value=2 id="2" />Mentitore (senza conoscere il prodotto)</label>
                    </div>
            </div>                    
        <div class="col-xs-12">
         <input class="btn btn-info btn-lg col-xs-5" type="submit" name="submitRegister" id="submitRegister" value="Registrati"></input>
         <input class="btn btn-info btn-danger col-xs-offset-1 col-xs-5" type="reset" name="button" id="button" value="Cancella" ></input>
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