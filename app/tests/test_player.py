import unittest
from unittest.mock import MagicMock
from app.player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        """Setup before each test."""
        self.player = Player()
        self.player.player = MagicMock()  # Mock the mpv player

    def test_play(self):
        """Test playing a track."""
        self.player.play("test_track.mp3")
        self.player.player.playlist_clear.assert_called_once()
        self.player.player.playlist_append.assert_called_once_with("test_track.mp3")
        self.player.player.play.assert_called_once()

    def test_play_no_track(self):
        """Test playing the current playlist."""
        self.player.play()
        self.player.player.playlist_clear.assert_not_called()
        self.player.player.playlist_append.assert_not_called()
        self.player.player.play.assert_called_once()

    def test_pause(self):
        """Test pausing playback."""
        self.player.pause()
        self.assertEqual(self.player.player.pause, True)

    def test_resume(self):
        """Test resuming playback."""
        self.player.resume()
        self.assertEqual(self.player.player.pause, False)

    def test_stop(self):
        """Test stopping playback."""
        self.player.stop()
        self.player.player.stop.assert_called_once()

    def test_next_track(self):
        """Test playing the next track."""
        self.player.next_track()
        self.player.player.playlist_next.assert_called_once()

    def test_previous_track(self):
        """Test playing the previous track."""
        self.player.previous_track()
        self.player.player.playlist_prev.assert_called_once()

    def test_set_volume(self):
        """Test setting the volume."""
        self.player.set_volume(75)
        self.assertEqual(self.player.player.volume, 75)

    def test_get_volume(self):
        """Test getting the volume."""
        self.player.player.volume = 50
        self.assertEqual(self.player.get_volume(), 50)

    def test_set_position(self):
        """Test setting the playback position."""
        self.player.set_position(30)
        self.player.player.seek.assert_called_once_with(30, reference="absolute")

    def test_get_position(self):
        """Test getting the playback position."""
        self.player.player.time_pos = 15
        self.assertEqual(self.player.get_position(), 15)

    def test_get_duration(self):
        """Test getting the track duration."""
        self.player.player.duration = 180
        self.assertEqual(self.player.get_duration(), 180)

    def test_add_to_playlist(self):
        """Test adding a track to the playlist."""
        self.player.add_to_playlist("new_track.mp3")
        self.player.player.playlist_append.assert_called_once_with("new_track.mp3")

    def test_clear_playlist(self):
        """Test clearing the playlist."""
        self.player.clear_playlist()
        self.player.player.playlist_clear.assert_called_once()

    def test_get_playlist(self):
        """Test getting the playlist."""
        self.player.player.playlist = ["track1.mp3", "track2.mp3"]
        self.assertEqual(self.player.get_playlist(), ["track1.mp3", "track2.mp3"])

    def test_is_playing(self):
        """Test checking if audio is playing."""
        self.player.player.pause = False
        self.assertTrue(self.player.is_playing())
        self.player.player.pause = True
        self.assertFalse(self.player.is_playing())

    def test_get_current_track(self):
        """Test getting information about the current track."""
        self.player.player.filename = "current_track.mp3"
        self.player.player.media_title = "Current Track Title"
        expected_track_info = {
            'filename': "current_track.mp3",
            'title': "Current Track Title"
        }
        self.assertEqual(self.player.get_current_track(), expected_track_info)

    def test_get_audio_devices(self):
        """Test getting the list of audio devices."""
        self.player.player.audio_device_list = ["Device 1", "Device 2"]
        self.assertEqual(self.player.get_audio_devices(), ["Device 1", "Device 2"])

    def test_set_audio_device(self):
        """Test setting the audio device."""
        self.player.player.audio_device_list = ["Device 1", "Device 2"]
        self.player.set_audio_device("Device 2")
        self.assertEqual(self.player.player.audio_device, "Device 2")

    def test_set_audio_device_invalid(self):
        """Test setting an invalid audio device."""
        self.player.player.audio_device_list = ["Device 1", "Device 2"]
        with self.assertRaises(ValueError):
            self.player.set_audio_device("Invalid Device")

    def test_get_current_audio_device(self):
        """Test getting the current audio device."""
        self.player.player.audio_device = "Device 1"
        self.assertEqual(self.player.get_current_audio_device(), "Device 1")

    def test_del(self):
        """Test the destructor."""
        player = Player()
        player.player = MagicMock()
        del player
        player.player.terminate.assert_called_once()


if __name__ == '__main__':
    unittest.main()
