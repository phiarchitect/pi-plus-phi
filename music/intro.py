"""
test percusion patterns
"""
import harmonic_resonance.midiator as pm
from rich import print


PROJECT = 'pi-plus-phi'
title = 'intro'
bpm = 180  # beats per minute
bpM = 4  # beats per Measure
root = pm.N.E4  # the root note of the key
key = 'E'
scale = pm.Scale(root, pm.S.pentatonic_major)
#  print(scale)
#  breakpoint()

part = pm.Part(PROJECT, title, bpm=bpm, bpM=bpM, root=root, key=key)
M = part.measure_ticks()

clave = pm.Percussion(part, pm.P.claves)
shaker = pm.Percussion(part, pm.P.shaker)
conga = pm.Conga(part)
vibes = part.add_vibes()
choir = part.add_choir_swell()

part.set_marker('count', M)

#  clave.set_hits(M, 4)
conga.rest_all(2 * M)
shaker.set_rest(2 * M)
vibes.set_rest(2 * M)
choir.set_rest(2 * M)

pm.patterns.latin.son_clave2(2 * M, clave)

pattern = conga.patterns["samba"]

chord = pm.chords.get_chord_notes(root, pm.C.dominant_7)

for i in range(4):
    if i % 2:
        conga.set_patterns(pattern, 2 * M, velocity_mod=10)
    else:
        conga.set_patterns(pattern, 2 * M, velocity_mod=-10)

    vibes.set_note(root, 2 * M)

    choir.set_rest(2 * M)

    pm.patterns.latin.son_clave2(2 * M, clave)
    for _ in range(4):
        shaker.set_hit(M/4, velocity=90)
        shaker.set_hit(M/4, velocity=60)

vibes.set_note(root, 2 * M)
#  choir.set_notes(chord, 2*M, M/16)
choir.set_notes(chord, 2*M, )

part.save()
part.play()
part.convert()
