import pytest
import re
from fractions import Fraction
from unittest.mock import Mock, patch
from analyzer.frame_sampler import sample_frames_ffmpeg
from tests.conftest import norm_names


def _find_vf_arg(argv):
    """Find "-vf" and return its value (the next token)"""
    for i, a in enumerate(argv):
        if a == "-vf" and i + 1 < len(argv):
            return argv[i + 1]
    return None


def _extract_fps_value(vf_str: str):
    """
    Accepts strings like:
      "fps=1", "fps=1.0", "fps=1/2", "fps=1,scale=320:-1", "scale=...,fps=2"
    Returns float fps or None if no fps filter found.
    """
    if not vf_str:
        return None
    # split combined filters by comma and search fps=
    parts = [p.strip() for p in vf_str.split(",")]
    for p in parts:
        m = re.match(r"^\s*fps\s*=\s*([0-9]+(?:\.[0-9]+)?(?:/[0-9]+)?)\s*$", p)
        if m:
            val = m.group(1)
            if "/" in val:
                return float(Fraction(val))
            return float(val)
    return None


def _extract_scene_threshold(vf_str: str):
    """
    Extract scene threshold from select='gt(scene,threshold)' filter
    """
    if not vf_str:
        return None
    # Look for select='gt(scene,value)' pattern
    m = re.search(r"select\s*=\s*'gt\s*\(\s*scene\s*,\s*([0-9]+(?:\.[0-9]+)?)\s*\)'", vf_str)
    if m:
        return float(m.group(1))
    return None


