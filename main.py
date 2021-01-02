from flask import Flask, render_template, redirect
import json
import ssl
import http.client
import sys
from keys.hue_keys import *

# Set URL Headers to send
headers = {
    	'cache-control': "no-cache",
}

def getScene(input1):
	params = "/api/" + api_key + "/scenes/" + input1
	conn = http.client.HTTPConnection(url)
	conn.request("GET", params, "", headers)
	r1 = conn.getresponse()
	data1 = r1.read()
	conn.close()
	return data1

def setScene(input1):
	params = "/api/" + api_key + "/groups/1/action"
	payload = "{\"scene\": \"" + input1 + "\"}"
	conn = http.client.HTTPConnection(url)
	conn.request("PUT", params, payload, headers)
	r1 = conn.getresponse()
	data1 = r1.read()
	conn.close()
	return data1

def formatJSON(input1, input2):
	output1 = json.loads(input1)[input2]
	return output1


def getGroupList(scene_list):
    group_list = []
    for x in scene_list:
        try:
            group_num = scene_list[x]['group']
        except:
            continue
        if group_num not in group_list:
            group_list.append(group_num)
    group_list.sort()
    return(group_list)

def printScenes():
    scene_list = json.loads(getScene(""))
    group_list = getGroupList(scene_list)
    for group in group_list:
        print("Group {}:  ".format(group))
        scene_names = []
        for x in scene_list:

            try:
                scene_group = scene_list[x]['group']
            except:
                scene_group = 9999
            if scene_group == group:
                group_lights = scene_list[x]['lights']
                scene_names.append(scene_list[x]['name'])

        print("Lights:  {}".format(group_lights))
        print("Scenes:  {}".format(scene_names))
        print("\n")
        

def setGroupScene(group_name, scene_name='na'):
    group_name = group_name.capitalize()
    scene_name = scene_name.capitalize()
    scene_list = json.loads(getScene(""))
    try:
        group = group_dict[group_name]
        scene_names = []
        for x in scene_list:
            try:
                scene_group = scene_list[x]['group']
            except:
                scene_group = 'N/A'
            if scene_group == group:
                scene_names.append(scene_list[x]['name'])
                if scene_name == scene_list[x]['name']:
                    scene_code = x
        if scene_name in scene_names:
            response = "Setting {} to {}".format(group_name, scene_name)
            setScene(scene_code)
        else:
            response = "Scene name '{}' not found.  Valid options are:  {}".format(scene_name, scene_names)
    except:
        response = "Group name '{}' not found.  Valid options are:  {}".format(group_name, group_dict.keys())

    return(response)
        
        
group_dict = {'All':'0', 'Office':'1', 'Library':'2', 'Calvin':'3'}

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/lights")
def lights():
    return render_template("lights.html")
    
@app.route("/other")
def other():
    return render_template("other.html")
    
@app.route("/about")
def about():
    return render_template("about.html")
    
@app.route("/light_button_1")
def light_button_1():
    setGroupScene('office', 'computer work')
    return redirect('/lights')
    
@app.route("/light_button_2")
def light_button_2():
    setGroupScene('office', 'video call')
    return redirect('/lights')
    
@app.route("/light_button_3")
def light_button_3():
    setGroupScene('office', 'read')
    return redirect('/lights')
    
@app.route("/light_button_4")
def light_button_4():
    setGroupScene('office', 'energize')
    return redirect('/lights')

if __name__ == "__main__":
    app.run(debug=True)