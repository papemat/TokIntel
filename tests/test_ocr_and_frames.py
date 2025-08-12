import unittest
from unittest.mock import patch, MagicMock
import json
import pathlib
import tempfile
import shutil

from analyzer.ocr_extractor import run_ocr_on_frames

class TestOCRAndFrames(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.frames_dir = pathlib.Path(self.test_dir) / "vid_99999"
        self.frames_dir.mkdir(parents=True)
        
        # Create dummy images
        from PIL import Image, ImageDraw, ImageFont
        
        texts = ["Hello", "World"]
        for i, text in enumerate(texts, 1):
            img = Image.new("RGB", (800, 450), (255, 255, 255))
            drw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 48)
            except:
                font = ImageFont.load_default()
            
            bbox = drw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (800 - text_width) // 2
            y = (450 - text_height) // 2
            
            drw.text((x, y), text, fill=(0, 0, 0), font=font)
            img.save(self.frames_dir / f"frame_{i:05d}.jpg")
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    @patch('analyzer.ocr_extractor.easyocr.Reader')
    def test_run_ocr_on_frames(self, mock_reader):
        """Test OCR extraction with mocked EasyOCR"""
        # Setup mock
        mock_instance = MagicMock()
        mock_instance.readtext.return_value = ["Hello", "World"]
        mock_reader.return_value = mock_instance
        
        # Get frame paths
        frames = sorted([str(p) for p in self.frames_dir.glob("*.jpg")])
        out_json = pathlib.Path(self.test_dir) / "ocr_result.json"
        
        # Run OCR
        result = run_ocr_on_frames(frames, ["en"], str(out_json))
        
        # Verify results
        self.assertIn("frames", result)
        self.assertIn("combined_text", result)
        self.assertGreater(len(result["combined_text"]), 0)
        self.assertEqual(len(result["frames"]), 2)
        
        # Verify JSON file was created
        self.assertTrue(out_json.exists())
        
        # Verify JSON content
        with open(out_json, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            self.assertEqual(json_data["combined_text"], "Hello World")
    
    def test_run_ocr_empty_frames(self):
        """Test OCR with empty frame list"""
        out_json = pathlib.Path(self.test_dir) / "empty_ocr.json"
        
        result = run_ocr_on_frames([], ["en"], str(out_json))
        
        self.assertEqual(result["frames"], [])
        self.assertEqual(result["combined_text"], "")
        
        # Verify JSON file was created
        self.assertTrue(out_json.exists())

if __name__ == "__main__":
    unittest.main()
