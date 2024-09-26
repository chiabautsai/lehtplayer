import mpv

class Player:
    def __init__(self):
        """
        Initialize the Player class.
        Sets up the mpv player with audio-only configuration.
        """
        self.player = mpv.MPV(
            video=False,  # Disable video output
            audio_display=False  # Disable audio visualization
        )

    def play(self, media=None, playlist_pos=None):
        """
        Start playback of a track or the current playlist.
        
        :param media: Optional; path or URL of the track to play.
        :param playlist_pos: Optional; position in the playlist to play.
        """
        if media:
            self.player.play(media)
        elif playlist_pos is not None:
            if playlist_pos < self.player.playlist_count and playlist_pos >= 0:
                self.player.playlist_pos = playlist_pos
            else:
                raise ValueError("Invalid playlist position")
        else:
            self.resume()

    def pause(self):
        """Pause the current playback."""
        self.player.pause = True

    def resume(self):
        """Resume playback if paused."""
        self.player.pause = False

    def stop(self):
        """Stop the current playback. Clears the playlist."""
        self.player.stop()

    def next_track(self):
        """Play the next track in the playlist."""
        if self.player.playlist_pos < self.player.playlist_count - 1 and self.player.playlist_pos >= 0:
            self.player.playlist_next()
        else:
            raise ValueError("No next track")

    def previous_track(self):
        """Play the previous track in the playlist."""
        if self.player.playlist_pos > 0 and self.player.playlist_pos < self.player.playlist_count:
            self.player.playlist_prev()
        else:
            raise ValueError("No previous track")

    def set_volume(self, volume):
        """
        Set the playback volume.
        
        :param volume: Volume level (0-100).
        """
        self.player.volume = volume

    def get_volume(self):
        """Get the current volume level."""
        return self.player.volume

    def set_position(self, position):
        """
        Seek to a specific position in the current track.
        
        :param position: Position in seconds.
        """
        self.player.seek(position, reference="absolute")

    def get_position(self):
        """Get the current playback position in seconds."""
        return self.player.time_pos

    def get_duration(self):
        """Get the duration of the current track in seconds."""
        return self.player.duration

    def add_to_playlist(self, track):
        """
        Add a track to the playlist.
        
        :param track: Path or URL of the track to add.
        """
        self.player.playlist_append(track)

    def clear_playlist(self):
        """Clear the current playlist."""
        self.player.playlist_clear()

    def get_playlist(self):
        """Get the current playlist."""
        return self.player.playlist

    def is_playing(self):
        """Check if audio is currently playing."""
        return not self.player.pause

    def get_current_track(self):
        """Get information about the current track."""
        return {
            'filename': self.player.filename,
            'title': self.player.media_title,
            'metadata': self.player.metadata
        }

    def get_audio_devices(self):
        """Get a list of available audio output devices."""
        return self.player.audio_device_list

    def set_audio_device(self, device_name):
        """
        Set the audio output device.

        :param device_name: The name of the audio device to use.
        """
        devices = self.get_audio_devices()
        if device_name in devices:
            self.player.audio_device = device_name
        else:
            raise ValueError(f"Invalid audio device: {device_name}")

    def get_current_audio_device(self):
        """Get the name of the current audio output device."""
        return self.player.audio_device
