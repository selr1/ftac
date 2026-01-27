import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError, USLT, APIC
from mutagen.flac import FLAC, Picture
from mutagen.oggvorbis import OggVorbis
from mutagen.mp4 import MP4, MP4Cover
import os
from PIL import Image
import io

class MetadataHandler:
    def __init__(self, filepath):
        self.filepath = filepath
        self.audio = None
        self.load_file()

    def load_file(self):
        try:
            self.audio = mutagen.File(self.filepath, easy=True)
            if self.audio is None:
                # Fallback for some MP3s
                try:
                    self.audio = EasyID3(self.filepath)
                except ID3NoHeaderError:
                    self.audio = mutagen.File(self.filepath)
                    self.audio.add_tags()
        except Exception as e:
            print(f"Error loading file {self.filepath}: {e}")

    def get_tag(self, tag):
        if self.audio and tag in self.audio:
            return self.audio[tag][0]
        return ""

    def set_tag(self, tag, value):
        if self.audio:
            if isinstance(value, list):
                # Deduplicate while preserving order
                deduped = list(dict.fromkeys(str(v) for v in value))
                self.audio[tag] = deduped
            else:
                self.audio[tag] = [str(value)]

    def save(self):
        if self.audio:
            self.audio.save()
            # Auto-save lyrics to .lrc if present
            if self.lyrics:
                self.save_lyrics_file()

    def save_lyrics_file(self):
        """Saves lyrics to a .lrc file with the same name as the audio file."""
        if not self.lyrics:
            return
            
        try:
            base_path = os.path.splitext(self.filepath)[0]
            lrc_path = base_path + ".lrc"
            
            with open(lrc_path, 'w', encoding='utf-8') as f:
                f.write(self.lyrics)
        except Exception as e:
            print(f"Error saving lyrics file: {e}")

    def save_cover_file(self, data=None, overwrite=True):
        """
        Saves cover art to cover.jpg in the same directory.
        If data is provided, uses it. Otherwise tries to get from tags.
        If overwrite is False, checks if file exists first.
        """
        try:
            if data is None:
                data = self.get_cover()
            
            if not data:
                return

            dir_path = os.path.dirname(self.filepath)
            cover_path = os.path.join(dir_path, "cover.jpg")
            
            if not overwrite and os.path.exists(cover_path):
                return
                
            with open(cover_path, 'wb') as f:
                f.write(data)
        except Exception as e:
            print(f"Error saving cover file: {e}")

    @property
    def title(self):
        return self.get_tag('title')

    @title.setter
    def title(self, value):
        self.set_tag('title', value)

    @property
    def artist(self):
        return self.get_tag('artist')

    @artist.setter
    def artist(self, value):
        self.set_tag('artist', value)

    @property
    def album(self):
        return self.get_tag('album')

    @album.setter
    def album(self, value):
        self.set_tag('album', value)

    @property
    def year(self):
        return self.get_tag('date')

    @year.setter
    def year(self, value):
        self.set_tag('date', value)

    @property
    def genre(self):
        return self.get_tag('genre')

    @genre.setter
    def genre(self, value):
        self.set_tag('genre', value)

    @property
    def track_number(self):
        return self.get_tag('tracknumber')

    @track_number.setter
    def track_number(self, value):
        self.set_tag('tracknumber', value)

    @property
    def disc_number(self):
        val = self.get_tag('discnumber')
        # For FLAC/Ogg, try to combine with total if available and not already in val
        if self.audio and isinstance(self.audio, (FLAC, OggVorbis)):
            if '/' not in str(val) and 'DISCTOTAL' in self.audio:
                total = self.audio['DISCTOTAL'][0]
                return f"{val}/{total}"
        return val

    @disc_number.setter
    def disc_number(self, value):
        if self.audio and isinstance(self.audio, (FLAC, OggVorbis)) and value and '/' in str(value):
            try:
                num, total = str(value).split('/')
                self.set_tag('discnumber', num)
                self.audio['DISCTOTAL'] = [str(total)]
                return
            except ValueError:
                pass
        self.set_tag('discnumber', value)

    @property
    def track_total(self):
        if self.audio and isinstance(self.audio, (FLAC, OggVorbis)):
            if 'TRACKTOTAL' in self.audio:
                return self.audio['TRACKTOTAL'][0]
        return ""

    @track_total.setter
    def track_total(self, value):
        if self.audio and isinstance(self.audio, (FLAC, OggVorbis)):
            if value:
                self.audio['TRACKTOTAL'] = [str(value)]
            elif 'TRACKTOTAL' in self.audio:
                del self.audio['TRACKTOTAL']

    @property
    def album_artist(self):
        return self.get_tag('albumartist')

    @album_artist.setter
    def album_artist(self, value):
        self.set_tag('albumartist', value)

    @property
    def comment(self):
        # Comments are tricky in EasyID3, often not mapped standardly or as 'comment'
        # For now, let's try 'comment' or fallback to raw tags if needed.
        # EasyID3 maps 'comment' to COMM frames.
        return self.get_tag('comment')

    @comment.setter
    def comment(self, value):
        self.set_tag('comment', value)

    @property
    def lyrics(self):
        """Returns lyrics from tags."""
        if self.audio is None:
            return ""
            
        try:
            # ID3 (MP3)
            if isinstance(self.audio, (ID3, EasyID3)) or hasattr(self.audio, 'tags') and isinstance(self.audio.tags, (ID3, EasyID3)):
                tags = self.audio if isinstance(self.audio, ID3) else self.audio.tags
                if tags:
                    for key in tags.keys():
                        if key.startswith('USLT:'):
                            return tags[key].text
            
            # FLAC / Ogg
            elif isinstance(self.audio, (FLAC, OggVorbis)):
                if 'LYRICS' in self.audio:
                    return self.audio['LYRICS'][0]
            
            # MP4
            elif isinstance(self.audio, MP4):
                if '\xa9lyr' in self.audio:
                    return self.audio['\xa9lyr'][0]
                    
        except Exception as e:
            print(f"Error getting lyrics: {e}")
        return ""

    @lyrics.setter
    def lyrics(self, value):
        """Sets lyrics to tags."""
        if self.audio is None:
            return

        try:
            # ID3 (MP3)
            if isinstance(self.audio, (ID3, EasyID3)) or hasattr(self.audio, 'tags') and isinstance(self.audio.tags, (ID3, EasyID3)):
                tags = self.audio if isinstance(self.audio, ID3) else self.audio.tags
                if tags is not None:
                    # Remove existing
                    to_del = [k for k in tags.keys() if k.startswith('USLT:')]
                    for k in to_del:
                        del tags[k]
                    
                    if value:
                        tags.add(USLT(
                            encoding=3,
                            lang='eng', # Default to eng
                            desc='',
                            text=value
                        ))
            
            # FLAC
            elif isinstance(self.audio, (FLAC, OggVorbis)):
                if value:
                    self.audio['LYRICS'] = value
                elif 'LYRICS' in self.audio:
                    del self.audio['LYRICS']
            
            # MP4
            elif isinstance(self.audio, MP4):
                if value:
                    self.audio['\xa9lyr'] = value
                elif '\xa9lyr' in self.audio:
                    del self.audio['\xa9lyr']
                
        except Exception as e:
            print(f"Error setting lyrics: {e}")

    @property
    def bpm(self):
        return self.get_tag('bpm')

    @bpm.setter
    def bpm(self, value):
        self.set_tag('bpm', value)

    @property
    def initial_key(self):
        return self.get_tag('initialkey')

    @initial_key.setter
    def initial_key(self, value):
        self.set_tag('initialkey', value)

    @property
    def isrc(self):
        return self.get_tag('isrc')

    @isrc.setter
    def isrc(self, value):
        self.set_tag('isrc', value)

    @property
    def publisher(self):
        return self.get_tag('organization')

    @publisher.setter
    def publisher(self, value):
        self.set_tag('organization', value)

    @property
    def duration(self):
        try:
            if self.audio and hasattr(self.audio, 'info') and self.audio.info:
                return int(self.audio.info.length)
        except Exception:
            pass
        return 0

    @property
    def bitrate(self):
        try:
            if self.audio and hasattr(self.audio, 'info') and hasattr(self.audio.info, 'bitrate'):
                return int(self.audio.info.bitrate / 1000) # kbps
        except Exception:
            pass
        return 0

    @property
    def sample_rate(self):
        try:
            if self.audio and hasattr(self.audio, 'info') and hasattr(self.audio.info, 'sample_rate'):
                return int(self.audio.info.sample_rate / 1000) # kHz
        except Exception:
            pass
        return 0

    @property
    def filesize(self):
        try:
            size_bytes = os.path.getsize(self.filepath)
            return round(size_bytes / (1024 * 1024), 2) # MB
        except Exception:
            pass
        return 0.0

    def get_cover(self):
        if self.audio is None:
            return None

        try:
            # ID3 (MP3)
            if isinstance(self.audio, (ID3, EasyID3)):
                tags = self.audio
                if hasattr(tags, '_ID3__id3'): # EasyID3 internal
                    tags = tags._ID3__id3
                
                for key in tags.keys():
                    if key.startswith('APIC:'):
                        return tags[key].data
            
            elif hasattr(self.audio, 'tags') and not isinstance(self.audio, (FLAC, OggVorbis)):
                # Other formats with .tags attribute (like MP4)
                tags = self.audio.tags
                if tags:
                    # Handle MP4 covers separately if needed, but let's see
                    if isinstance(self.audio, MP4) and 'covr' in tags:
                        return bytes(tags['covr'][0])
                    
                    # Fallback for others
                    for key in tags.keys():
                        if key.startswith('APIC:'):
                            return tags[key].data

            # FLAC / Ogg (Directly on the object)
            if isinstance(self.audio, (FLAC, OggVorbis)):
                if hasattr(self.audio, 'pictures') and self.audio.pictures:
                    return self.audio.pictures[0].data
                # Some Ogg might have it in tags? Usually FLAC uses pictures.

            # MP4
            elif isinstance(self.audio, MP4):
                if 'covr' in self.audio and self.audio['covr']:
                    return bytes(self.audio['covr'][0])

        except Exception as e:
            print(f"Error getting cover: {e}")
        return None

    def set_cover(self, data, max_size=500):
        """Sets the cover art, optionally resizing it."""
        if self.audio is None or not data:
            return

        # Resize if needed
        if max_size and max_size > 0:
            try:
                img = Image.open(io.BytesIO(data))
                
                if img.width > max_size or img.height > max_size:
                    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                    
                    # Save back to bytes
                    output = io.BytesIO()
                    # Preserve format if possible, but APIC usually expects JPEG or PNG. 
                    # Let's default to JPEG for compatibility and size.
                    img = img.convert('RGB')
                    img.save(output, format='JPEG', quality=85)
                    data = output.getvalue()
            except Exception as e:
                print(f"Error resizing cover: {e}")
                # Proceed with original data if resize fails

        try:
            # ID3 (MP3)
            if isinstance(self.audio, (ID3, EasyID3)) or hasattr(self.audio, 'tags') and isinstance(self.audio.tags, (ID3, EasyID3)):
                tags = self.audio if isinstance(self.audio, ID3) else self.audio.tags
                if tags is not None:
                    # Remove existing
                    to_del = [k for k in tags.keys() if k.startswith('APIC:')]
                    for k in to_del:
                        del tags[k]
                    
                    tags.add(APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,
                        desc='Cover',
                        data=data
                    ))
            
            # FLAC
            elif isinstance(self.audio, (FLAC, OggVorbis)):
                self.audio.clear_pictures()
                p = Picture()
                p.data = data
                p.type = 3
                p.mime = "image/jpeg"
                self.audio.add_picture(p)
            
            # MP4
            elif isinstance(self.audio, MP4):
                self.audio['covr'] = [MP4Cover(data, imageformat=MP4Cover.FORMAT_JPEG)]
                
        except Exception as e:
            print(f"Error setting cover: {e}")
