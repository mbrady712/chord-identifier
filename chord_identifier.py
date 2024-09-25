import itertools

def get_notes():
    notes = input("Enter the notes separated by spaces (e.g., C E G): ")
    return notes.split()


def notes_to_semitones(notes):
    note_to_semitone = {
        'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5,
        'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
    }
    return [note_to_semitone[note] for note in notes]

def find_intervals(allInversions, chordIter):
    noteIter = 0
    intervals = []
    numIntervals = len(allInversions[chordIter]) - 1
    currentSemitone = 0
    nextSemitone = 0
    while noteIter < numIntervals:
        currentSemitone = allInversions[chordIter][noteIter]
        nextSemitone = allInversions[chordIter][noteIter + 1]
        if(currentSemitone > nextSemitone):
            nextSemitone += 12
        intervals.append(nextSemitone - currentSemitone)
        noteIter = noteIter + 1
    return intervals
    

def find_root(semitones):
    allInversions = [list(permutation) for permutation in itertools.permutations(semitones)]
    root = 0
    chordIter = 0
    rootFound = False
    while rootFound == False:
        #Get intervals of permutations
        if(chordIter < len(allInversions)):
            intervals = find_intervals(allInversions, chordIter)
        #See if the permutation has all thirds (i.e. is in root position)
        allThirds = True
        for interval in intervals:
            if(interval != 3 and interval != 4):
                allThirds = False
        #Set root to root of chord
        if(allThirds):
            root = allInversions[chordIter][0]
            rootFound = True
        chordIter += 1
    return root



notes = get_notes()
semitones = notes_to_semitones(notes)
print(find_root(semitones))


