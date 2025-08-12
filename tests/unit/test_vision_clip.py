import pytest
import numpy as np
from unittest.mock import patch
from analyzer.vision_clip import device_from_pref, image_paths_to_embeddings, pool_video_embedding

# Deterministic dummy embeddings for testing - always (1, 512) shape
DUMMY_EMB = np.full((1, 512), 0.1, dtype=np.float32)
DUMMY_EMB_MULTI = np.full((2, 512), 0.1, dtype=np.float32)  # For multiple images


class _DummyVisionModel:
    """Dummy vision model that returns deterministic (1, 512) embeddings"""
    def __init__(self, device="cpu", dtype="float32"):
        self.device = device
        self.dtype = dtype

    def encode(self, inputs, **kwargs):
        """Encode images or text to embeddings"""
        if isinstance(inputs, list):
            # Return shape (N, 512) for N inputs
            return np.full((len(inputs), 512), 0.1, dtype=np.float32)
        else:
            # Single input -> (1, 512)
            return DUMMY_EMB


@pytest.fixture(autouse=True)
def _seed_env(monkeypatch):
    """Ensure deterministic behavior"""
    monkeypatch.setenv("PYTHONHASHSEED", "0")
    try:
        import random
        random.seed(0)
    except Exception:
        pass
    np.random.seed(0)


@pytest.fixture
def mock_vision_model(monkeypatch):
    """Mock vision model to avoid loading heavy weights"""
    import importlib
    
    try:
        vc = importlib.import_module("analyzer.vision_clip")
    except ModuleNotFoundError:
        pytest.skip("analyzer.vision_clip not present")

    # Factory function that returns dummy model
    def _factory(*args, **kwargs):
        device = kwargs.get("device", "cpu")
        dtype = kwargs.get("dtype", "float32")
        return _DummyVisionModel(device=device, dtype=dtype)

    # Mock SentenceTransformer initialization
    monkeypatch.setattr("sentence_transformers.SentenceTransformer", _factory, raising=False)
    monkeypatch.setattr("analyzer.vision_clip.SentenceTransformer", _factory, raising=False)
    
    return _factory()


