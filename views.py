# from crypt import methods
# from pydoc import render_doc
# from turtle import title
from flask import render_template, request, jsonify
# from numpy import histogram_bin_edges
from __init__ import app
import chatbot
# import json

chatlog = []

@app.route('/')
def index():
    my_dict = {
        'insert_something1' : "Hi I'm something!",
        'insert_something2' : "Hello I'm somekind!",
        'test_titles' : ['title1', 'title2', 'title3']
    }
    return render_template('app/index.html', my_dict=my_dict)

@app.route('/chat', methods=['POST', 'GET'])
def other2():
    return render_template('app/chat_interface.html')

@app.route('/ai_intereact', methods=['POST'])
def ai_intereact():
    if request.method == 'POST':
        try:
            print("---------------------")
            message = request.form["message"]
            print("Message:", message)
            response, emo = chatbot.main(message)
            print("Response:", response, "\nEmotion:", emo)
            print("---------------------")
        except:
            response = "ERROR"
        dict = {"who": "ai", "message": str(response), "emo": str(emo)}
        
    return jsonify(dict)

@app.route('/genVoice', methods=['POST'])
def genVoice():
    if request.method == 'POST':
        try:
            response = request.form["message"]
            response = chatbot.generate_wav(response)
        except:
            response = "ERROR"
    return response

@app.route('/delAudio', methods=['POST'])
def delAudio():
    if request.method == 'POST':
        try:
            id = request.form["id"]
            chatbot.delAudio(id)
        except:
            pass
    return ('', 204)

@app.route('/contact')
def other1():
    return render_template('app/contact.html')