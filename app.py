import screen_brightness_control as sbc
from math import hypot
import mediapipe as mp
from flask import Flask, render_template, Response, request, make_response
import cv2
import datetime
import time
import os
import sys
import numpy as np
from flask_mysqldb import MySQL
import pdfkit
from threading import Thread

app = Flask(__name__)


global capture, rec_frame, grey, switch, neg, face, rec, out
capture = 0
grey = 0
neg = 0
face = 0
switch = 1
rec = 0


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Hand range 15 - 220
# Brightness range 0 - 100

camera = cv2.VideoCapture(0)


def record(out):
    global rec_frame
    while (rec):
        time.sleep(0.05)
        out.write(rec_frame)


def generate_frames():
    while True:
        # read the camera frame
        global out, capture, rec_frame
        success, frame = camera.read()

        if success:
            if (capture):
                capture = 0
                now = datetime.datetime.now()
                p = os.path.sep.join(
                    ['static/images', "shot_{}.png".format(str(now))])
                cv2.imwrite(p, frame)

            try:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass

        else:
            pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/kirim', methods=['POST', 'GET'])
def kirim():
    global nama_pasien, usia_pasien
    output = request.form.to_dict()
    nama_pasien = output["nama_pasien"]
    umur_pasien = output["umur_pasien"]
    no_pasien = output["no_pasien"]

    return render_template('preview.html',  nama_pasien=nama_pasien, umur_pasien=umur_pasien, no_pasien=no_pasien)


@app.route('/fiturCamera', methods=['POST', 'GET'])
def fiturCam():
    global switch, camera, capture
    capture = 0
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            capture = 1
        else:
            capture = 0
        # elif request.form.get('stop') == 'Simpan':

        #     if (switch == 1):
        #         switch = 0
        #         camera.release()
        #         cv2.destroyAllWindows()

        #     else:
        #         camera = cv2.VideoCapture(0)
        #         switch = 1

    elif request.method == 'GET':
        return render_template('preview.html')

    if capture == 1:
        nama_pasien = request.form.get('nama_pasien')
        umur_pasien = request.form.get('umur_pasien')
        no_pasien = request.form.get('no_pasien')

        current_datetime = datetime.datetime.now()
        tanggal = current_datetime.date()
        jam = current_datetime.time()

        # Membaca frame dari kamera
        ret, frame = camera.read()

        if ret:
            # Membuat nama file dengan format: nama_pasien-tanggal-jam.jpg
            file_name = f"{nama_pasien}.jpg"

            direk_path = os.path.join("static", "images", "diagnosa")

            path = os.path.join(direk_path, file_name)
            # Menyimpan gambar
            cv2.imwrite(path, frame)
            # Menutup kamera
            camera.release()
            cv2.destroyAllWindows()

    return render_template('results.html', file_name=file_name, path=path, nama_pasien=nama_pasien, umur_pasien=umur_pasien, no_pasien=no_pasien)


@app.route('/simpan', methods=['POST'])
def hasil():
    if request.method == "POST":
        nama_pasien = request.form['nama_pasien']
        umur_pasien = request.form['umur_pasien']
        no_pasien = request.form['no_pasien']
        path = request.form['path']
        diagnosa = request.form['diagnosa']

        nama_file = "data_pasien/data_pasien.txt"

        # Membuka file untuk menulis
        with open(nama_file, 'a') as file:
            # Format data sebagai string
            data = f"Nama Pasien: {nama_pasien}, Usia: {umur_pasien}, No. Pasien: {no_pasien}, Foto Diagnosa: {path}, Diagnosa: {diagnosa}\n"

            # Menulis data ke dalam file
            file.write(data)

    return render_template('akhir.html', path=path, nama_pasien=nama_pasien, umur_pasien=umur_pasien, no_pasien=no_pasien, diagnosa=diagnosa)


@app.route('/lihat_data', methods=['POST'])
def baca_data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM data_pasien ORDER BY pasien_id DESC")
    data_pasien = cur.fetchall()
    cur.close()

    return render_template('test.html', data_pasien=data_pasien)


@app.route('/generate_pdf', methods=['GET'])
def generate_pdf():
    pdfkit_config = pdfkit.configuration(
        wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

    pdfkit_options = {
        'disable-external-links': True
    }

    html = render_template("akhir.html")
    pdf = pdfkit.from_string(
        html, False, configuration=pdfkit_config,  options=pdfkit_options)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline;filename=output.pdf"

    return response


if __name__ == '__main__':
    app.run()
