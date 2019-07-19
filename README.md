# LieDetectionExperiments

Welcome to the Lie Detection Project!

We can distinguish two experiments:

 - One which simulates a questionnaire about subject's identity. All files concerning that questionnaire are located in the Questionnaire directory.

 - One which simulates a review form. All files concerning that form are in the Review directory.

To run an experiment, you must move files from the directory that concerns your experiment to the parent directory. Once you have finished, just put them in the directory they were.

To do so, you have 4 commands:
 - mvfromreview : put the files from Review/ to the current directory.
 
 - mvfromquestionnaire : put the files from Questionnaire/ to the current directory.
 
 - mvtoreview : put the files concerning the review form from the current directory to Review/
 
 - mvtoquestionnaire : put the files concerning the questionnaire from the current directory to Questionnaire/

To run these commands, you must be in the work directory (/var/www/html).

Here is the list of files and directories common to both projects and which musn't be moved:
 - favicon.ico
 - css files
 - thanks.php
 - images 
 - js