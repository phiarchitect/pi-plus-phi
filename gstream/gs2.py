"""
"""
import subprocess
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Initialize GStreamer
Gst.init(None)

def main():
    # Create the main loop
    loop = GLib.MainLoop()

    screen_pipeline = Gst.parse_launch(
        "ximagesrc use-damage=0 startx=0 starty=768 endx=1919 endy=1847 ! "
        "videoconvert ! vp8enc cpu-used=4 target-bitrate=2000000 ! matroskamux ! "
        "filesink location=screen.mkv")

    mic = "alsa_input.usb-BLUE_MICROPHONE_Blue_Snowball_201305-00.analog-stereo"
    mic_pipeline = Gst.parse_launch(
        f"pulsesrc device={mic} ! "
        "volume volume=1.8 ! "
        "audioconvert ! opusenc ! oggmux ! "
        "filesink location=mic.ogg")

    system = "alsa_output.pci-0000_0a_00.6.analog-stereo.monitor"
    system_audio_pipeline = Gst.parse_launch(
        f"pulsesrc device={system} ! "
        "volume volume=0.7 ! "
        "audioconvert ! opusenc ! oggmux ! "
        "filesink location=system.ogg")


    # Start the pipelines
    screen_pipeline.set_state(Gst.State.PLAYING)
    mic_pipeline.set_state(Gst.State.PLAYING)
    system_audio_pipeline.set_state(Gst.State.PLAYING)

    try:
        loop.run()
    except KeyboardInterrupt:
        # Send EOS to each pipeline
        screen_pipeline.send_event(Gst.Event.new_eos())
        mic_pipeline.send_event(Gst.Event.new_eos())
        system_audio_pipeline.send_event(Gst.Event.new_eos())

        # Stop the pipelines on interrupt
        screen_pipeline.set_state(Gst.State.NULL)
        mic_pipeline.set_state(Gst.State.NULL)
        system_audio_pipeline.set_state(Gst.State.NULL)
        loop.quit()

    # Step 1: Combine screen (video) with system audio into an MP4 file
    combine_screen_and_system = [
        'ffmpeg',
        '-i', 'screen.mkv',
        '-i', 'system.ogg',
        '-c:v', 'libx264',
        '-crf', '23',
        '-preset', 'veryfast',
        '-c:a', 'copy',
        '-shortest','screen_system.mp4'
    ]
    subprocess.run(combine_screen_and_system)

    #  post_process_mic_command = [
        #  'ffmpeg',
        #  '-i', 'mic.ogg',
        #  '-af', "afftdn, equalizer=f=2500:t=q:w=0.5:g=3, acompressor=threshold=-30dB:ratio=3:knee=2.5:attack=50:release=1000:makeup=6dB",
        #  'mic_processed.ogg'
    #  ]
    #  subprocess.run(post_process_mic_command)

    # Step 2: Merge the combined file with microphone audio track
    merge_with_mic_audio_command = [
        'ffmpeg',
        '-i', 'screen_system.mp4',  # Input file with system audio
        '-i', 'mic.ogg',  # Input file with microphone audio
        '-filter_complex', '[0:a][1:a]amix=inputs=2:duration=shortest,volume=2.0[a]',  # Mix audio streams
        '-map', '0:v',  # Map video from first input
        '-map', '[a]',  # Map mixed audio
        '-c:v', 'copy',  # Copy the video stream as is
        '-c:a', 'aac',  # Re-encode audio to AAC
        '-b:a', '128k',  # Bitrate for the audio
        'screen_system_mic.mp4'  # Output file
    ]

    subprocess.run(merge_with_mic_audio_command)
if __name__ == "__main__":
    main()

