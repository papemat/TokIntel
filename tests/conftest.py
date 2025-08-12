import os
import pytest
import pathlib
from unittest.mock import Mock
import numpy as np

# Set deterministic seeds for reproducible tests
os.environ["PYTHONHASHSEED"] = "42"
np.random.seed(42)

@pytest.fixture(scope="session")
def tmp_media(tmp_path_factory):
    """Create temporary media directory with test images"""
    tmp_dir = tmp_path_factory.mktemp("media")
    
    # Create tiny test images
    try:
        from PIL import Image
        
        # Create tiny.jpg (16x16)
        tiny_img = Image.new('RGB', (16, 16), color='red')
        tiny_path = tmp_dir / "tiny.jpg"
        tiny_img.save(tiny_path, "JPEG", quality=90)
        
        # Create tiny2.jpg (32x32)
        tiny2_img = Image.new('RGB', (32, 32), color='blue')
        tiny2_path = tmp_dir / "tiny2.jpg"
        tiny2_img.save(tiny2_path, "JPEG", quality=90)
        
    except ImportError:
        # Fallback: create minimal binary files
        tiny_path = tmp_dir / "tiny.jpg"
        tiny_path.write_bytes(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x10\x00\x10\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9')
        
        tiny2_path = tmp_dir / "tiny2.jpg"
        tiny2_path.write_bytes(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x20\x00\x20\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9')
    
    # Create tiny.txt
    txt_path = tmp_dir / "tiny.txt"
    txt_path.write_text("Test content for OCR", encoding="utf-8")
    
    return tmp_dir

@pytest.fixture
def tiny_image(tmp_media):
    """Return path to a tiny test image"""
    return str(tmp_media / "tiny.jpg")

@pytest.fixture
def tiny_image_path(tmp_media):
    """Return path to a tiny test image (alias for tiny_image)"""
    return str(tmp_media / "tiny.jpg")

@pytest.fixture
def tiny_image_32x32(tmp_media):
    """Return path to a 32x32 test image"""
    return str(tmp_media / "tiny2.jpg")

@pytest.fixture
def tiny_text_file(tmp_media):
    """Return path to a tiny text file"""
    return str(tmp_media / "tiny.txt")

@pytest.fixture
def no_network(monkeypatch):
    """Mock network calls to raise exceptions"""
    
    def mock_requests_get(*args, **kwargs):
        raise RuntimeError("Network calls disabled in tests")
    
    def mock_httpx_get(*args, **kwargs):
        raise RuntimeError("Network calls disabled in tests")
    
    def mock_subprocess_run(*args, **kwargs):
        # Allow local commands but block network-related ones
        cmd = args[0] if args else []
        if isinstance(cmd, list) and any(net_cmd in str(cmd).lower() for net_cmd in ['curl', 'wget', 'http', 'https']):
            raise RuntimeError("Network calls disabled in tests")
        return Mock(returncode=0, stdout=b"", stderr=b"")
    
            # Mock common network libraries
        try:
            monkeypatch.setattr("requests.get", mock_requests_get)
        except AttributeError:
            pass  # requests not available
        
        try:
            monkeypatch.setattr("httpx.get", mock_httpx_get)
        except AttributeError:
            pass  # httpx not available
        
        monkeypatch.setattr("subprocess.run", mock_subprocess_run)
        
        # Mock yt-dlp specifically
        monkeypatch.setattr("downloader.fetch_many.subprocess.run", mock_subprocess_run)
    
    return True

@pytest.fixture
def fake_logger():
    """Create a fake logger that accumulates messages for assertions"""
    class FakeLogger:
        def __init__(self):
            self.messages = []
            self.errors = []
            self.warnings = []
        
        def info(self, msg):
            self.messages.append(("INFO", msg))
        
        def warning(self, msg):
            self.warnings.append(msg)
            self.messages.append(("WARNING", msg))
        
        def error(self, msg):
            self.errors.append(msg)
            self.messages.append(("ERROR", msg))
        
        def debug(self, msg):
            self.messages.append(("DEBUG", msg))
        
        def get_messages(self, level=None):
            if level:
                return [msg for lvl, msg in self.messages if lvl == level]
            return [msg for _, msg in self.messages]
    
    return FakeLogger()

@pytest.fixture
def mock_easyocr(monkeypatch):
    """Mock EasyOCR to avoid heavy model loading"""
    mock_reader = Mock()
    mock_reader.readtext.return_value = [("test text", 0.95, (10, 10, 100, 30))]
    
    def mock_reader_init(*args, **kwargs):
        return mock_reader
    
    monkeypatch.setattr("easyocr.Reader", mock_reader_init)
    return mock_reader

@pytest.fixture
def mock_sentence_transformer(monkeypatch):
    """Mock SentenceTransformer to avoid heavy model loading"""
    mock_model = Mock()
    
    def mock_encode(images, **kwargs):
        # Return embeddings with correct shape based on number of images
        if isinstance(images, list):
            num_images = len(images)
        else:
            num_images = 1
        return np.random.randn(num_images, 512).astype(np.float32)
    
    mock_model.encode.side_effect = mock_encode
    
    def mock_model_init(*args, **kwargs):
        return mock_model
    
    # Mock both the class and the module
    monkeypatch.setattr("sentence_transformers.SentenceTransformer", mock_model_init)
    monkeypatch.setattr("analyzer.vision_clip.SentenceTransformer", mock_model_init)
    return mock_model

@pytest.fixture
def mock_torch_cuda(monkeypatch):
    """Mock torch.cuda to always return False for CPU-only tests"""
    monkeypatch.setattr("torch.cuda.is_available", lambda: False)
    return False

@pytest.fixture
def mock_pil_image(monkeypatch):
    """Mock PIL Image operations"""
    mock_img = Mock()
    mock_img.size = (512, 384)
    mock_img.resize.return_value = mock_img
    mock_img.save.return_value = None
    
    def mock_open(*args, **kwargs):
        return mock_img
    
    def mock_new(*args, **kwargs):
        return mock_img
    
    monkeypatch.setattr("PIL.Image.open", mock_open)
    monkeypatch.setattr("PIL.Image.new", mock_new)
    return mock_img

@pytest.fixture
def mock_cv2(monkeypatch):
    """Mock OpenCV operations"""
    mock_cap = Mock()
    mock_cap.read.return_value = (True, np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8))
    mock_cap.release.return_value = None
    
    def mock_videocapture(*args, **kwargs):
        return mock_cap
    
    def mock_cvtcolor(*args, **kwargs):
        return np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    monkeypatch.setattr("cv2.VideoCapture", mock_videocapture)
    monkeypatch.setattr("cv2.cvtColor", mock_cvtcolor)
    monkeypatch.setattr("cv2.COLOR_BGR2RGB", "COLOR_BGR2RGB")
    
    return mock_cap

@pytest.fixture
def mock_sqlite(monkeypatch):
    """Mock SQLite operations"""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_cursor.fetchall.return_value = [("https://example.com/video1",), ("https://example.com/video2",)]
    mock_conn.cursor.return_value = mock_cursor
    
    def mock_connect(*args, **kwargs):
        return mock_conn
    
    monkeypatch.setattr("sqlite3.connect", mock_connect)
    return mock_conn


def _make_frames(count: int, absolute: bool = True, prefix: str = "frame_", ext: str = ".jpg"):
    """Generate ordered frame Paths for testing"""
    base = pathlib.Path.cwd() if absolute else pathlib.Path(".")
    return [(base / f"{prefix}{i:06d}{ext}") for i in range(1, count+1)]


@pytest.fixture
def fake_frame_list(monkeypatch):
    """Patch Path.glob to return a controlled, ordered list of frames"""
    def _apply(count=10, pattern="*.jpg", absolute=True, max_frames=None):
        all_frames = _make_frames(count=count, absolute=absolute)
        call_count = 0
        
        def _glob(self, pat):
            nonlocal call_count
            call_count += 1
            
            # First call: return all frames (for initial processing)
            # Second call: return limited frames (for final result)
            if call_count == 1:
                return all_frames
            else:
                # Return limited frames for the final result
                limit = max_frames if max_frames is not None else len(all_frames)
                return all_frames[:limit]
        
        # Mock both the module's pathlib.Path.glob and the global pathlib.Path.glob
        monkeypatch.setattr("analyzer.frame_sampler.pathlib.Path.glob", _glob, raising=True)
        monkeypatch.setattr("pathlib.Path.glob", _glob, raising=True)
        
        return all_frames
    return _apply


def norm_names(paths):
    """Return just the file names (no dirs) from Path or str items"""
    out = []
    for p in paths:
        if isinstance(p, pathlib.Path):
            out.append(p.name)
        else:
            # assume string path
            out.append(pathlib.Path(p).name)
    return out


# ===== SPRINT 2: FAISS/Index + Multimodal Search Fixtures =====

def gen_embeds(n=8, d=16, seed=0, normalize=True):
    """Generate deterministic embeddings for testing"""
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d)).astype(np.float32)
    if normalize:
        X /= np.clip(np.linalg.norm(X, axis=1, keepdims=True), 1e-12, None)
    return X


