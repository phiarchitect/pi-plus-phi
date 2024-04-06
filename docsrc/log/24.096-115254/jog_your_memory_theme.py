"""
orchestration template
"""
import harmonic_resonance.midiator as pm
import itertools as itertools
import random as random
from rich import print as log

PROJECT = "jog-your-memory"
title = "theme"
bpm = 180  # beats per minute
bpM = 4  # beats per Measure
root = pm.N.E3  # the root note of the key
key = "E"

part = pm.Part(PROJECT, title, bpm=bpm, root=root, key=key)
M = part.measure_ticks()

chords = pm.progressions.ii_V_i_i(root)
#  chords = pm.progressions.i_vi_ii_V(root)

piano = part.add_piano()
vibes = part.add_vibes()
bass = part.add_bass()
strings = part.add_strings()

horns = part.add_horns()
HORNS = False

choir = part.add_choir_swell()

conga = pm.Conga(part)
standard = pm.Standard(part)

for loop in range(4):
    part.set_marker(f"{loop}", 0)
    for chord_num, (chord_name, chord) in enumerate(chords):
        chord2 = [note + 12 for note in chord]
        chord3 = [note + 12 for note in chord2]
        chord4 = [note + 12 for note in chord3]

        part.set_marker(f"{chord_name} - {chord}", 0)

        measures = 4
        for m in range(measures):
            part.set_marker(f"{m + 1}", M)
            if m == 3:
                #  velocity_mod = 10
                patterns = standard.patterns["funky_drummer"]
                standard.set_patterns(patterns, M, velocity_mod=-10)
            else:

                patterns = standard.patterns["billie_jean"]
                standard.set_patterns(patterns, M, velocity_mod=-10)

            #  patterns = standard.patterns["swing"]
            #  standard.set_patterns(patterns, M, velocity_mod=-10)

            if chord_num == 3:
                if m == measures - 1:
                    # last
                    bass.set_note(chord[1] - 12, M, velocity=90)
                else:
                    bass.set_note(chord[2] - 12, M, velocity=70)
            else:
                if m == measures - 1:
                    # last
                    bass.set_note(chord[1] - 12, M, velocity=90)
                else:
                    bass.set_note(chord[0] - 12, M, velocity=70)

            if loop > 0:
                if chord_num == 3:
                    # last
                    piano.set_notes(chord2, M, velocity=60)
                else:
                    piano.set_notes(chord, M, velocity=60)
            else:
                piano.set_rest(M)

        if loop > 1:
            patterns = conga.patterns["samba"]
            conga.set_patterns(patterns, 2 * M, velocity_mod=-10)
            patterns = conga.patterns["tumbao"]
            conga.set_patterns(patterns, 2 * M, velocity_mod=10)
        else:
            conga.rest_all(4 * M)


        if HORNS:
            if loop >= 0:
                #  horns.set_rest(3 * M)
                for _ in range(4):
                    b = M / 8
                    horns.set_note(chord[-1] - 12, 1 * b, velocity=90)
                    #  horns.set_note(chord[0], 3 * b, velocity=30)
                    horns.set_rest(3 * b)
                    horns.set_note(chord[-2] - 12, 1 * b, velocity=70)
                    #  horns.set_note(chord[1], 3 * b, velocity=50)
                    horns.set_rest(3 * b)
            else:
                horns.set_rest(4 * M)

        if loop > 2:
            strings.set_rest(3 * M)
            strings.set_notes(chord2, M / 2, velocity=20)
            strings.set_notes(chord3, M / 2, velocity=30)
        else:
            strings.set_rest(4 * M)

        if loop > 1:
            #  choir.set_rest(M)
            #  choir.set_notes(chord, (measures - 1) * M, offset=M/8)
            if chord_num == 3:
                choir.set_rest(4 * M)
                choir.set_volume(32, 4 * M)
            else:
                choir.set_notes(chord, measures * M, offset=M / 4)
                choir.set_volume(32, 0)
                choir.ramp_volume_up(2 * M)
                choir.ramp_volume_down(2 * M)
        else:
            choir.set_rest(4 * M)
            choir.set_volume(32, 4 * M)

        #  offset = M/32
        #  #  vibes.set_rst(2 * M)
        #  vibes.set_notes(chord3, 3 * M, offset=offset, velocity=55)
        #  vibes.set_notes(chord4, M/2, offset=offset, velocity=65)
        #  vibes.set_notes(chord4, M/2, offset=offset, velocity=65)

        #  #  strings
        #  if chord_num in [2, 3]:
        #  strings.set_rest(2 * M)
        #  strings.set_notes(chord, 2 * M, M / 8)
        #  else:
        #  strings.set_rest(measures * M)

        #  strings.set_volume(32, 2 * M)
        #  strings.ramp_volume_up(2 * M)

part.save()
part.play()
part.convert()
