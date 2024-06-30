from flask import Flask, request, jsonify
import os
import time
from constants.constants import Constants 
app = Flask(__name__)

#init classes
DEFAULT_CONSTANTS=Constants()
# Configure the storage folder
UPLOAD_FOLDER = 'storage'
app.config['UPLOAD_FOLDER'] = DEFAULT_CONSTANTS.UPLOAD_FOLDER

# Ensure the storage folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/', methods=['GET'])
def home():
    return "GST EXTRACTION APP RUNNING"

@app.route('/extract', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files.get('file')
        extractionMethod=request.form.get("extractionMethod")
        LLMType=request.form.get("LLMType")

        if not extractionMethod or \
        extractionMethod not in  DEFAULT_CONSTANTS.EXTRACTOR.keys() :
            return jsonify({"error": "Missing Value Extraction Method"}), 400
        
        if not LLMType or \
        LLMType not in DEFAULT_CONSTANTS.LLM.keys() :
            return jsonify({"error": "Missing Value LLM Type"}), 400
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file:
            timestamp = int(time.time())
            _, file_extension = os.path.splitext(file.filename)
            new_filename = f"{os.path.splitext(file.filename)[0]}_{timestamp}{file_extension}"

            # Save the file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(file_path)

            # Print the filename
            print(f"Saved file: {new_filename}")
            print(DEFAULT_CONSTANTS.EXTRACTOR,extractionMethod)
            extractor=DEFAULT_CONSTANTS.EXTRACTOR[extractionMethod]()
            print(extractor)
            extracted_data=extractor.extract(file_path)

            genAI=DEFAULT_CONSTANTS.LLM[LLMType]()
            response=genAI.getLLMResponse(extracted_data)
            
            # Delete the file after extraction is 
            os.remove(file_path)



            return jsonify({"extracted_data": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
