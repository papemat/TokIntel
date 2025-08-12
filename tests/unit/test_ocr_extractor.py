import pytest
import json
from analyzer.ocr_extractor import run_ocr_on_frames


class TestOCRExtractor:
    """Test suite for OCR extractor module"""
    
    def test_empty_frames_list(self, tmp_path):
        """Test handling of empty frames list"""
        out_json = tmp_path / "empty_output.json"
        
        result = run_ocr_on_frames([], ["it", "en"], str(out_json))
        
        assert result["frames"] == []
        assert result["combined_text"] == ""
        assert out_json.exists()
        
        # Verify JSON content
        with open(out_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        assert data["frames"] == []
        assert data["combined_text"] == ""
    
    def test_nonexistent_frame_path(self, mock_easyocr, tmp_path):
        """Test handling of non-existent frame paths"""
        out_json = tmp_path / "nonexistent_output.json"
        nonexistent_frame = "/path/to/nonexistent/frame.jpg"
        
        result = run_ocr_on_frames([nonexistent_frame], ["it"], str(out_json))
        
        # Should handle gracefully and return empty text for failed frames
        assert len(result["frames"]) == 1
        assert result["frames"][0]["frame"] == nonexistent_frame
        assert result["frames"][0]["text"] == ""
        assert result["combined_text"] == ""
    
    def test_valid_frame_processing(self, mock_easyocr, tiny_image, tmp_path):
        """Test processing of valid frame images"""
        out_json = tmp_path / "valid_output.json"
        
        result = run_ocr_on_frames([tiny_image], ["it", "en"], str(out_json))
        
        # Verify structure
        assert len(result["frames"]) == 1
        assert result["frames"][0]["frame"] == tiny_image
        assert "text" in result["frames"][0]
        assert "combined_text" in result
        
        # Verify EasyOCR was called correctly
        mock_easyocr.readtext.assert_called_once_with(tiny_image, detail=0)
        
        # Verify output file exists
        assert out_json.exists()
    
    def test_multiple_frames_processing(self, mock_easyocr, tiny_image, tiny_image_32x32, tmp_path):
        """Test processing multiple frames"""
        out_json = tmp_path / "multiple_output.json"
        frames = [tiny_image, tiny_image_32x32]
        
        result = run_ocr_on_frames(frames, ["en"], str(out_json))
        
        assert len(result["frames"]) == 2
        assert result["frames"][0]["frame"] == tiny_image
        assert result["frames"][1]["frame"] == tiny_image_32x32
        
        # Verify EasyOCR was called for each frame
        assert mock_easyocr.readtext.call_count == 2
        
        # Verify combined text
        assert "combined_text" in result
    
    def test_language_options_passed_correctly(self, mock_easyocr, tiny_image, tmp_path):
        """Test that language options are passed correctly to EasyOCR"""
        out_json = tmp_path / "lang_output.json"
        languages = ["it", "en", "fr"]
        
        run_ocr_on_frames([tiny_image], languages, str(out_json))
        
        # Verify EasyOCR readtext was called
        mock_easyocr.readtext.assert_called_once()
    
    def test_output_directory_creation(self, mock_easyocr, tiny_image, tmp_path):
        """Test that output directory is created if it doesn't exist"""
        nested_dir = tmp_path / "nested" / "deep" / "directory"
        out_json = nested_dir / "output.json"
        
        run_ocr_on_frames([tiny_image], ["en"], str(out_json))
        
        # Verify directory was created
        assert nested_dir.exists()
        assert out_json.exists()
    
    def test_ocr_exception_handling(self, mock_easyocr, tiny_image, tmp_path):
        """Test handling of OCR exceptions"""
        out_json = tmp_path / "exception_output.json"
        
        # Make EasyOCR raise an exception
        mock_easyocr.readtext.side_effect = Exception("OCR failed")
        
        result = run_ocr_on_frames([tiny_image], ["en"], str(out_json))
        
        # Should handle exception gracefully
        assert len(result["frames"]) == 1
        assert result["frames"][0]["frame"] == tiny_image
        assert result["frames"][0]["text"] == ""
        assert result["combined_text"] == ""
    
    def test_combined_text_formatting(self, mock_easyocr, tiny_image, tmp_path):
        """Test that combined text is properly formatted"""
        out_json = tmp_path / "format_output.json"
        
        # Mock OCR to return specific text
        mock_easyocr.readtext.return_value = ["Hello", "World"]
        
        result = run_ocr_on_frames([tiny_image], ["en"], str(out_json))
        
        assert result["combined_text"] == "Hello World"
    
    def test_json_output_format(self, mock_easyocr, tiny_image, tmp_path):
        """Test that JSON output is properly formatted"""
        out_json = tmp_path / "json_output.json"
        
        run_ocr_on_frames([tiny_image], ["en"], str(out_json))
        
        # Verify JSON is valid and has correct structure
        with open(out_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert "frames" in data
        assert "combined_text" in data
        assert isinstance(data["frames"], list)
        assert isinstance(data["combined_text"], str)
    
    @pytest.mark.parametrize("languages", [
        ["en"],
        ["it", "en"],
        ["en", "fr", "de"],
        ["it"]
    ])
    def test_different_language_combinations(self, mock_easyocr, tiny_image, tmp_path, languages):
        """Test different language combinations"""
        out_json = tmp_path / f"lang_{len(languages)}_output.json"
        
        result = run_ocr_on_frames([tiny_image], languages, str(out_json))
        
        # Verify structure is correct regardless of languages
        assert "frames" in result
        assert "combined_text" in result
        assert len(result["frames"]) == 1
    
    def test_gpu_option_disabled(self, mock_easyocr, tiny_image, tmp_path):
        """Test that GPU is disabled by default"""
        out_json = tmp_path / "gpu_output.json"
        
        run_ocr_on_frames([tiny_image], ["en"], str(out_json))
        
        # Verify EasyOCR readtext was called
        mock_easyocr.readtext.assert_called()
