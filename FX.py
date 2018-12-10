from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import datetime
from time import sleep
from API import get_result
import threading
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'skasjdlajs@aklsjd2093'
socketio = SocketIO(app)
input_list = []
check = 0
thread_start = 0


def get_rate():
	global check
	with app.test_request_context('/'):
		while check == 1:
			output_list = []
			print("Try to get rate: "+ str(datetime.datetime.now()))
			for items in input_list:
				answer = get_result(str(items))
				if answer < 0:
					output_list.append("Currency pair not founded!")
				else:
					output_list.append(str(answer))
			print("emit: "+ str(datetime.datetime.now()))
			socketio.emit('server_response', {'data': output_list})
			socketio.sleep(1)


@socketio.on('connect_event', namespace = '/')
def joined(message):
	pass


@socketio.on('disconnect', namespace='/')
def do_disconnect():
    global thread_start
    thread_start = 0
    


@socketio.on('client_event', namespace = '/')
def get_FX(message):
	global thread_start
	global check
	global t
	print("received from frontend:" + str(datetime.datetime.now()))
	if (message['option'] == "Add"):
		input_list.append(message['data'])
	else:
		input_list.remove(message['data'])
	check = 1
	if thread_start == 0:
		print("starting thread")
		t = threading.Thread(target = get_rate)
		t.start()
		thread_start = 1
		
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
	debug = True
	socketio.run(app)

