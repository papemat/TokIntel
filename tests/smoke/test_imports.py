import pytest


class TestImports:
    """Smoke tests for module imports"""
    
    def test_analyzer_imports(self):
        """Test that analyzer modules can be imported"""
        import analyzer.ocr_extractor
        import analyzer.frame_sampler
        import analyzer.vision_clip
        
        # Verify key functions exist
        assert hasattr(analyzer.ocr_extractor, 'run_ocr_on_frames')
        assert hasattr(analyzer.frame_sampler, 'sample_frames_ffmpeg')
        assert hasattr(analyzer.vision_clip, 'device_from_pref')
        assert hasattr(analyzer.vision_clip, 'image_paths_to_embeddings')
        assert hasattr(analyzer.vision_clip, 'pool_video_embedding')
    
    def test_downloader_imports(self):
        """Test that downloader modules can be imported"""
        import downloader.fetch_many
        
        # Verify key functions exist
        assert hasattr(downloader.fetch_many, 'fetch_one')
        assert hasattr(downloader.fetch_many, 'fetch_missing')
        assert hasattr(downloader.fetch_many, 'fetch_missing_with_callbacks')
        assert hasattr(downloader.fetch_many, 'already_downloaded')
        assert hasattr(downloader.fetch_many, 'extract_thumbnail')
        assert hasattr(downloader.fetch_many, 'make_thumb_from_file')
    
    def test_optional_analyzer_imports(self):
        """Test optional analyzer modules (may not exist)"""
        try:
            import analyzer.build_visual_index
            assert True  # Module exists
        except ImportError:
            pytest.skip("analyzer.build_visual_index not available")
        
        try:
            import analyzer.index_faiss
            assert True  # Module exists
        except ImportError:
            pytest.skip("analyzer.index_faiss not available")
        
        try:
            import analyzer.search_multimodal
            assert True  # Module exists
        except ImportError:
            pytest.skip("analyzer.search_multimodal not available")
        
        try:
            import analyzer.run_multimodal
            assert True  # Module exists
        except ImportError:
            pytest.skip("analyzer.run_multimodal not available")
    
    def test_optional_downloader_imports(self):
        """Test optional downloader modules (may not exist)"""
        try:
            import downloader.fetch_video
            assert True  # Module exists
        except ImportError:
            pytest.skip("downloader.fetch_video not available")
    
    def test_collector_imports(self):
        """Test collector modules (may not exist)"""
        try:
            import collector.collect_tiktok_collection
            assert True  # Module exists
        except ImportError:
            pytest.skip("collector.collect_tiktok_collection not available")
    
    def test_dash_imports(self):
        """Test dashboard modules (may not exist)"""
        try:
            import dash.app
            assert True  # Module exists
        except ImportError:
            pytest.skip("dash.app not available")
        
        try:
            import dash.perf_dashboard
            assert True  # Module exists
        except ImportError:
            pytest.skip("dash.perf_dashboard not available")
    
    def test_config_imports(self):
        """Test configuration loading"""
        try:
            import yaml
            import pathlib
            
            config_path = pathlib.Path("config/settings.yaml")
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                assert isinstance(config, dict)
            else:
                pytest.skip("config/settings.yaml not found")
        except ImportError:
            pytest.skip("yaml not available")
    
    def test_third_party_imports(self):
        """Test that key third-party libraries can be imported"""
        try:
            import numpy as np
            assert hasattr(np, 'array')
        except ImportError:
            pytest.skip("numpy not available")
        
        try:
            import pandas as pd
            assert hasattr(pd, 'DataFrame')
        except ImportError:
            pytest.skip("pandas not available")
        
        try:
            from PIL import Image
            assert hasattr(Image, 'open')
        except ImportError:
            pytest.skip("PIL not available")
        
        try:
            import easyocr
            assert hasattr(easyocr, 'Reader')
        except ImportError:
            pytest.skip("easyocr not available")
        
        try:
            from sentence_transformers import SentenceTransformer
            assert hasattr(SentenceTransformer, '__init__')
        except ImportError:
            pytest.skip("sentence_transformers not available")
        
        try:
            import torch
            assert hasattr(torch, 'cuda')
        except ImportError:
            pytest.skip("torch not available")
    
    def test_standard_library_imports(self):
        """Test that standard library modules work"""
        import pathlib
        import json
        import sqlite3
        import subprocess
        import tempfile
        import shutil
        
        # Verify basic functionality
        assert hasattr(pathlib.Path, 'exists')
        assert hasattr(json, 'dumps')
        assert hasattr(sqlite3, 'connect')
        assert hasattr(subprocess, 'run')
        assert hasattr(tempfile, 'mkdtemp')
        assert hasattr(shutil, 'rmtree')
    
    def test_package_structure(self):
        """Test that package structure is correct"""
        import pathlib
        
        # Check that main directories exist
        assert pathlib.Path("analyzer").exists()
        assert pathlib.Path("downloader").exists()
        assert pathlib.Path("tests").exists()
        
        # Check that __init__.py files exist
        assert pathlib.Path("analyzer/__init__.py").exists()
        assert pathlib.Path("downloader/__init__.py").exists()
        assert pathlib.Path("tests/__init__.py").exists()
    
    def test_test_structure(self):
        """Test that test structure is correct"""
        import pathlib
        
        # Check that test directories exist
        assert pathlib.Path("tests/unit").exists()
        assert pathlib.Path("tests/smoke").exists()
        assert pathlib.Path("tests/data").exists()
        
        # Check that conftest.py exists
        assert pathlib.Path("tests/conftest.py").exists()
    
    def test_requirements_files(self):
        """Test that requirements files exist"""
        import pathlib
        
        # Check that requirements files exist
        assert pathlib.Path("requirements.txt").exists()
        assert pathlib.Path("pyproject.toml").exists()
    
    def test_makefile_exists(self):
        """Test that Makefile exists"""
        import pathlib
        
        assert pathlib.Path("Makefile").exists()
    
    def test_readme_exists(self):
        """Test that README exists"""
        import pathlib
        
        assert pathlib.Path("README.md").exists()
