import numpy as np
from flask import Flask, request,send_file
from flask_cors import CORS
import soundfile as sf
import io
import os

app = Flask(__name__)
CORS(app)

@app.route('/generate',methods = ['Post'])

def genrate():
    data = request.json
    base = data.get('base',440)
    diff = data.get('diff',10)
    duration = data.get('duration',60)
    
    sample_rate = 44100
    t = np.linspace(0,duration,int(sample_rate*duration))
    left = np.sin(2*np.pi*base*t)
    right = np.sin(2*np.pi*(base+diff)*t)

    stereo  = np.stack([left,right],axis=1)
    max_val = np.max(np.abs(stereo))
    normalize_stereo = np.int16(stereo/max_val*32767)

    buffer = io.BytesIO()
    sf.write(buffer,normalize_stereo,sample_rate,format='WAV')
    buffer.seek(0)
    return send_file(buffer,mimetype='audio/wav',as_attachment=True,download_name='binaural.wav')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