class NumpyIndex:
    """Deterministic in-memory index with cosine similarity."""
    def __init__(self, dim: int):
        self.dim = dim
        self._vecs = []
        self._meta = []

    def add(self, vectors, meta):
        for v, m in zip(vectors, meta):
            arr = np.asarray(v, dtype=float).reshape(-1)
            if np.any(~np.isfinite(arr)):
                continue
            self._vecs.append(arr)
            self._meta.append(m)

    def search(self, vec, k):
        if not self._vecs or k <= 0 or vec is None:
            return []
        q = np.asarray(vec, dtype=float).reshape(-1)
        scores = []
        for i, v in enumerate(self._vecs):
            s = float(np.dot(q, v))
            scores.append((i, s))
        order = sorted(
            range(len(scores)),
            key=lambda i: (-scores[i][1], self._meta[i].get("original_idx", i))
        )
        out = []
        for idx in order[:k]:
            out.append({
                "id": self._meta[idx]["id"],
                "score": scores[idx][1],
                "original_idx": self._meta[idx].get("original_idx", idx),
            })
        return out


@pytest.fixture
def np_index_factory():
    """Factory for creating NumpyIndex instances"""
    def _make(dim):
        return NumpyIndex(dim)
    return _make

@pytest.fixture
def numpy_index_cls():
    """Return the NumpyIndex class for testing"""
    return NumpyIndex


@pytest.fixture
def small_dataset():
    """Small deterministic dataset for testing"""
    X = gen_embeds(n=10, d=16, seed=42)
    q = X[0].copy()
    return X, q
