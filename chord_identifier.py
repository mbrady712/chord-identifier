import itertools

note_to_semitone = {
    'B#': 0, 'Cn': 0, 'Dd': 0, 
    'Bx': 1, 'C#': 1, 'Db': 1, 
    'Cx': 2, 'Dn': 2, 'Ed': 2,
    'D#': 3, 'Eb': 3, 'Fd': 3,
    'Dx': 4, 'En': 4, 'Fb': 4,
    'E#': 5, 'Fn': 5, 'Gd': 5,
    'Ex': 6, 'F#': 6, 'Gb': 6,
    'Fx': 7, 'Gn': 7, 'Ad': 7,
    'G#': 8, 'Ab': 8, 
    'Gx': 9, 'An': 9, 'Bd': 9,
    'A#': 10, 'Bb': 10, 'Cd': 10,
    'Ax': 11, 'Bn': 11, 'Cb': 11
}

natural_to_naturalTone = {
    'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6
}

naturalTone_to_natural = {
    0: 'C', 1: 'D', 2: 'E', 3: 'F', 4: 'G', 5: 'A', 6: 'B'
}

chordQualities = {
    "major": [4, 3],
    "minor": [3, 4],
    "augmented": [4, 4],
    "diminished": [3, 3],
    "major 7": [4, 3, 4],
    "dominant 7": [4, 3, 3],
    "minor 7": [3, 4, 3],
    "diminished 7": [3, 3, 3],
    "minor-major 7": [3, 4, 4],
    "half-diminished 7": [3, 3, 4]
}

class ChordIdentifier:
    def __init__(self, notes):
        self.notes = notes
        self.naturals = self.getNaturals()
        self.accidentals = self.getAccidentals()
        self.naturalTones = self.getNaturalTones()
        self.numNaturals = 7
        self.numSemitones = 12
        self.rootPosNaturalTones = self.find_rootPos(self.numNaturals)
        if(self.rootPosNaturalTones != []):
            self.rootPosNaturals = self.naturalTonesToNaturals(self.rootPosNaturalTones)
            self.concatenatedNotes = self.getConcatenatedNotes(self.notes)
            self.rootPosNotes = self.getRootPosNotes(self.rootPosNaturals, self.concatenatedNotes)
            self.rootPosSemitones = self.getSemitones(self.rootPosNotes)
            self.rootPosSemitoneIntervals = self.find_intervals(self.rootPosSemitones, self.numSemitones)
            self.rootPosNaturalToneIntervals = self.find_intervals(self.rootPosNaturalTones, self.numNaturals)
            self.chordQuality = self.getChordQuality(self.rootPosSemitoneIntervals)
            self.chordIdentity = self.identifyChord(self.rootPosNotes, self.chordQuality)
        else:
            self.chordIdentity = "Unknown chord"

    def identifyChord(self, rootPosNotes, chordQuality):
        root = rootPosNotes[0] + " "
        if(chordQuality == "Unknown chord"):
            root = ""
        elif(root[1] == 'n'):
            root = root[0] + " "
        return root + chordQuality

    def getChordQuality(self, rootPosSemitoneIntervals):
        quality = "Unknown chord"
        for key, value in chordQualities.items():
            if value == rootPosSemitoneIntervals:
                quality = key
        return quality
    
    def naturalTonesToNaturals(self, rootPosNaturalTones):
        rootPosNaturals = []
        for i in range(len(rootPosNaturalTones)):
            rootPosNaturals.append(naturalTone_to_natural[rootPosNaturalTones[i]])
        return rootPosNaturals

    def getRootPosNotes(self, rootPosNaturals, concatenatedNotes):
        rootPosNotes = []
        for i in range(len(rootPosNaturals)):
            for j in range(len(concatenatedNotes)):
                if(rootPosNaturals[i] == concatenatedNotes[j][0]):
                    rootPosNotes.append(concatenatedNotes[j])
        return rootPosNotes

    def getConcatenatedNotes(self, notes):
        concatenatedNotes = []
        for i in range(len(notes) - 1):
            if(i % 2 == 0):
                concatenatedNotes.append(notes[i] + notes[i + 1]) 
        return concatenatedNotes

    def getSemitones(self, notes):
        semitones = [note_to_semitone[note] for note in notes]
        return semitones

    def getNaturals(self):
        naturals = []
        for element in self.notes:
            if (self.notes.index(element) % 2 == 0):
                naturals.append(element)
        return naturals
    
    def getAccidentals(self):
        accidentals = []
        for element in self.notes:
            if (self.notes.index(element) % 2 == 0):
                accidentals.append(element)
        return accidentals
    
    def getNaturalTones(self):
        naturalTones = [natural_to_naturalTone[natural] for natural in self.naturals]
        return naturalTones
    
    def find_intervals(self, tones, numPossibleTones):
        noteIter = 0
        intervals = []
        numIntervals = len(tones) - 1
        currentTone = 0
        nextTone = 0
        while noteIter < numIntervals:
            currentTone = tones[noteIter]
            nextTone = tones[noteIter + 1]
            if(currentTone > nextTone):
                nextTone += numPossibleTones
            intervals.append(nextTone - currentTone)
            noteIter = noteIter + 1
        return intervals

    def find_rootPos(self, numPossibleTones):
        third = 2
        allInversions = [list(permutation) for permutation in itertools.permutations(self.naturalTones)]
        rootPositionNaturalTones = []
        chordIter = 0
        for i in range(len(allInversions)):
            #Get intervals of permutations
            intervals = self.find_intervals(allInversions[chordIter], numPossibleTones)
            #See if the permutation has all thirds (i.e. is in root position)
            allThirds = True
            for interval in intervals:
                if(interval != third):
                    allThirds = False
            if(allThirds):
                rootPositionNaturalTones = allInversions[chordIter]
            chordIter += 1
        return rootPositionNaturalTones

def get_notes():
    notes = input("Enter the notes and their accidentals separated by spaces (e.g., C # E # G #): ")
    return notes.split()

def main():
    letter_names = ["C", "D", "E", "F", "G", "A", "B"]
    accidentals = ["n", "b", "#", "d", "x"]
    counter = 0

    # Num triads = possible roots times inversions times num of different triads
    # Possible roots = Cb, C, C#, Db, D, D#, Eb, E, E#, Fb, F, F#, Gb, G, G#, Ab, A, A#, Bb, B, B# = 21
    # Num triads = 21 x 6 x 4 = 504 - 6 (B# augmented requires a triple sharp) = 498

    # Generate all possible six-member lists for triads
    triad_combinations = itertools.product(letter_names, accidentals, repeat=3)
    for triad in triad_combinations:
        notes = [note for pair in triad for note in pair]
        chord_identifier = ChordIdentifier(notes)
        output = chord_identifier.chordIdentity
        if(output != "Unknown chord" and output[1] != 'x' and output[1] !='d' and "augmented" in output):
            print(f"{notes}: {output}")
            counter += 1
            print(counter)
    
    # Num 7th chords = 21 x 24 x 6 = 3024
    # 504 chords of each quality 
    # No Cb, Fb diminished 7th, bc they require a triple flat

    # Generate all possible eight-member lists for seventh chords
    seventh_combinations = itertools.product(letter_names, accidentals, repeat=4)
    for seventh in seventh_combinations:
        notes = [note for pair in seventh for note in pair]
        chord_identifier = ChordIdentifier(notes)
        output = chord_identifier.chordIdentity
        if(output != "Unknown chord" and output[1] != 'x' and output[1] !='d'):
            print(f"{notes}: {output}")
            counter += 1
            print(counter)

if __name__ == "__main__":
    main()
