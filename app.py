from flask import Flask, request, jsonify
import pandas as pd

# Load your data frame from a CSV file
data = pd.read_csv('./res/Student.csv')

app = Flask(__name__)

# Define the constant filename for the CSV file.
CSV_FILENAME = 'Student.csv'
UPLOAD_FOLDER = 'res'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload directory if it doesn't exist.
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET'])
def index():
    return 'System is running'


@app.route('/upload', methods=['POST'])
def upload_csv():
    # Check if a file was submitted with the request.
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    # Check if the file has a valid filename.
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Check if the file is a CSV file.
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must have a .csv extension'}), 400

    # Save the uploaded CSV file to the constant filename.
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], CSV_FILENAME))

    return jsonify({'message': 'File uploaded and replaced successfully'}), 200


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
