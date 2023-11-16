from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import cv2
import numpy as np
import os
import threading
from camera import Estacionamento

app = Flask(__name__)
socketio = SocketIO(app)
estacionamento = Estacionamento  # A instância será criada mais tarde

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_status', methods=['POST'])
def update_status():
    data = request.get_json()

    if estacionamento is not None:
        vaga1_ocupada = data.get('vaga1', False)
        vaga2_ocupada = data.get('vaga2', False)
        vaga3_ocupada = data.get('vaga3', False)

        estacionamento.vaga1[4] = vaga1_ocupada
        estacionamento.vaga2[4] = vaga2_ocupada
        estacionamento.vaga3[4] = vaga3_ocupada

        return jsonify({
                'vaga1': estacionamento.vaga1[4],
                'vaga2': estacionamento.vaga2[4],
                'vaga3': estacionamento.vaga3[4]
        })
    
    return 

def camera_thread():
    global estacionamento
    estacionamento = Estacionamento()
    estacionamento.run()

if __name__ == "__main__":
    # Inicie a thread da câmera
    camera_thread = threading.Thread(target=camera_thread)
    camera_thread.start()

    # Inicie o servidor Flask e o SocketIO
    socketio.run(app, debug=True)