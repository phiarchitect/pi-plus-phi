import harmonic_resonance.midiator as pm
from rich import print


PROJECT = "pi-plus-phi"
title = "intro4"
bpm = 180  # beats per minute
bpM = 4  # beats per Measure
root = pm.N.E4  # the root note of the key
key = "E"
scale = pm.Scale(root, pm.S.pentatonic_major)
#  print(scale)
#  breakpoint()

part = pm.Part(PROJECT, title, bpm=bpm, bpM=bpM, root=root, key=key)
M = part.measure_ticks()

clave = pm.Percussion(part, pm.P.claves)
shaker = pm.Percussion(part, pm.P.shaker)
conga = pm.Conga(part)
vibes = part.add_vibes()
horns = part.add_horns()
choir = part.add_choir_swell()
oohs = part.add_choir_ooh()

VIBES_SWITCH = False
#  VIBES_SWITCH = True

HORNS_SWITCH = False
#  HORNS_SWITCH = True

OOH_SWITCH = False
#  OOH_SWITCH = True

#  part.set_marker("count", M)

#  clave.set_hits(M, 4)
conga.rest_all(2 * M)
shaker.set_rest(2 * M)
choir.set_rest(2 * M)
oohs.set_rest(2 * M)

pm.patterns.latin.son_clave2(2 * M, clave)

patterns = [
    conga.patterns["bolero"],
    conga.patterns["samba"],
]

chord = pm.chords.get_chord_notes(root, pm.C.dominant_7)


if VIBES_SWITCH:
    intro_chord = pm.chords.get_chord_notes(root, pm.C.dominant_13)
    vibes.set_notes(intro_chord, 2 * M, offset=M/16)
else:
    vibes.set_rest(2 * M)



horns_chord = pm.chords.get_chord_notes(root - 12, pm.C.major)
horns2_chord = pm.chords.get_chord_notes(root - 24, pm.C.major)
if HORNS_SWITCH:
    horns.set_rest(2 * M)
    horns.set_volume(32, 2 * M)
else:
    horns.set_rest(2 * M)
    horns.set_volume(32, 2 * M)

    #  horns.ramp_volume_up(2 * M)
    #  horns.ramp_volume_down(2 * M)


for pattern in patterns:
    for i in range(2):
        if i % 2:
            conga.set_patterns(pattern, 2 * M, velocity_mod=10)
        else:
            conga.set_patterns(pattern, 2 * M, velocity_mod=-10)

        if VIBES_SWITCH:
            vibes.set_notes(chord, 2 * M, offset=M/16)
        else:
            vibes.set_note(root, 2 * M)

        if HORNS_SWITCH:
            if i % 2:
                horns.set_rest(M)
                horns.set_rest(M/4)
                horns.set_notes(horns2_chord,  3 * M/8, velocity=70)
                horns.set_notes(horns2_chord,  M/8, velocity=100)
                horns.set_rest(M/4)
                horns.set_volume(100, 2 * M)
                #  horns.ramp_volume_up(2 * M)
                #  horns.ramp_volume_down(2 * M)
            else:
                # first
                horns.set_rest(M)
                horns.set_rest(M/4)
                horns.set_notes(horns_chord,  3 * M/8, velocity=70)
                horns.set_notes(horns_chord,  M/8, velocity=100)
                horns.set_rest(M/4)
                horns.set_volume(100, 2 * M)
                #  horns.set_notes(horns_chord, 2 * M, velocity=80)
                #  horns.set_volume(100, 0)
                #  horns.ramp_volume_down(2 * M)

        else:
            horns.set_rest(2 * M)

        if OOH_SWITCH:
            if i % 2:
                note = scale[2]
                oohs.set_note(note,  2 * M, velocity=70)
                #  oohs.set_volume(100, 2 * M)
            else:
                # first
                oohs.set_note(root + 12,  2 * M, velocity=80)
                #  oohs.set_volume(100, 0)
                #  oohs.ramp_volume_down(2 * M)

        else:
            oohs.set_rest(2 * M)

        choir.set_rest(2 * M)

        pm.patterns.latin.son_clave2(2 * M, clave)
        for _ in range(4):
            shaker.set_hit(M / 4, velocity=90)
            shaker.set_hit(M / 4, velocity=60)

vibes.set_note(root, 2 * M)
#  choir.set_notes(chord, 2*M, M/16)
choir.set_notes(
    chord,
    2 * M,
)

part.save()
part.play()
part.convert()
