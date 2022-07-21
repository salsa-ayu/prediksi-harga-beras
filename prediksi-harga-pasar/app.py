from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__, template_folder='template')

def load_model():
    with open('model_linreg.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

model = load_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form-prediksi')
def form_prediksi():
    return render_template('formpage.html')

@app.route('/prediksi-harga', methods=['POST'])
def predict():
    
    Tahun = float(request.form['Tahun'])
    Bulan = float(request.form['Bulan'])
    kl_beras = float(request.form['kl_beras'])

    hitung = np.array([[Tahun, Bulan, kl_beras]])
    
    prediction = model.predict(hitung)
    output = round(prediction[0], 3)
    
    #versi int
    tahun = int(request.form['Tahun'])
    bulan = int(request.form['Bulan'])
    
    #nentuin kualitas
    if kl_beras == 1:
        kl_beras = "Premium"
    elif kl_beras == 2:
        kl_beras = "Medium"
    else:
        kl_beras = "Luar Kualitas"
    
    return render_template('hasil.html', hasil = output, year = tahun, month = bulan, quality = kl_beras)

if __name__ == '__main__':
    app.run(debug = True)