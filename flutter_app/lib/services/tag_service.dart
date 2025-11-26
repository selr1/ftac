import 'package:audiotags/audiotags.dart';
import '../models/audio_file.dart';

class TagService {
  Future<AudioFile> readTags(AudioFile file) async {
    try {
      final tag = await AudioTags.read(file.path);
      return file.copyWith(
        tags: tag,
        duration: tag?.duration,
      );
    } catch (e) {
      print('Error reading tags for ${file.path}: $e');
      return file.copyWith(hasError: true, errorMessage: e.toString());
    }
  }

  Future<bool> writeTags(AudioFile file, Tag tags) async {
    try {
      await AudioTags.write(file.path, tags);
      return true;
    } catch (e) {
      print('Error writing tags for ${file.path}: $e');
      return false;
    }
  }
  
  /// Get lyrics from audio file
  Future<String?> getLyrics(AudioFile file) async {
    try {
      final tag = file.tags ?? await AudioTags.read(file.path);
      return tag?.lyrics;
    } catch (e) {
      print('Error reading lyrics for ${file.path}: $e');
      return null;
    }
  }
}
