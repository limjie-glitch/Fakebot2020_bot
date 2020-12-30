server_url = "https://49d6ae89e683.ngrok.io/fakebox/check"
#user_url = "https://www.browserstack.com/guide/python-selenium-to-run-web-automation-test"
#user_title = ""
#user_content = ""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/geturl/", methods=["GET", "POST"])
def respond():
	if request.method=='GET':
		link = request.args.get("link", None)
		print(f"got link {link}")
		response = {}
		if not link:
			response["ERROR"] = "no link found, please enter link"
		else:
			response["MESSAGE"] = f"You have entered {link} on our awesome platform!!"
		return jsonify(response)

	elif request.method=='POST':
		# user inputs
		url_post = request.form.get("link")
		title_post = request.form.get("title")
		content_post = request.form.get("content")
		# snatchbot required
		user_id_post = request.form.get("user_id")
		bot_id_post = request.form.get("bot_id")
		module_id_post = request.form.get("module_id")

		print(f"post url {url_post}")
		print(f"user d {user_id_post}")

		#validate entry
		if url_post or title_post or content_post:
			myobj = {'url': url_post,
					'title': title_post,
					'content': content_post}

			x = requests.post(server_url, data = myobj)
			print(x.text)

			#define extraction function
			def json_extract(obj, key):
			    arr = []
			    def extract(obj, arr, key):
			        if isinstance(obj, dict):
			            for k, v in obj.items():
			                if isinstance(v, (dict, list)):
			                    extract(v, arr, key)
			                elif k == key:
			                    arr.append(v)
			        elif isinstance(obj, list):
			            for item in obj:
			                extract(item, arr, key)
			        return arr
			    values = extract(obj, arr, key)
			    return values
			domain = str(json_extract(x.json(), 'domain'))
			domain_slice = domain[2:-2]
			category = str(json_extract(x.json(), 'category'))
			category_slice = category[2:-2]
			decision = str(json_extract(x.json(), 'decision'))
			decision_slice = decision[2:-2]

			#if url is inserted
			if url_post:
				if category_slice != "credible" or category_slice != "trusted":
					return_myobj = {"user_id": user_id_post,"bot_id": bot_id_post,"module_id": module_id_post,"message": "The link that you have authenticated is CREDIBLE. Feel free to browse the content freely!","suggested_replies": ["Next"],"blocked_input": "false"}
					return jsonify(return_myobj)
				else:
					return_myobj = {"user_id": user_id_post,"bot_id": bot_id_post,"module_id": module_id_post,"message": "The link that you have authenticated is UNRELIABLE. You may want to be wary of the content you are browsing.","suggested_replies": ["Next"],"blocked_input": "false"}
					return jsonify(return_myobj)
			#if title or content is inserted		
			else:
				if decision_slice == "bias":
					return_myobj = {"user_id": user_id_post,"bot_id": bot_id_post,"module_id": module_id_post,"message": "The text that you have authenticated is BIASED. You may want to be wary of the content you are browsing.","suggested_replies": ["Next"],"blocked_input": "false"}
					return jsonify(return_myobj)
				elif decision_slice == "impartial":
					return_myobj = {"user_id": user_id_post,"bot_id": bot_id_post,"module_id": module_id_post,"message": "The text that you have authenticated is IMPARTIAL. Feel free to browse the content freely!","suggested_replies": ["Next"],"blocked_input": "false"}
					return jsonify(return_myobj)
				elif decision_slice == "unsure":
					return_myobj = {"user_id": user_id_post,"bot_id": bot_id_post,"module_id": module_id_post,"message": "We are UNSURE about the text that you have authenticated.","suggested_replies": ["Next"],"blocked_input": "false"}
					return jsonify(return_myobj)

		#error entry
		else:
			return_myobj_error = {"user_id": user_id_post,"bot_id": bot_id_post,"module_id": module_id_post,"message": "No data validated","suggested_replies": ["Retry"],"blocked_input": "false"}						
			return jsonify(return_myobj_error)

@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
	app.run(threaded=True, port=5000)
#title = driver.find_element_by_name("title")
#title.send_keys(user_title)

#content = driver.find_element_by_name("content")
#content.send_keys(user_content)

#RETURN JSON

#RETURN CONTENT