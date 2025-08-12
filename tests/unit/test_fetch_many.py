import pytest
import pathlib
from unittest.mock import Mock, patch
from downloader.fetch_many import (
    make_thumb_from_file, already_downloaded, extract_thumbnail,
    fetch_one, fetch_missing, fetch_missing_with_callbacks
)


class TestFetchMany:
    """Test suite for fetch_many module"""
    
    def test_make_thumb_from_file_creates_directory(self, tmp_path):
        """Test that thumbnail directory is created"""
        video_file = tmp_path / "test_video.mp4"
        video_file.write_text("dummy video content")
        
        with patch('downloader.fetch_many.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            make_thumb_from_file(video_file)
            
            # Verify thumbnail directory was created
            thumb_dir = pathlib.Path("data/thumbnails")
            assert thumb_dir.exists()
    
    def test_make_thumb_from_file_skips_existing(self, tmp_path):
        """Test that existing thumbnails are skipped"""
        video_file = tmp_path / "test_video.mp4"
        video_file.write_text("dummy video content")
        
        # Create existing thumbnail
        thumb_dir = pathlib.Path("data/thumbnails")
        thumb_dir.mkdir(parents=True, exist_ok=True)
        existing_thumb = thumb_dir / "test_video.jpg"
        existing_thumb.write_text("existing thumbnail")
        
        with patch('subprocess.run') as mock_run:
            make_thumb_from_file(video_file)
            
            # Should not call ffmpeg if thumbnail exists
            mock_run.assert_not_called()
    
    def test_make_thumb_from_file_calls_ffmpeg(self, tmp_path):
        """Test that ffmpeg is called correctly"""
        video_file = tmp_path / "test_video.mp4"
        video_file.write_text("dummy video content")
        
        # Ensure thumbnail directory exists but thumbnail doesn't
        thumb_dir = pathlib.Path("data/thumbnails")
        thumb_dir.mkdir(parents=True, exist_ok=True)
        thumbnail_path = thumb_dir / "test_video.jpg"
        if thumbnail_path.exists():
            thumbnail_path.unlink()
        
        with patch('downloader.fetch_many.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            make_thumb_from_file(video_file)
            
            # Verify ffmpeg command
            mock_run.assert_called_once()
            call_args = mock_run.call_args[0][0]
            assert call_args[0] == "ffmpeg"
            assert call_args[1] == "-y"
            assert call_args[2] == "-ss"
            assert call_args[3] == "0.5"
            assert call_args[4] == "-i"
            assert call_args[5] == str(video_file)
    
    def test_make_thumb_from_file_handles_ffmpeg_error(self, tmp_path):
        """Test handling of ffmpeg errors"""
        video_file = tmp_path / "test_video.mp4"
        video_file.write_text("dummy video content")
        
        with patch('downloader.fetch_many.subprocess.run') as mock_run:
            mock_run.side_effect = Exception("ffmpeg failed")
            
            # Should not raise exception
            make_thumb_from_file(video_file)
    
    def test_already_downloaded_finds_existing(self, tmp_path):
        """Test that already_downloaded finds existing files"""
        # Create media directory and existing video
        media_dir = pathlib.Path("data/media/video")
        media_dir.mkdir(parents=True, exist_ok=True)
        
        video_id = "test123"
        existing_video = media_dir / f"{video_id}.mp4"
        existing_video.write_text("existing video content")
        
        url = f"https://example.com/video/{video_id}"
        assert already_downloaded(url) is True
    
    def test_already_downloaded_not_found(self, tmp_path):
        """Test that already_downloaded returns False for missing files"""
        # Create media directory but no video
        media_dir = pathlib.Path("data/media/video")
        media_dir.mkdir(parents=True, exist_ok=True)
        
        url = "https://example.com/video/nonexistent123"
        assert already_downloaded(url) is False
    
    def test_already_downloaded_handles_different_extensions(self, tmp_path):
        """Test that already_downloaded handles different video extensions"""
        # Create media directory and existing video with different extension
        media_dir = pathlib.Path("data/media/video")
        media_dir.mkdir(parents=True, exist_ok=True)
        
        video_id = "test123"
        existing_video = media_dir / f"{video_id}.avi"
        existing_video.write_text("existing video content")
        
        url = f"https://example.com/video/{video_id}"
        assert already_downloaded(url) is True
    
    def test_extract_thumbnail_success(self, mock_cv2):
        """Test successful thumbnail extraction"""
        video_path = pathlib.Path("test_video.mp4")
        
        with patch('PIL.Image.fromarray') as mock_fromarray:
            mock_img = Mock()
            mock_fromarray.return_value = mock_img
            
            result = extract_thumbnail(video_path)
            
            assert result == mock_img
            mock_fromarray.assert_called_once()
    
    def test_extract_thumbnail_failure(self, mock_cv2):
        """Test thumbnail extraction failure"""
        video_path = pathlib.Path("test_video.mp4")
        
        # Make VideoCapture.read return False (no frame)
        mock_cv2.read.return_value = (False, None)
        
        result = extract_thumbnail(video_path)
        
        assert result is None
    
    def test_extract_thumbnail_exception(self, mock_cv2):
        """Test thumbnail extraction with exception"""
        video_path = pathlib.Path("test_video.mp4")
        
        # Make VideoCapture raise exception
        mock_cv2.read.side_effect = Exception("OpenCV error")
        
        result = extract_thumbnail(video_path)
        
        assert result is None
    
    def test_fetch_one_success(self, no_network, tmp_path):
        """Test successful video download"""
        url = "https://example.com/video/test123"
        
        # Mock yt-dlp success
        with patch('downloader.fetch_many.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            # Mock finding the downloaded file
            media_dir = pathlib.Path("data/media/video")
            media_dir.mkdir(parents=True, exist_ok=True)
            downloaded_video = media_dir / "test123.mp4"
            downloaded_video.write_text("video content")
            
            with patch('pathlib.Path.glob') as mock_glob:
                mock_glob.return_value = [downloaded_video]
                
                result = fetch_one(url)
                
                assert result is True
                
                # Verify yt-dlp was called correctly (should be the first call)
                assert mock_run.call_count >= 1
                # Find the yt-dlp call
                yt_dlp_calls = [call for call in mock_run.call_args_list if call[0][0][0] == "yt-dlp"]
                assert len(yt_dlp_calls) >= 1
                call_args = yt_dlp_calls[0][0][0]
                assert call_args[0] == "yt-dlp"
                assert call_args[1] == "-f"
                assert call_args[2] == "mp4"
    
    def test_fetch_one_failure(self, no_network):
        """Test video download failure"""
        url = "https://example.com/video/test123"
        
        # Mock yt-dlp failure
        with patch('downloader.fetch_many.subprocess.run') as mock_run:
            mock_run.side_effect = Exception("Download failed")
            
            result = fetch_one(url)
            
            assert result is False
    
    def test_fetch_one_with_thumbnail_callback(self, no_network, tmp_path):
        """Test video download with thumbnail callback"""
        url = "https://example.com/video/test123"
        callback_called = False
        
        def thumbnail_callback(img):
            nonlocal callback_called
            callback_called = True
        
        # Mock successful download and thumbnail extraction
        with patch('downloader.fetch_many.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            # Mock finding the downloaded file
            media_dir = pathlib.Path("data/media/video")
            media_dir.mkdir(parents=True, exist_ok=True)
            downloaded_video = media_dir / "test123.mp4"
            downloaded_video.write_text("video content")
            
            with patch('downloader.fetch_many.extract_thumbnail') as mock_extract:
                mock_extract.return_value = Mock()
                
                result = fetch_one(url, thumbnail_callback)
                
                assert result is True
                assert callback_called is True
                mock_extract.assert_called_once()
    
    def test_fetch_missing_with_limit(self, mock_sqlite, no_network):
        """Test fetch_missing with limit"""
        limit = 2
        
        with patch('downloader.fetch_many.fetch_one') as mock_fetch_one:
            mock_fetch_one.return_value = True
            
            fetch_missing(limit)
            
            # Should call fetch_one for each URL up to limit
            assert mock_fetch_one.call_count == 2
    
    def test_fetch_missing_skips_existing(self, mock_sqlite, no_network):
        """Test that fetch_missing skips already downloaded videos"""
        with patch('downloader.fetch_many.already_downloaded') as mock_already:
            mock_already.return_value = True  # All videos already downloaded
            
            with patch('downloader.fetch_many.fetch_one') as mock_fetch_one:
                fetch_missing()
                
                # Should not call fetch_one if already downloaded
                mock_fetch_one.assert_not_called()
    
    def test_fetch_missing_with_callbacks(self, mock_sqlite, no_network):
        """Test fetch_missing_with_callbacks functionality"""
        status_messages = []
        thumbnail_called = False
        
        def status_callback(msg):
            status_messages.append(msg)
        
        def thumbnail_callback(img):
            nonlocal thumbnail_called
            thumbnail_called = True
        
        with patch('downloader.fetch_many.already_downloaded') as mock_already:
            mock_already.return_value = False  # Video not already downloaded
            
            with patch('downloader.fetch_many.fetch_one') as mock_fetch_one:
                def mock_fetch_one_impl(url, thumbnail_callback=None):
                    if thumbnail_callback:
                        thumbnail_callback(Mock())  # Call the callback with a mock image
                    return True
                
                mock_fetch_one.side_effect = mock_fetch_one_impl
                
                fetch_missing_with_callbacks(
                    limit=1,
                    thumbnail_callback=thumbnail_callback,
                    status_callback=status_callback
                )
                
                # Verify callbacks were called
                assert len(status_messages) > 0
                assert thumbnail_called is True
                mock_fetch_one.assert_called_once()
    
    def test_fetch_missing_with_callbacks_no_limit(self, mock_sqlite, no_network):
        """Test fetch_missing_with_callbacks without limit"""
        with patch('downloader.fetch_many.fetch_one') as mock_fetch_one:
            mock_fetch_one.return_value = True
            
            fetch_missing_with_callbacks()
            
            # Should process all URLs
            assert mock_fetch_one.call_count == 2  # From mock_sqlite fixture
    
    def test_fetch_missing_with_callbacks_handles_failures(self, mock_sqlite, no_network):
        """Test fetch_missing_with_callbacks handles download failures"""
        with patch('downloader.fetch_many.already_downloaded') as mock_already:
            mock_already.return_value = False  # Video not already downloaded
            
            with patch('downloader.fetch_many.fetch_one') as mock_fetch_one:
                mock_fetch_one.return_value = False  # Download fails
                
                fetch_missing_with_callbacks(limit=1)
                
                # Should call fetch_one for each URL until limit is reached
                # Since fetch_one returns False, count doesn't increment, so it processes all URLs
                assert mock_fetch_one.call_count >= 1
    
    def test_sqlite_connection_handling(self, no_network):
        """Test SQLite connection handling in fetch functions"""
        with patch('sqlite3.connect') as mock_connect:
            mock_conn = Mock()
            mock_cursor = Mock()
            mock_cursor.fetchall.return_value = [("https://example.com/video1",)]
            mock_conn.cursor.return_value = mock_cursor
            mock_connect.return_value = mock_conn
            
            with patch('downloader.fetch_many.fetch_one') as mock_fetch_one:
                mock_fetch_one.return_value = True
                
                fetch_missing(limit=1)
                
                # Verify SQLite operations
                mock_connect.assert_called_once_with("data/db.sqlite")
                mock_conn.cursor.assert_called_once()
                mock_conn.close.assert_called_once()
    
    def test_error_handling_in_fetch_functions(self, mock_sqlite, no_network):
        """Test error handling in fetch functions"""
        with patch('downloader.fetch_many.fetch_one') as mock_fetch_one:
            mock_fetch_one.side_effect = Exception("Network error")
            
            # Should handle exceptions gracefully
            with pytest.raises(Exception):
                fetch_missing(limit=1)
            
            # Should still call fetch_one but handle the exception
            mock_fetch_one.assert_called_once()
    
    def test_media_directory_creation(self, no_network):
        """Test that media directories are created when needed"""
        url = "https://example.com/video/test123"
        
        with patch('downloader.fetch_many.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            with patch('pathlib.Path.glob') as mock_glob:
                mock_glob.return_value = []
                
                fetch_one(url)
                
                # Verify media directory was created
                media_dir = pathlib.Path("data/media/video")
                assert media_dir.exists()
    
    def test_thumbnail_directory_creation(self, tmp_path):
        """Test that thumbnail directory is created when needed"""
        video_file = tmp_path / "test_video.mp4"
        video_file.write_text("dummy video content")
        
        with patch('downloader.fetch_many.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            make_thumb_from_file(video_file)
            
            # Verify thumbnail directory was created
            thumb_dir = pathlib.Path("data/thumbnails")
            assert thumb_dir.exists()
    
    def test_smoke_test_import(self):
        """Smoke test: verify module can be imported"""
        import downloader.fetch_many
        assert hasattr(downloader.fetch_many, 'make_thumb_from_file')
        assert hasattr(downloader.fetch_many, 'already_downloaded')
        assert hasattr(downloader.fetch_many, 'extract_thumbnail')
        assert hasattr(downloader.fetch_many, 'fetch_one')
        assert hasattr(downloader.fetch_many, 'fetch_missing')
        assert hasattr(downloader.fetch_many, 'fetch_missing_with_callbacks')
