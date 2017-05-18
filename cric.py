from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()
import json
import requests
import pprint 
import csv
import os
from flask import Flask, request, make_response
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):

	with open('PlayerData.csv', 'rt') as csvfile:
		csv_id = csv.reader(csvfile)
		for row in csv_id:
			if(row[0]==req['result']['parameters']['PlayerData']):
				pid=row[4]
	info={'pid':pid,'apikey':'9RNVu0DPMcajGAsFXW0JDYVMg4L2'}
	final=requests.get('http://cricapi.com/api/playerStats',params=info)
	output = json.loads(final.text)
	formatg=req['result']['parameters']['format']
	stats=req['result']['parameters']['Stats']
	if stats="Econ" or stats="Wkts" :
	answer=output['data']['bowling'][formatg][stats]
	elif stats="Runs"or stats="Ct"or stats="SR" :
	answer=output['data']['bowling'][formatg][stats]

	speech = "The player has the following stats"+" " +answer

	print("Response:")
	print(speech)

	return {
		"speech": speech,
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')



















