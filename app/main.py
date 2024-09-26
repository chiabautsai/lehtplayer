import curses
import time
from player import Player

class AudioPlayerGUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.player = Player()
        self.current_track = ""
        self.volume = 100
        self.position = 0
        self.duration = 0
        self.playlist = []
        self.selected_index = 0
        self.scroll_offset = 0
        self.add_media_mode = False
        self.new_media_input = ""
        self.debug_mode = False
        self.debug_info = {}
        self.error_message = ""
        self.error_time = 0

    def draw_interface(self):
        self.stdscr.clear()
        height, width = self.stdscr.getmaxyx()

        # Title
        title = "Audio Player"
        self.stdscr.addstr(0, (width - len(title)) // 2, title, curses.A_BOLD)

        # Error message (if any)
        if self.error_message and time.time() - self.error_time < 5:  # Display error for 5 seconds
            self.stdscr.addstr(1, 2, self.error_message, curses.A_BOLD | curses.color_pair(1))

        # Current track
        self.stdscr.addstr(2, 2, f"Now playing: {self.current_track}")

        # Progress bar
        progress = int((self.position / self.duration) * (width - 4)) if self.duration else 0
        self.stdscr.addstr(4, 2, "[" + "=" * progress + " " * (width - 4 - progress) + "]")

        # Time
        time_str = f"{self.format_time(self.position)} / {self.format_time(self.duration)}"
        self.stdscr.addstr(5, (width - len(time_str)) // 2, time_str)

        # Volume
        self.stdscr.addstr(6, 2, f"Volume: {self.volume}%")

        # Playlist
        playlist_start = 8
        playlist_height = height - playlist_start - 3  # Leave space for controls
        self.stdscr.addstr(playlist_start, 2, "Playlist:", curses.A_UNDERLINE)
        
        for i in range(playlist_height):
            playlist_index = i + self.scroll_offset
            if playlist_index >= len(self.playlist):
                break
            track = self.playlist[playlist_index]
            if playlist_index == self.selected_index:
                self.stdscr.addstr(playlist_start + i + 1, 2, f"> {track}", curses.A_REVERSE)
            else:
                self.stdscr.addstr(playlist_start + i + 1, 2, f"  {track}")

        # Scroll indicators
        if self.scroll_offset > 0:
            self.stdscr.addstr(playlist_start + 1, width - 3, "↑")
        if self.scroll_offset + playlist_height < len(self.playlist):
            self.stdscr.addstr(playlist_start + playlist_height, width - 3, "↓")

        # Debug Info
        if self.debug_mode:
            debug_start = playlist_start + len(self.playlist) + 2
            self.stdscr.addstr(debug_start, 2, "Debug Info:", curses.A_UNDERLINE)
            for i, (key, value) in enumerate(self.debug_info.items()):
                if debug_start + i + 1 >= height - 3:
                    break
                self.stdscr.addstr(debug_start + i + 1, 2, f"{key}: {value}")

        # Controls
        controls = "SPACE: Play/Pause | N: Next | P: Previous | 9/0: Volume | A: Add Media | D: Debug | Q: Quit"
        self.stdscr.addstr(height - 2, 0, controls.center(width), curses.A_BOLD)

        # Add Media Input
        if self.add_media_mode:
            self.stdscr.addstr(height - 4, 2, "Enter media path or URL: ")
            self.stdscr.addstr(height - 4, 28, self.new_media_input)

        self.stdscr.refresh()

    def display_error(self, message):
        self.error_message = f"Error: {message}"
        self.error_time = time.time()

    def format_time(self, seconds):
        return time.strftime("%M:%S", time.gmtime(seconds))

    def update_player_info(self):
        track_info = self.player.get_current_track()
        self.current_track = track_info['filename'] if track_info['filename'] else "No track playing"
        self.position = self.player.get_position() or 0
        self.duration = self.player.get_duration() or 0
        self.volume = int(self.player.get_volume())
        self.playlist = self.player.get_playlist()

        # Debug info
        self.debug_info = {
            "Playlist Length": len(self.playlist),
            "Selected Index": self.selected_index,
        }

    def handle_input(self, key):
        if self.add_media_mode:
            return self.handle_add_media_input(key)
        
        if key == ord('q'):
            return False
        elif key == ord(' '):
            if self.player.is_playing():
                self.player.pause()
            else:
                self.player.resume()
        elif key == ord('n'):
            try:
                self.player.next_track()
            except ValueError as e:
                self.display_error(str(e))
        elif key == ord('p'):
            try:
                self.player.previous_track()
            except ValueError as e:
                self.display_error(str(e))
        elif key == ord('0'):
            self.player.set_volume(min(100, self.volume + 5))
        elif key == ord('9'):
            self.player.set_volume(max(0, self.volume - 5))
        elif key == curses.KEY_UP:
            self.selected_index = max(0, self.selected_index - 1)
            self.adjust_scroll()
        elif key == curses.KEY_DOWN:
            self.selected_index = min(len(self.playlist) - 1, self.selected_index + 1)
            self.adjust_scroll()
        elif key == ord('\n'):  # Enter key
            if self.playlist:
                self.player.play(playlist_pos=self.selected_index)
        elif key == ord('a'):
            self.add_media_mode = True
        elif key == ord('d'):
            self.debug_mode = not self.debug_mode
        return True

    def adjust_scroll(self):
        height, _ = self.stdscr.getmaxyx()
        playlist_height = height - 11  # Adjust based on your layout
        if self.selected_index < self.scroll_offset:
            self.scroll_offset = self.selected_index
        elif self.selected_index >= self.scroll_offset + playlist_height:
            self.scroll_offset = self.selected_index - playlist_height + 1

    def handle_add_media_input(self, key):
        if key == ord('\n'):  # Enter key
            if self.new_media_input:
                self.player.add_to_playlist(self.new_media_input)
                self.new_media_input = ""
            self.add_media_mode = False
        elif key == 27:  # Escape key
            self.new_media_input = ""
            self.add_media_mode = False
        elif key == curses.KEY_BACKSPACE or key == 127:  # Backspace
            self.new_media_input = self.new_media_input[:-1]
        elif 32 <= key <= 126:  # Printable characters
            self.new_media_input += chr(key)
        return True

    def run(self):
        curses.curs_set(0)  # Hide the cursor
        self.stdscr.timeout(100)  # Set getch() timeout to 100ms

        # Initialize color pairs
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

        running = True
        while running:
            self.update_player_info()
            self.draw_interface()
            
            key = self.stdscr.getch()
            if key != -1:
                running = self.handle_input(key)

def main(stdscr):
    gui = AudioPlayerGUI(stdscr)
    gui.run()

if __name__ == "__main__":
    curses.wrapper(main)