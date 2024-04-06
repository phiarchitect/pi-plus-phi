#!/usr/bin/env bash

ffmpeg -y -i mic_clean.ogg \
  -filter_complex "showwaves=s=400x400:mode=cline:colors=Green|White" \
  -c:v libx264 \
  -pix_fmt yuv420p \
  mic_waves.mp4

ffmpeg -y -i system.ogg \
  -filter_complex "showwaves=s=400x400:mode=cline:colors=Orange|White" \
  -c:v libx264 \
  -pix_fmt yuv420p \
  system_waves.mp4

ffmpeg -y -i screen.mkv \
       -i mic_waves.mp4 \
       -i system_waves.mp4 \
       -i circle_mask.png \
       -filter_complex "\
       [1:v]scale=100x100,format=yuva420p[1scaled]; \
       [2:v]scale=100x100,format=yuva420p[2scaled]; \
       [1scaled][3:v]alphamerge[1masked]; \
       [2scaled][3:v]alphamerge[2masked]; \
       [0:v][1masked] overlay=shortest=1:x=10:y=H-h-10 [v1];\
       [v1][2masked] overlay=shortest=1:x=W-w-10:y=H-h-10,format=yuv420p[v];\
       [1:a][2:a]amix=inputs=2:duration=shortest:normalize=0,volume=2.0[a]" \
       -map "[v]" -map "[a]" \
       -c:v libx264 \
       -c:a aac \
       -b:a 128k \
       screen_with_circular_waves.mp4

