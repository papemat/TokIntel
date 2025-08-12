import unittest
from unittest.mock import patch, MagicMock
import numpy as np

from analyzer.vision_clip import device_from_pref, image_paths_to_embeddings, pool_video_embedding

class TestVisionCLIP(unittest.TestCase):
    
    def test_device_from_pref(self):
        """Test device preference logic"""
        # Test auto mode with CUDA available
        with patch('analyzer.vision_clip.torch.cuda.is_available', return_value=True):
            self.assertEqual(device_from_pref("auto"), "cuda")
            self.assertEqual(device_from_pref("on"), "cuda")
            self.assertEqual(device_from_pref("off"), "cpu")
        
        # Test auto mode with CUDA not available
        with patch('analyzer.vision_clip.torch.cuda.is_available', return_value=False):
            self.assertEqual(device_from_pref("auto"), "cpu")
            self.assertEqual(device_from_pref("on"), "cpu")
            self.assertEqual(device_from_pref("off"), "cpu")
    
    @patch('analyzer.vision_clip.SentenceTransformer')
    def test_image_paths_to_embeddings(self, mock_transformer):
        """Test image embedding generation with mocked SentenceTransformer"""
        # Setup mock
        mock_model = MagicMock()
        mock_model.encode.return_value = np.random.rand(3, 512).astype(np.float32)
        mock_transformer.return_value = mock_model
        
        # Test with dummy image paths
        img_paths = ["/path/to/img1.jpg", "/path/to/img2.jpg", "/path/to/img3.jpg"]
        
        result = image_paths_to_embeddings(
            img_paths, "clip-ViT-B-32", "cpu", batch_size=32, normalize=True
        )
        
        # Verify results
        self.assertEqual(result.shape, (3, 512))
        self.assertEqual(result.dtype, np.float32)
        mock_model.encode.assert_called_once()
    
    def test_image_paths_to_embeddings_empty(self):
        """Test embedding generation with empty image list"""
        result = image_paths_to_embeddings([], "clip-ViT-B-32", "cpu")
        
        self.assertEqual(result.shape, (0, 512))
        self.assertEqual(result.dtype, np.float32)
    
    def test_pool_video_embedding(self):
        """Test video embedding pooling"""
        # Test with multiple frame embeddings
        frame_embs = np.random.rand(5, 512).astype(np.float32)
        result = pool_video_embedding(frame_embs)
        
        self.assertEqual(result.shape, (1, 512))
        self.assertEqual(result.dtype, np.float32)
        
        # Verify it's the mean of input embeddings
        expected_mean = np.mean(frame_embs, axis=0, keepdims=True)
        np.testing.assert_array_almost_equal(result, expected_mean)
    
    def test_pool_video_embedding_empty(self):
        """Test pooling with empty embeddings"""
        empty_embs = np.zeros((0, 512), dtype=np.float32)
        result = pool_video_embedding(empty_embs)
        
        self.assertEqual(result.shape, (1, 512))
        self.assertEqual(result.dtype, np.float32)
        np.testing.assert_array_equal(result, np.zeros((1, 512), dtype=np.float32))
    
    def test_pool_video_embedding_single(self):
        """Test pooling with single frame embedding"""
        single_emb = np.random.rand(1, 512).astype(np.float32)
        result = pool_video_embedding(single_emb)
        
        self.assertEqual(result.shape, (1, 512))
        self.assertEqual(result.dtype, np.float32)
        np.testing.assert_array_almost_equal(result, single_emb)

if __name__ == "__main__":
    unittest.main()
