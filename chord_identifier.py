import itertools

def get_notes():
    notes = input("Enter the notes separated by spaces (e.g., C E G): ")
    return notes.split()

note_to_semitone = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5,
    'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
}

semitone_to_note = {
    0: 'C', 1: 'C#', 1: 'Db', 2: 'D', 3: 'D#', 3: 'Eb', 4: 'E',5: 'F', 6: 'F#', 6: 'Gb',
    7: 'G', 8: 'G#', 8: 'Ab', 9: 'A', 10: 'A#', 10: 'Bb', 11: 'B'
}

def notes_to_semitones(notes):
    return [note_to_semitone[note] for note in notes]

def get_note_from_semitone(semitone):
    if semitone in semitone_to_note:
        # Return the first note in the list for that semitone
        return semitone_to_note[semitone][0]
    else:
        return "Invalid semitone value"

def find_intervals(semitones):
    noteIter = 0
    intervals = []
    numIntervals = len(semitones) - 1
    currentSemitone = 0
    nextSemitone = 0
    while noteIter < numIntervals:
        currentSemitone = semitones[noteIter]
        nextSemitone = semitones[noteIter + 1]
        if(currentSemitone > nextSemitone):
            nextSemitone += 12
        intervals.append(nextSemitone - currentSemitone)
        noteIter = noteIter + 1
    return intervals
    

def find_rootPos(semitones):
    allInversions = [list(permutation) for permutation in itertools.permutations(semitones)]
    rootPositionSemitones = []
    root = 0
    currentInversionIntervals = []
    chordIter = 0
    rootFound = False
    while rootFound == False:
        #Get intervals of permutations
        if(chordIter < len(allInversions)):
            currentInversionIntervals = allInversions[chordIter]
            intervals = find_intervals(currentInversionIntervals)
        #See if the permutation has all thirds (i.e. is in root position)
        allThirds = True
        for interval in intervals:
            if(interval != 3 and interval != 4):
                allThirds = False
        if(allThirds):
            rootPositionSemitones = allInversions[chordIter]
            rootFound = True
        chordIter += 1
    return rootPositionSemitones

def find_quality(rootPositionSemitones):
    quality = "Unknown chord"
    intervals = find_intervals(rootPositionSemitones)
    chordQualities = {
        "major": [4, 3],
        "minor": [3, 4],
        "augmented": [4, 4],
        "diminished": [3, 4],
        "major 7": [4, 3, 4],
        "dominant 7": [4, 3, 3],
        "minor 7": [3, 4, 3],
        "diminished 7": [3, 3, 3],
        "minor-major 7": [3, 4, 4],
        "half-diminished 7": [3, 3, 4]
    }
    for key, value in chordQualities.items():
        if value == intervals:
            quality = key
    return quality

notes = get_notes()
semitones = notes_to_semitones(notes)
rootPosition = find_rootPos(semitones)
root = get_note_from_semitone(rootPosition[0])
quality = find_quality(rootPosition)
print(f"{root} {quality}")