class TestFrameSampler:
    """Test suite for frame sampler module"""
    
    def test_output_directory_creation(self, tmp_path, fake_frame_list):
        """Test that output directory is created"""
        out_dir = tmp_path / "frames_output"
        fake_frame_list(count=5)  # Mock 5 frames
        
        with patch('analyzer.frame_sampler.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            result = sample_frames_ffmpeg("dummy_video.mp4", str(out_dir))
            
            assert out_dir.exists()
            assert len(result) == 5
    
    def test_fps_mode_command_generation(self, tmp_path, fake_frame_list):
        """Test FPS mode command generation"""
        out_dir = tmp_path / "fps_frames"
        video_path = "test_video.mp4"
        fps = 1.0
        fake_frame_list(count=3)  # Mock 3 frames
        
        with patch('analyzer.frame_sampler.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            sample_frames_ffmpeg(video_path, str(out_dir), mode="fps", fps=fps)
            
            # Verify ffmpeg command was called with correct parameters
            mock_run.assert_called_once()
            call_args = mock_run.call_args[0][0]
            
            assert call_args[0] == "ffmpeg"
            assert call_args[1] == "-y"
            assert call_args[2] == "-i"
            assert call_args[3] == video_path
            
            # Robust verification of fps filter
            vf = _find_vf_arg(call_args)
            assert vf is not None, "ffmpeg command must include -vf argument"
            
            fps_val = _extract_fps_value(vf)
            assert fps_val is not None, f"missing fps filter in -vf: {vf}"
            assert fps_val == pytest.approx(fps, rel=0, abs=1e-6)
    
    def test_scene_mode_command_generation(self, tmp_path, fake_frame_list):
        """Test scene detection mode command generation"""
        out_dir = tmp_path / "scene_frames"
        video_path = "test_video.mp4"
        threshold = 0.3
        fake_frame_list(count=4)  # Mock 4 frames
        
        with patch('analyzer.frame_sampler.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            sample_frames_ffmpeg(video_path, str(out_dir), mode="scene", scene_threshold=threshold)
            
            # Verify ffmpeg command was called with scene detection
            mock_run.assert_called_once()
            call_args = mock_run.call_args[0][0]
            
            assert call_args[0] == "ffmpeg"
            assert call_args[1] == "-y"
            assert call_args[2] == "-i"
            assert call_args[3] == video_path
            
            # Robust verification of scene detection filter
            vf = _find_vf_arg(call_args)
            assert vf is not None, "ffmpeg command must include -vf argument"
            
            scene_val = _extract_scene_threshold(vf)
            assert scene_val is not None, f"missing scene detection filter in -vf: {vf}"
            assert scene_val == pytest.approx(threshold, rel=0, abs=1e-6)
    
    def test_ffmpeg_failure_handling(self, tmp_path, fake_frame_list):
        """Test handling of ffmpeg failures"""
        out_dir = tmp_path / "failed_frames"
        fake_frame_list(count=0)  # Mock no frames when ffmpeg fails
        
        with patch('analyzer.frame_sampler.subprocess.run') as mock_run:
            mock_run.side_effect = Exception("ffmpeg failed")
            
            result = sample_frames_ffmpeg("dummy_video.mp4", str(out_dir))
            
            assert result == []
    
    def test_frame_limiting(self, tmp_path, fake_frame_list):
        """Test that frame count is limited correctly"""
        out_dir = tmp_path / "limited_frames"
        max_frames = 5
        frames = fake_frame_list(count=10, max_frames=max_frames)  # Mock 10 frames, should be limited to 5
        
        with patch('analyzer.frame_sampler.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            result = sample_frames_ffmpeg("dummy_video.mp4", str(out_dir), max_frames=max_frames)
            
            # Should return only max_frames
            assert len(result) == max_frames
    
    def test_image_resizing(self, tmp_path, mock_pil_image, fake_frame_list):
        """Test image resizing functionality"""
        out_dir = tmp_path / "resized_frames"
        resize_width = 256
        fake_frame_list(count=1)  # Mock 1 frame
        
        with patch('analyzer.frame_sampler.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            with patch('PIL.Image.open') as mock_open:
                mock_img = Mock()
                mock_img.size = (1024, 768)  # Large image
                mock_img.resize.return_value = mock_img
                mock_open.return_value = mock_img
                
                result = sample_frames_ffmpeg("dummy_video.mp4", str(out_dir), resize_width=resize_width)
                
                # Verify resize was called
                mock_img.resize.assert_called_once()
                resize_args = mock_img.resize.call_args[0]
                assert resize_args[0][0] == resize_width  # width
    
    def test_no_resize_for_small_images(self, tmp_path, mock_pil_image, fake_frame_list):
        """Test that small images are not resized"""
        out_dir = tmp_path / "small_frames"
        resize_width = 512
        fake_frame_list(count=1)  # Mock 1 frame
        
        with patch('analyzer.frame_sampler.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            with patch('PIL.Image.open') as mock_open:
                mock_img = Mock()
                mock_img.size = (256, 192)  # Small image
                mock_img.resize.return_value = mock_img
                mock_open.return_value = mock_img
                
                result = sample_frames_ffmpeg("dummy_video.mp4", str(out_dir), resize_width=resize_width)
                
                # Verify resize was not called for small images
                mock_img.resize.assert_not_called()
    
    def test_empty_result_handling(self, tmp_path, fake_frame_list):
        """Test handling when no frames are extracted"""
        out_dir = tmp_path / "empty_frames"
        fake_frame_list(count=0)  # Mock no frames
        
        with patch('analyzer.frame_sampler.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            result = sample_frames_ffmpeg("dummy_video.mp4", str(out_dir))
            
            assert result == []
    
    def test_frame_cleanup(self, tmp_path, fake_frame_list):
        """Test cleanup of extra frames beyond max_frames"""
        out_dir = tmp_path / "cleanup_frames"
        max_frames = 3
        fake_frame_list(count=5)  # Mock 5 frames, should clean up 2
        
        with patch('analyzer.frame_sampler.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            with patch('pathlib.Path.unlink') as mock_unlink:
                result = sample_frames_ffmpeg("dummy_video.mp4", str(out_dir), max_frames=max_frames)
                
                # Verify cleanup was called for extra frames
                assert mock_unlink.call_count == 2  # 5 total - 3 max = 2 to delete
    
    def test_return_sorted_frame_paths(self, tmp_path, fake_frame_list):
        """Test that returned frame paths are sorted"""
        out_dir = tmp_path / "sorted_frames"
        fake_frame_list(count=3)  # Mock 3 frames
        
        with patch('analyzer.frame_sampler.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            result = sample_frames_ffmpeg("dummy_video.mp4", str(out_dir))
            
            # Verify paths are sorted (normalize to just filenames)
            expected = ["frame_000001.jpg", "frame_000002.jpg", "frame_000003.jpg"]
            assert norm_names(result) == expected
    
    @pytest.mark.parametrize("mode,fps,threshold", [
        ("fps", 0.5, 0.4),
        ("fps", 1.0, 0.4),
        ("scene", 0.5, 0.3),
        ("scene", 0.5, 0.5),
    ])
    def test_different_sampling_modes(self, tmp_path, fake_frame_list, mode, fps, threshold):
        """Test different sampling mode combinations"""
        out_dir = tmp_path / f"{mode}_frames"
        fake_frame_list(count=2)  # Mock 2 frames
        
        with patch('analyzer.frame_sampler.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            result = sample_frames_ffmpeg(
                "dummy_video.mp4", str(out_dir), 
                mode=mode, fps=fps, scene_threshold=threshold
            )
            
            # Should handle all combinations gracefully
            assert isinstance(result, list)
            assert len(result) == 2
    
    def test_default_parameters(self, tmp_path, fake_frame_list):
        """Test that default parameters work correctly"""
        out_dir = tmp_path / "default_frames"
        fake_frame_list(count=1)  # Mock 1 frame
        
        with patch('analyzer.frame_sampler.subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            
            result = sample_frames_ffmpeg("dummy_video.mp4", str(out_dir))
            
            # Should work with all defaults
            assert isinstance(result, list)
            assert len(result) == 1
            
            # Verify default mode is scene
            call_args = mock_run.call_args[0][0]
            vf = _find_vf_arg(call_args)
            assert vf is not None, "ffmpeg command must include -vf argument"
            
            # Default scene threshold is 0.4
            scene_val = _extract_scene_threshold(vf)
            assert scene_val is not None, f"missing scene detection filter in -vf: {vf}"
            assert scene_val == pytest.approx(0.4, rel=0, abs=1e-6)