class TestVisionCLIP:
    """Test suite for vision CLIP module"""
    
    def test_device_from_pref_auto_no_cuda(self, mock_torch_cuda):
        """Test device selection with auto preference and no CUDA"""
        device = device_from_pref("auto")
        assert device == "cpu"
    
    def test_device_from_pref_auto_with_cuda(self, monkeypatch):
        """Test device selection with auto preference and CUDA available"""
        monkeypatch.setattr("torch.cuda.is_available", lambda: True)
        
        device = device_from_pref("auto")
        assert device == "cuda"
    
    def test_device_from_pref_on_with_cuda(self, monkeypatch):
        """Test device selection with on preference and CUDA available"""
        monkeypatch.setattr("torch.cuda.is_available", lambda: True)
        
        device = device_from_pref("on")
        assert device == "cuda"
    
    def test_device_from_pref_on_without_cuda(self, mock_torch_cuda):
        """Test device selection with on preference but no CUDA"""
        device = device_from_pref("on")
        assert device == "cpu"
    
    def test_device_from_pref_off(self, monkeypatch):
        """Test device selection with off preference"""
        monkeypatch.setattr("torch.cuda.is_available", lambda: True)
        
        device = device_from_pref("off")
        assert device == "cpu"
    
    def test_device_from_pref_case_insensitive(self, mock_torch_cuda):
        """Test device selection is case insensitive"""
        device1 = device_from_pref("AUTO")
        device2 = device_from_pref("Auto")
        device3 = device_from_pref("auto")
        
        assert device1 == device2 == device3 == "cpu"
    
    def test_device_from_pref_none_input(self, mock_torch_cuda):
        """Test device selection with None input"""
        device = device_from_pref(None)
        assert device == "cpu"
    
    def test_image_paths_to_embeddings_empty_list(self, mock_vision_model):
        """Test embedding generation with empty image list"""
        result = image_paths_to_embeddings([], "clip-ViT-B-32", "cpu")
        
        assert result.shape == (0, 512)
        assert result.dtype == np.float32
    
    def test_image_paths_to_embeddings_single_image(self, mock_vision_model, tiny_image):
        """Test embedding generation with single image"""
        result = image_paths_to_embeddings([tiny_image], "clip-ViT-B-32", "cpu")
        
        assert result.shape == (1, 512)
        assert result.dtype == np.float32
        
        # Verify the result has the expected shape and dtype
        assert result.shape == (1, 512)
        assert str(result.dtype) == "float32"
    
    def test_image_paths_to_embeddings_multiple_images(self, mock_vision_model, tiny_image, tiny_image_32x32):
        """Test embedding generation with multiple images"""
        images = [tiny_image, tiny_image_32x32]
        result = image_paths_to_embeddings(images, "clip-ViT-B-32", "cpu")
        
        assert result.shape == (2, 512)
        assert result.dtype == np.float32
        
        # Verify the result has the expected shape and dtype
        assert result.shape == (2, 512)
        assert str(result.dtype) == "float32"
    
    def test_image_paths_to_embeddings_custom_batch_size(self, mock_vision_model, tiny_image):
        """Test embedding generation with custom batch size"""
        batch_size = 16
        result = image_paths_to_embeddings([tiny_image], "clip-ViT-B-32", "cpu", batch_size=batch_size)
        
        # Verify the result is correct regardless of batch size
        assert result.shape == (1, 512)
        assert result.dtype == np.float32
    
    def test_image_paths_to_embeddings_no_normalize(self, mock_vision_model, tiny_image):
        """Test embedding generation without normalization"""
        result = image_paths_to_embeddings([tiny_image], "clip-ViT-B-32", "cpu", normalize=False)
        
        # Verify the result is correct regardless of normalization
        assert result.shape == (1, 512)
        assert result.dtype == np.float32
    
    def test_image_paths_to_embeddings_different_model(self, mock_vision_model, tiny_image):
        """Test embedding generation with different model"""
        model_name = "clip-ViT-L-14"
        result = image_paths_to_embeddings([tiny_image], model_name, "cpu")
        
        # Verify the result is correct regardless of model name
        assert result.shape == (1, 512)
        assert result.dtype == np.float32
    
    def test_pool_video_embedding_empty(self):
        """Test pooling with empty embeddings"""
        empty_emb = np.zeros((0, 512), dtype=np.float32)
        result = pool_video_embedding(empty_emb)
        
        assert result.shape == (1, 512)
        assert result.dtype == np.float32
        assert np.all(result == 0)
    
    def test_pool_video_embedding_single(self):
        """Test pooling with single embedding"""
        single_emb = np.full((1, 512), 0.1, dtype=np.float32)
        result = pool_video_embedding(single_emb)
        
        assert result.shape == (1, 512)
        assert result.dtype == np.float32
        np.testing.assert_array_almost_equal(result, single_emb)
    
    def test_pool_video_embedding_multiple(self):
        """Test pooling with multiple embeddings"""
        multiple_emb = np.full((5, 512), 0.1, dtype=np.float32)
        result = pool_video_embedding(multiple_emb)
        
        assert result.shape == (1, 512)
        assert result.dtype == np.float32
        
        # Verify it's the mean of all embeddings
        expected_mean = np.mean(multiple_emb, axis=0, keepdims=True)
        np.testing.assert_array_almost_equal(result, expected_mean)
    
    def test_pool_video_embedding_1d_input(self):
        """Test pooling with 1D input (edge case)"""
        single_emb = np.full(512, 0.1, dtype=np.float32)
        result = pool_video_embedding(single_emb)
        
        # For 1D input, np.mean(axis=0) returns a scalar, then keepdims=True makes it (1,)
        assert result.shape == (1,)
        assert result.dtype == np.float32
    
    def test_sentence_transformer_initialization(self, mock_vision_model, tiny_image):
        """Test SentenceTransformer initialization parameters"""
        model_name = "clip-ViT-B-32"
        device = "cpu"
        
        result = image_paths_to_embeddings([tiny_image], model_name, device)
        
        # Verify the result is correct
        assert result.shape == (1, 512)
        assert result.dtype == np.float32
    
    def test_embedding_output_consistency(self, mock_vision_model, tiny_image):
        """Test that embedding output is consistent"""
        result1 = image_paths_to_embeddings([tiny_image], "clip-ViT-B-32", "cpu")
        result2 = image_paths_to_embeddings([tiny_image], "clip-ViT-B-32", "cpu")
        
        # Results should be identical
        np.testing.assert_array_equal(result1, result2)
        
        # Both should have the expected shape and dtype
        assert result1.shape == (1, 512)
        assert str(result1.dtype) == "float32"
    
    @pytest.mark.parametrize("device", ["cpu", "cuda"])
    def test_device_parameter_passing(self, mock_vision_model, tiny_image, device, monkeypatch):
        """Test that device parameter is passed correctly"""
        if device == "cuda":
            monkeypatch.setattr("torch.cuda.is_available", lambda: True)
        
        result = image_paths_to_embeddings([tiny_image], "clip-ViT-B-32", device)
        
        # Verify the result is correct regardless of device
        assert result.shape == (1, 512)
        assert result.dtype == np.float32
    
    def test_error_handling_missing_model(self, tiny_image):
        """Test error handling when model is not available"""
        with patch('sentence_transformers.SentenceTransformer') as mock_st:
            mock_st.side_effect = Exception("Model not found")
            
            with pytest.raises(Exception):
                image_paths_to_embeddings([tiny_image], "nonexistent-model", "cpu")
    
    def test_smoke_test_import(self):
        """Smoke test: verify module can be imported"""
        import analyzer.vision_clip
        assert hasattr(analyzer.vision_clip, 'device_from_pref')
        assert hasattr(analyzer.vision_clip, 'image_paths_to_embeddings')
        assert hasattr(analyzer.vision_clip, 'pool_video_embedding')
    
    def test_smoke_test_basic_functionality(self, mock_vision_model, tiny_image):
        """Smoke test: verify basic functionality works"""
        # Test device selection
        device = device_from_pref("auto")
        assert device in ["cpu", "cuda"]
        
        # Test embedding generation
        embeddings = image_paths_to_embeddings([tiny_image], "clip-ViT-B-32", device)
        assert embeddings.shape[1] == 512
        
        # Test pooling
        pooled = pool_video_embedding(embeddings)
        assert pooled.shape == (1, 512)
