var request = require('request');
var cheerio = require('cheerio');
var twilio = require('twilio');
var accountSid = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'; //replace w/ real SID
var authToken = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'; //replace w/ real
authToken
var client = new twilio.RestClient(accountSid, authToken);
var requrl = 'http://proshop.innovadiscs.com/mcpro-roc3.html'
var textStr = "McPro Roc3s are in stock again!\n" + requrl;
var status = '';

function rocquest(err, resp, body){         //makes HTTP GET request to
Innova
   if(!err && resp.statusCode == 200){
var $ = cheerio.load(body);
$("p[class~='availability']").each(function(){
  status = this.attribs.class;
  console.log(status);
});
   }}

var sendAlert = function(){           //Sends text message when discs in
stock
   client.messages.create({
body: textStr,
to: '+19705552600,  // Text this number (change as needed)
from: '+19704202600' // From a valid Twilio number
   }, function(err, message) {
if(err) {
  console.error(err.message);
} else {
  console.log(message.sid);
}
   });
};

var mcquery = function(){                 //check status and send text if
available
   request(requrl, rocquest);
   if(status.includes('availability in-stock')){
clearInterval(loop);
sendAlert();
   }
};

var loop = setInterval(mcquery, 30000);     //starts the program by
invoking a loop

