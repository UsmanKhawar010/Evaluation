import traceback
from flask import Flask
from flask import request,render_template

class ML:
    def __init__(self):
        self.avaliable_models = {
            "face_detection": "/additional_drive/ML/face_detection",
            "car_detection": "/additional_drive/ML/car_detection",
            "shoe_detection": "/additional_drive/ML/shoe_detection",
            "cloth_detection": "/additional_drive/ML/cloth_detection",
            "signal_detection": "/additional_drive/ML/signal_detection",
            "water_level_detection": "/additional_drive/ML/water_level_detection",
            "missile_detection": "/additional_drive/ML/missile_detection"
        }
        self.loaded_models_limit = 5
        self.loaded_models = {
            model: self.load_weights(model)
            for model in list(self.avaliable_models)[:self.loaded_models_limit]
        }
    
    def load_weights(self, model):
        return self.avaliable_models.get(model,None)

    def load_balancer(self, new_model):
        if new_model in self.loaded_models:
            return (self.loaded_models)
        
        else:
            least_freq_model = min(self.loaded_models, key = lambda x: self.loaded_models[x]['count'])
            del self.loaded_models[least_freq_model]
            self.loaded_models[new_model] = self.load_weights(new_model)
            return self.loaded_models            


app = Flask(__name__)
ml = ML()

@app.route('/')
def get_loaded_models():
    return render_template("model.html")


@app.route('/process_request', methods=['GET', 'POST'])
def process_request():
    try:
        model = request.form["model"]
        if model not in ml.loaded_models:
            ml.load_balancer(model)
        return "processed by "+ ml.loaded_models[model]
    except:
        return str(traceback.format_exc())

app.run(host='127.0.0.1', port=5000,debug=True)
