class Romanizer:
    @staticmethod
    def romanize_text(text):
        if not text:
            return ""
        try:
            from koroman import romanize
            return romanize(text)
        except ImportError:
            raise ImportError("koroman library is not installed. Install with: pip install koroman")
        except Exception as e:
            print(f"Error romanizing text: {e}")
            return text
