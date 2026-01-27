import subprocess
import shutil
import os
import tempfile


class FlacEncoder:
    
    @staticmethod
    def is_flac_available():
        return shutil.which('flac') is not None
    
    @staticmethod
    def is_ffmpeg_available():
        return shutil.which('ffmpeg') is not None
    
    @staticmethod
    def get_available_encoder():
        if FlacEncoder.is_flac_available():
            return 'flac'
        elif FlacEncoder.is_ffmpeg_available():
            return 'ffmpeg'
        return None
    
    @staticmethod
    def reencode_flac(filepath):
        if not filepath.lower().endswith('.flac'):
            return False, "Not a FLAC file"
        
        encoder = FlacEncoder.get_available_encoder()
        if not encoder:
            return False, "Neither flac nor ffmpeg is installed"
            
        # Capture metadata before encoding
        tags_to_preserve = {}
        cover_data = None
        try:
            from tagqt.core.tags import MetadataHandler
            original_meta = MetadataHandler(filepath)
            
            # Store all tags in a dict
            for attr in ['title', 'artist', 'album', 'year', 'genre', 
                         'track_number', 'disc_number', 'album_artist', 'comment', 'lyrics',
                         'bpm', 'initial_key', 'isrc', 'publisher']:
                val = getattr(original_meta, attr)
                if val:
                    tags_to_preserve[attr] = val
            
            cover_data = original_meta.get_cover()
            
        except Exception as e:
            print(f"Warning: Could not read original metadata: {e}")

        # Force 24-bit 48kHz
        # ffmpeg flac encoder uses s32 for 24-bit
        
        temp_fd, temp_path = tempfile.mkstemp(suffix='.flac')
        os.close(temp_fd)
        os.remove(temp_path)
        
        try:
            # Construct command
            cmd = ['ffmpeg', '-y', '-i', filepath, 
                   '-map_metadata', '0',
                   '-c:a', 'flac', 
                   '-compression_level', '5',
                   '-sample_fmt', 's32',
                   '-ar', '48000']
            
            # -c:v copy to keep cover art (as a backup, though we restore manually too)
            cmd.extend(['-c:v', 'copy', temp_path])

            result = subprocess.run(
                cmd,
                capture_output=True,
                check=True
            )
            
            # Restore metadata to temp file
            try:
                from tagqt.core.tags import MetadataHandler
                new_meta = MetadataHandler(temp_path)
                
                for key, value in tags_to_preserve.items():
                    setattr(new_meta, key, value)
                
                if cover_data:
                    new_meta.set_cover(cover_data)
                    
                new_meta.save()
                
            except Exception as e:
                print(f"Warning: Could not restore metadata: {e}")
            
            shutil.move(temp_path, filepath)
            return True, None
            
        except subprocess.CalledProcessError as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return False, f"Encoding failed: {e.stderr.decode() if e.stderr else str(e)}"
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return False, str(e)


class DependencyChecker:
    
    @staticmethod
    def check_koroman():
        try:
            import koroman
            return True, None
        except ImportError:
            return False, "koroman library is not installed. Install with: pip install koroman"
    
    @staticmethod
    def check_flac_tools():
        encoder = FlacEncoder.get_available_encoder()
        if encoder:
            return True, encoder
        return False, "Neither flac nor ffmpeg is installed. Please install one of them."
