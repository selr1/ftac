import requests

class LyricsFetcher:
    BASE_URL = "https://lrclib.net/api/search"

    def search_lyrics(self, artist, title, album=None):
        params = {
            "q": f"{artist} {title}",
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Filter/Process results
            results = []
            for item in data:
                # Basic filtering if needed, but search usually returns relevant stuff
                results.append({
                    "id": item.get("id"),
                    "trackName": item.get("trackName"),
                    "artistName": item.get("artistName"),
                    "albumName": item.get("albumName"),
                    "duration": item.get("duration"),
                    "syncedLyrics": item.get("syncedLyrics"),
                    "plainLyrics": item.get("plainLyrics"),
                    "isSynced": bool(item.get("syncedLyrics"))
                })
            return results
        except requests.exceptions.RequestException as e:
            print(f"Error fetching lyrics: {e}")
            return []
