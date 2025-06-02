from flask import Flask

# Import blueprints
from patients import patients_bp
from doctors import doctors_bp
# Import other blueprints here...

app = Flask(__name__)

# Register blueprints
app.register_blueprint(patients_bp)
app.register_blueprint(doctors_bp)
# Register others here...

@app.route('/')
def home():
    return "Welcome to Hospital Management"

if __name__ == '__main__':
    app.run(debug=True)
