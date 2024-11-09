import React, { useState } from 'react';

function ChordIdentifier() {
  // Initialize state with 8 empty strings for the 4 notes and 4 accidentals
  const [notes, setNotes] = useState(Array().fill(''));
  const [chord, setChord] = useState(''); // Stores the identified chord
  const [error, setError] = useState(null); // Stores any error messages

  // Letter names and accidentals options
  const letterOptions = ['', 'C', 'D', 'E', 'F', 'G', 'A', 'B'];
  const accidentalOptions = ['', 'n', 'b', '#', 'd', 'x'];

  // Update state when a dropdown value changes
  const handleDropdownChange = (index, value) => {
    const newNotes = [...notes];
    newNotes[index] = value;
    setNotes(newNotes);
  };

  // Function to handle form submission
  const identifyChord = async (event) => {
    event.preventDefault();
    setError(null); // Reset any previous error
    setChord('');   // Reset any previous chord result

    try {
      const response = await fetch('http://127.0.0.1:5000/identify-chord', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ notes: notes })
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      setChord(data.chord);
    } catch (err) {
      setError(`Failed to identify chord: ${err.message}`);
    }
  };

  return (
    <div>
      <h1>Chord Identifier</h1>
      <form onSubmit={identifyChord}>
        <p>Select notes and accidentals:</p>
        
        {[0, 2, 4, 6].map((i) => (
          <div key={i} style={{ marginBottom: '10px' }}>
            <select
              value={notes[i]}
              onChange={(e) => handleDropdownChange(i, e.target.value)}
            >
              {letterOptions.map((option, index) => (
                <option key={index} value={option}>
                  {option || 'Select Note'}
                </option>
              ))}
            </select>

            <select
              value={notes[i + 1]}
              onChange={(e) => handleDropdownChange(i + 1, e.target.value)}
            >
              {accidentalOptions.map((option, index) => (
                <option key={index} value={option}>
                  {option || 'Select Accidental'}
                </option>
              ))}
            </select>
          </div>
        ))}

        <button type="submit">Identify Chord</button>
      </form>
      
      {chord && <p>Identified Chord: {chord}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default ChordIdentifier;
