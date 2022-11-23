# Kroger Sale Monitor

Flask backend API + price check and email alert system. 
<br><br>
Users curate an inventory of products with desired pricing.  The UI denotes items meeting the pricing thresholds. The
email alert system (checker) can be scheduled to evaluate and alert users during runtime.  The system relies on existing
email providers by using SMTP. Current configuration assumes a gmail account. 
<br><br>
Users can receive text messages by using their mobile carrier's email SMS gateway e.g. <phone_number>@vtext.com for Verizon.

frontend: https://github.com/RyanEliopoulos/kroger_sale_monitor_FE <br>
Instance: https://ryanpaulos.dev/apps/sale_monitor

## Environment Variables
#### Kroger App OAuth
Communicator.py <br>
&nbsp;&nbsp;&nbsp;&nbsp;sale_monitor_client_id <br>
&nbsp;&nbsp;&nbsp;&nbsp;sale_monitor_client_secret <br>

#### Alert system
notifier.py  <br>
&nbsp;&nbsp;&nbsp;&nbsp;ip_alert_email <br>
&nbsp;&nbsp;&nbsp;&nbsp;ip_alert_email_pw <br>


## Deployment
Assuming Linux: <br>
(1) Install pipenv and run init.sh. <br>
(2) Use wsgi.py as the WSGI server entry point. <br>
(3) schedule price_check.sh.


