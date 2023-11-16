import cv2
import numpy as np
import os

class Estacionamento:
    def __init__(self):
        self.vaga1 = [1, 89, 150, 150, False]
        self.vaga2 = [151, 89, 150, 150, False]
        self.vaga3 = [300, 89, 150, 150, False]
        self.vagas = [self.vaga1, self.vaga2, self.vaga3]

        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

    def run(self):
        while True:
            check, img = self.video.read()
            if not check:
                break 

            imgCinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgTh = cv2.adaptiveThreshold(imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
            imgBlur = cv2.medianBlur(imgTh, 5)
            kernel = np.ones((3, 3), np.uint8)
            imgDil = cv2.dilate(imgBlur, kernel)

            for i, (x, y, w, h, ocupada) in enumerate(self.vagas):
                recorte = imgDil[y:y + h, x:x + w]
                vaga = cv2.countNonZero(recorte)
                cv2.putText(img, f'Vaga {i + 1}: {vaga}', (x, y + h - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

                if vaga > 2000:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    self.vagas[i][4] = True
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    self.vagas[i][4] = False

                #os.system("cls")
                #print(f"Vaga 1 {self.vaga1[4]}")
                #print(f"Vaga 2 {self.vaga2[4]}")
                #print(f"Vaga 3 {self.vaga3[4]}")

            cv2.imshow('video', img)
            cv2.imshow('video TH', imgDil)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break 

        self.video.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    app = Estacionamento()
    app.run()