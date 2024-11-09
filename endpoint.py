from flask import Flask, request, jsonify
from chord_identifier import ChordIdentifier  # Assuming you have this class
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/identify-chord', methods=['POST'])
def identify_chord():
    data = request.json  # Expecting data to be JSON
    notes = data.get('notes', [])  # Get the list of notes from the JSON
    chord_identifier = ChordIdentifier(notes)  # Your ChordIdentifier class instance
    chord = chord_identifier.chordIdentity
    return jsonify({'chord': chord})

if __name__ == '__main__':
    app.run(debug=True)
