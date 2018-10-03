# LCO_Scheduling
Scripts for the scheduling and managing LCO requests

USAGE
To use these scripts you need to have a file called token.txt with just your LCO authentacation token in it.  You can learn how to get this token here:
https://developers.lco.global/

Some example usage:

       python lco_cancel_target.py -p CLN2018B-004 -t HATS747-029
(lists the requests for target HATS747-029, but will NOT cancel them.)       

       python lco_cancel_target.py -p CLN2018B-004 -t HATS747-029 -kill yes
(lists the requests for target HATS747-029, and will cancel them.)       

       python lco_requests.py -p KEY2017AB-003d -u daniel_bayliss1 -s COMPLETED
(lists the requests for this proposal/user/status.)       
