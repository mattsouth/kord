from bestia.output import Row, FString, echo
from bestia.iterate import looped_list_item

_SHARP = 1
_FLAT = -1

_TONE = 2
_SEMITONE = 1

_UNISON = 0
_DIMINISHED_SECOND = 0

_MINOR_SECOND = 1
_AUGMENTED_UNISON = 1

_MAJOR_SECOND = 2
_DIMINISHED_THIRD = 2

_MINOR_THIRD = 3
_AUGMENTED_SECOND = 3

_DIMINISHED_FOURTH = 4
_MAJOR_THIRD = 4

_PERFECT_FOURTH = 5
_AUGMENTED_THIRD = 5

_AUGMENTED_FOURTH = 6
_DIMINISHED_FIFTH = 6

_PERFECT_FIFTH = 7
_DIMINISHED_SIXTH = 7

_MINOR_SIXTH = 8
_AUGMENTED_FIFTH = 8

_MAJOR_SIXTH = 9
_DIMINISHED_SEVENTH = 9

_MINOR_SEVENTH = 10
_AUGMENTED_SIXTH = 10

_MAJOR_SEVENTH = 11
_DIMINISHED_OCTAVE = 11

_OCTAVE = 12
_AUGMENTED_SEVENTH = 12

_TONES = [

    [ ('B', '#' ), ('C', '' ), ('D', 'bb')],

    [ ('B', '##'), ('C', '#'), ('D', 'b' )],

    [ ('C', '##'), ('D', '' ), ('E', 'bb')],

    [ ('F', 'bb'), ('D', '#' ), ('E', 'b')],

    [ ('D', '##'), ('E', ''  ), ('F', 'b')],

    [ ('G', 'bb'), ('F', ''  ), ('E', '#')],

    [ ('E', '##'), ('F', '#' ), ('G', 'b')],

    [ ('F', '##'), ('G', '' ), ('A', 'bb')],

    [ ('?', '??'), ('G', '#'), ('A', 'b')],

    [ ('G', '##'), ('A', '' ), ('B', 'bb')],

    [ ('C', 'bb'), ('A', '#' ), ('B', 'b')],

    [ ('A', '##'), ('B', '' ), ('C', 'b')],

]

class Fret(object):

    def __init__(self, note='', fret=0):
        self.fret = fret
        self.note = Note() if not note else note

    def __repr__(self):
        f = '||' if self.fret == 0 else '|'
        fret = FString(
            '{}{}{} {}'.format(self.note.tone, self.note.alt, self.note.octave, f),
            size=6, align='r', colors=['red']
        )
        return str(fret)


class String(object):

    fret = []

    def __init__(self, open_note='Abb3'):

        self.init_frets()

        tone = open_note[0]
        alt = open_note[1:-1]
        octave = int(open_note[-1])

        open_note = Note(tone, alt, octave)
        self.fret[0] = Fret(open_note)

    def init_frets(self):
        for n in range(12):
            self.fret.append(None)


    def __repr__(self):
        string_line = Row()
        for i in range(12):
            string_line.append(self.fret[i])
        return str(string_line)


class Tuning(object):

    def __init__(self, *arg, **kwargs):
        for k, v in kwargs.items():
            if k.startswith('string'):
                setattr(self, k, String(v))



class Note(object):

    _ORDER = ('C', 'D', 'E', 'F', 'G', 'A', 'B')

    def __init__(self, tone=' ', alt=' ', octave=' '):
        self.tone = tone.upper()
        self.alt = alt.lower()
        self.octave = octave

        self.tone_index = None
        self.alt_index = None
        self.get_indeces()

    def get_indeces(self):
        for t_i, _tones in enumerate(_TONES):
            for a_i, _tone in enumerate(_tones):
                if self.tone == _tone[0] and self.alt == _tone[1]:
                    self.tone_index = t_i
                    self.alt_index = a_i
                    break

    def next(self):
        my_index = self._ORDER.index(self.tone)
        return looped_list_item(my_index +1, self._ORDER)

    def previous(self):
        my_index = self._ORDER.index(self.tone)
        return looped_list_item(my_index -1, self._ORDER)

    def __repr__(self):
        return '{}{}'.format(self.tone, self.alt)



class Scale(object):

    def __init__(self, key='C', alt=''):

        self.degree = []
        self.init_degrees()

        self.tonic = Note(key, alt)
        self.add_degree(1, self.tonic)

        self.calculate_degrees()

    def __repr__(self):
        spell_line = Row()
        for i in range(1, self._PITCHES +2):
            spell_line.append(FString(self.degree[i], size=4, colors=['yellow']))
        return str(spell_line)

    def init_degrees(self):
        for n in range(13):
            self.degree.append(None)

    def add_degree(self, n, note):
        self.degree[n] = note

    def calculate_degrees(self):
        for d in range(2, self._PITCHES +2):
            self.calculate_degree(d)



