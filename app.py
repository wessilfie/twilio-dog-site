from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, make_response
from card import read_data
from definitions import definitions
import yaml 

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
	return render_template('home.html')

@app.route("/topics/<topic>", methods=['GET'])
def topic(topic):
	#modfify topic to match format in definitions.py file
	topic_modified = modify_topic(topic)
	#check dictionary of topics to verify user trying to find a valid topic
	# Return 404 if user goes to an invalid page
	if topic_modified not in definitions:
		error = "Unfortunately, we couldn't find the page you searched for."
		return render_template('home.html', error=error), 404
	definition = definitions[topic_modified][0]
	definition_link = definitions[topic_modified][1]
	title_placement = topic.title()
	resources = read_data(topic_modified)
	return render_template('topic.html', topic=topic, title=title_placement,
	definition=definition ,resources=resources, definition_link=definition_link)



@app.route("/api/search/<string:topic>", methods=['GET'])
def get_data(topic):
	if len(topic) == 0 or topic is None:
		return api_return_404()
	topic_modified = modify_topic(topic)
	file_path = "data/{0}.yml".format(topic_modified)
	
	# if the topic the user queried for does not exist, return a 404 error
	if topic_modified not in definitions:
		return api_return_404()

	try: 
		# read in file 
		with open(file_path, 'r') as yml_data:
			try:
				#convert file to dictionary
				data = yaml.safe_load(yml_data)
				return jsonify({'response': 200, 'results': data['data'][topic_modified]})
			except:
				return api_return_404()
	
	#return 404 if reading file not found 
	except:
		return api_return_404()	



@app.route("/api/topics", methods=['GET'])
def get_topics():
	return jsonify({'response': 200, 'results': list(definitions.keys())})

# Return 404 if user goes to an invalid page
@app.errorhandler(404)
def page_not_found(e):
	error = "We couldn't find the page you searched for."
	return render_template('home.html', error=error), 404

#modify topic to match format in definitions.py file
def modify_topic(topic):
	#replace all spaces with underscores and lowercase result
	return topic.replace(" ", "_").lower()

def api_return_404():
	return make_response(jsonify({'response': 404, 'results': 'No data returned for this topic.'}), 404)	

if __name__ == "__main__":
	app.run(debug=True)