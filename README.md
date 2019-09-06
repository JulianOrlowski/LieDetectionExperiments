# LieDetectionExperiments

Welcome to the Lie Detection Project!

Warning: you must be in the /var/www/html directory.

We can distinguish two experiments:

 - One which simulates a questionnaire about subject's identity. The files about that experiment are:
   - config.php
   - experiment.php
   - index_questionnaire.php
   - Inf_realtest.php
   - Inf_warmup.php

 - One which simulates a review form. The files about that experiment are:
   - config_review.php
   - experiment_review.php
   - index_review.php
   - Inf_realtest_review.php
   - product_presentation.php

Other files are common to both experiments.

To set up experiments, you must change values of $basename, $basepass and $database in config.php and config_review.php.

To generate a public URL, you have be in the ~ directory and to type that command: ./ngrok http 80.

The subject must connect the https url.