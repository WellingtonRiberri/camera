import requests
import schedule
import time

def atualizar_status_vagas():
    # Aqui você coloca a lógica para detectar o status das vagas, por exemplo:
    vaga1_ocupada = True
    vaga2_ocupada = False
    vaga3_ocupada = True

    data = {
        'vaga1': vaga1_ocupada,
        'vaga2': vaga2_ocupada,
        'vaga3': vaga3_ocupada
    }

    response = requests.post('http://127.0.0.1:5000', json=data)

    if response.status_code == 200:
        print('Status das vagas atualizado com sucesso!')
    else:
        print('Falha ao atualizar o status das vagas.')

# Agende a função de atualização para ser executada a cada 5 segundos
schedule.every(5).seconds.do(atualizar_status_vagas)

while True:
    schedule.run_pending()
    time.sleep(1)