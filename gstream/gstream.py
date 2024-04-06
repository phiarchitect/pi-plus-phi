import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Initialize GStreamer
Gst.init(None)

def create_pipeline(source, caps, filename):
    """
    Create a GStreamer pipeline for a given source and caps.
    """
    pipeline_desc = (
        f"{source} ! {caps} ! queue ! filesink location={filename}"
    )
    return Gst.parse_launch(pipeline_desc)

def main():
    # Define pipelines
    screen_pipeline = create_pipeline(
        source="pipewiresrc path=39",  # Adjust path= value based on your screen source
        caps="video/x-raw,framerate=30/1,width=1920,height=1080",
        filename="screen.mkv"
    )
    
    mic_pipeline = create_pipeline(
        source="pipewiresrc path=45",  # Adjust path= value based on your microphone source
        caps="audio/x-raw,channels=2",
        filename="mic_audio.wav"
    )
    
    system_pipeline = create_pipeline(
        source="pipewiresrc path=47",  # Adjust path= value based on your system audio source
        caps="audio/x-raw,channels=2",
        filename="system_audio.wav"
    )
    
    # Start recording
    screen_pipeline.set_state(Gst.State.PLAYING)
    mic_pipeline.set_state(Gst.State.PLAYING)
    system_pipeline.set_state(Gst.State.PLAYING)
    
    # Keep running
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        # Stop recording on Ctrl+C
        screen_pipeline.set_state(Gst.State.NULL)
        mic_pipeline.set_state(Gst.State.NULL)
        system_pipeline.set_state(Gst.State.NULL)
        print("Stopped recording")

if __name__ == "__main__":
    main()