class ChromaticScale(Scale):

    _PITCHES = 12

    interval = [
        None,
        _UNISON,
        _AUGMENTED_UNISON,

        _MAJOR_SECOND,
        _AUGMENTED_SECOND,

        _MAJOR_THIRD,

        _PERFECT_FOURTH,
        _AUGMENTED_FOURTH,

        _PERFECT_FIFTH,
        _AUGMENTED_FIFTH,

        _MAJOR_SIXTH,
        _AUGMENTED_SIXTH,

        _MAJOR_SEVENTH,
        _OCTAVE,
    ]

    def __init__(self):
        pass

    # def calculate_degree(self, d):
    #     row_index = self.tonic.tone_index +self.interval[d]
    #     next_degree = [t for t in looped_list_item(row_index, _TONES) if t[0] == self.degree[d -1].next()]

    #     if len(next_degree) != 1:
    #         echo('Failed to get degree[{}] of {} {}'.format(d, self.tonic, self.__class__.__name__), 'red')
    #         input()

    #     self.add_degree(d, Note(*next_degree[0]))



class DiatonicScale(Scale):

    _PITCHES = 7

    def calculate_degree(self, d):
        row_index = self.tonic.tone_index +self.interval[d]
        next_degree = [t for t in looped_list_item(row_index, _TONES) if t[0] == self.degree[d -1].next()]

        if len(next_degree) != 1:
            echo('Failed to get degree[{}] of {} {}'.format(d, self.tonic, self.__class__.__name__), 'red')
            input()

        self.add_degree(d, Note(*next_degree[0]))


class MajorScale(DiatonicScale):

    interval = [
        None,
        _UNISON,
        _MAJOR_SECOND,
        _MAJOR_THIRD,
        _PERFECT_FOURTH,
        _PERFECT_FIFTH,
        _MAJOR_SIXTH,
        _MAJOR_SEVENTH,
        _OCTAVE,
    ]

class MinorScale(DiatonicScale):

    interval = [
        None,
        _UNISON,
        _MAJOR_SECOND,
        _MINOR_THIRD,
        _PERFECT_FOURTH,
        _PERFECT_FIFTH,
        _MINOR_SIXTH,
        _MINOR_SEVENTH,
        _OCTAVE,
    ]

class NaturalMinorScale(DiatonicScale):

    interval = [
        None,
        _UNISON,
        _MAJOR_SECOND,
        _MINOR_THIRD,
        _PERFECT_FOURTH,
        _PERFECT_FIFTH,
        _MINOR_SIXTH,
        _MINOR_SEVENTH,
        _OCTAVE,
    ]

class MelodicMinorScale(DiatonicScale):

    interval = [
        None,
        _UNISON,
        _MAJOR_SECOND,
        _MINOR_THIRD,
        _PERFECT_FOURTH,
        _PERFECT_FIFTH,
        _MAJOR_SIXTH,
        _MINOR_SEVENTH,
        _OCTAVE,
    ]

class HarmonicMinorScale(DiatonicScale):

    interval = [
        None,
        _UNISON,
        _MAJOR_SECOND,
        _MINOR_THIRD,
        _PERFECT_FOURTH,
        _PERFECT_FIFTH,
        _MINOR_SIXTH,
        _MAJOR_SEVENTH,
        _OCTAVE,
    ]

if __name__ == '__main__':

    try:
        b_minor = NaturalMinorScale('B')
        print(b_minor)

        a_minor = MelodicMinorScale('A')
        print(a_minor)

        d_minor = HarmonicMinorScale('D')
        print(d_minor)

        std_tuning = Tuning(
            string1='E4',
            string2='B3',
            string3='G3',
            string4='D3',
            string5='A2',
            string6='E2'
        )
        echo(std_tuning.string3)

        empty_fret = Fret(fret=6)
        string1 = Row(
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            empty_fret, 
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            # FString(empty_fret, size=6, align='r'),
            width=72
        ).echo()

        Bb3 = Note('B', 'b', 3)
        # new_fret = Fret(Bb3, fret=12)
        # print(new_fret)

        bla = ChromaticScale()
        for w in bla.interval:
            echo(w, 'yellow')

    except KeyboardInterrupt:
        echo()


# JUST FINISHED BASIC CHROMATIC SCALE DEFINITION TO OUTPUT ALL FRETS OF STRING


