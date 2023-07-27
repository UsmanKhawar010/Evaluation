import traceback
from flask import Flask, request, render_template

class ML:
    def __init__(self):
        self.available_models = {
            "face_detection": "/additional_drive/ML/face_detection",
            "car_detection": "/additional_drive/ML/car_detection",
            "shoe_detection": "/additional_drive/ML/shoe_detection",
            "cloth_detection": "/additional_drive/ML/cloth_detection",
            "signal_detection": "/additional_drive/ML/signal_detection",
            "water_level_detection": "/additional_drive/ML/water_level_detection",
            "missile_detection": "/additional_drive/ML/missile_detection"
        }
        self.loaded_models_limit = 2
        self.loaded_models = {
            model: {
                "path": self.available_models[model],
                "count": 0
            }
            for model in list(self.available_models)[:self.loaded_models_limit]
        }

    def load_weights(self, model):
        return self.available_models.get(model, None)

    def load_balancer(self, new_model):
        if new_model in self.loaded_models:
            self.loaded_models[new_model]['count'] += 1
            return self.loaded_models
        else:
            if new_model not in self.loaded_models and new_model in self.available_models:
                least_freq_model = min(self.loaded_models, key=lambda x: self.loaded_models[x]['count'])
                del self.loaded_models[least_freq_model]
            self.loaded_models[new_model] = {
                "path": self.load_weights(new_model),
                "count": 1
            }
            return self.loaded_models
            
            
            
            
app = Flask(__name__)
ml = ML()

@app.route('/', methods=['GET', 'POST'])
def get_loaded_models():
    return render_template("model.html")

@app.route('/process_request', methods=['POST'])
def process_request():
    try:
        model = request.form.get("model")
        ml.load_balancer(model)
        return (ml.loaded_models)
    except:
         return str(traceback.format_exc())

app.run(host='127.0.0.1', port=5000, debug=True)
