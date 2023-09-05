from flask import Flask, request, jsonify
import pandas as pd

# Load your data frame from a CSV file
data = pd.read_csv('./res/Student.csv')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'System is running'


@app.route('/get_message', methods=['POST'])
def get_message():
    request_data = request.json  # Assuming you are sending JSON data

    registration_number = request_data.get('registration_number')

    if registration_number is None:
        return jsonify(message='Missing registration_number in request'), 400

    # Search for the registration number in your data frame
    result = data[data['RegistrationNumber'] == registration_number]

    if result.empty:
        return jsonify(message='Registration number not found'), 404
    else:
        message = result.iloc[0]['Message']
        return jsonify(message=message), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)