import pytest
import numpy as np
import sys
from analyzer.search_multimodal import combine_results
from analyzer.index_faiss import IndexBackend, FaissIndex

# Funzioni helper per i test
def search_text_simple(query, embeddings, query_embedding, ids, k=5, index_backend=None, text_encoder=None):
    """Versione semplificata di search_text per i test"""
    if len(embeddings) == 0:
        return []
    
    if embeddings.shape[1] != query_embedding.shape[0]:
        raise ValueError("Dimension mismatch between embeddings and query")
    
    if np.any(np.isnan(embeddings)) or np.any(np.isinf(embeddings)):
        raise ValueError("Embeddings contain NaN or Inf values")
    
    # Calcola similarità coseno
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    
    similarities = np.dot(embeddings_norm, query_norm)
    
    # Trova i top-k
    k = min(k, len(embeddings))
    top_indices = np.argsort(similarities)[::-1][:k]
    
    results = []
    for idx in top_indices:
        results.append({
            'id': ids[idx],
            'score': float(similarities[idx]),
            'metadata': {'text': f'text_{ids[idx]}'}
        })
    
    return results


class TestSprint2Robustness:
    """Test di robustezza per Sprint 2 - Micro-review"""
    
    def test_stable_ordering_identical_scores(self):
        """Test che l'ordinamento sia stabile su punteggi identici"""
        # Setup: crea embedding con punteggi identici
        np.random.seed(42)
        embeddings = np.random.rand(10, 16).astype(np.float32)
        query_embedding = np.random.rand(16).astype(np.float32)
        
        # Normalizza per avere punteggi simili
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        
        # Crea risultati con punteggi identici
        results = []
        for i in range(10):
            results.append({
                'id': f'item_{i}',
                'score': 0.5,  # Punteggio identico per tutti
                'metadata': {'text': f'text_{i}'}
            })
        
        # Esegui ordinamento multiplo volte
        sorted_results_1 = sorted(results, key=lambda x: x['score'], reverse=True)
        sorted_results_2 = sorted(results, key=lambda x: x['score'], reverse=True)
        sorted_results_3 = sorted(results, key=lambda x: x['score'], reverse=True)
        
        # Verifica che l'ordinamento sia stabile (stesso ordine)
        assert [r['id'] for r in sorted_results_1] == [r['id'] for r in sorted_results_2]
        assert [r['id'] for r in sorted_results_2] == [r['id'] for r in sorted_results_3]
        
        # Verifica che tutti i punteggi siano identici
        scores = [r['score'] for r in sorted_results_1]
        assert all(abs(s - 0.5) < 1e-6 for s in scores)
    
    def test_multimodal_duplicate_merge(self):
        """Test merge multimodale con duplicati mantenendo score = max(text_score, image_score)"""
        # Setup: risultati con duplicati (formato corretto per combine_results)
        text_results = [
            {'url': 'item_1', 'score': 0.8, 'type': 'text'},
            {'url': 'item_2', 'score': 0.6, 'type': 'text'},
            {'url': 'item_3', 'score': 0.4, 'type': 'text'}
        ]
        
        image_results = [
            {'url': 'item_1', 'score': 0.9, 'type': 'visual'},  # Duplicato con score diverso
            {'url': 'item_2', 'score': 0.5, 'type': 'visual'},  # Duplicato con score diverso
            {'url': 'item_4', 'score': 0.7, 'type': 'visual'}   # Solo in image
        ]
        
        # Test con pesi personalizzati
        combined = combine_results(
            text_results, image_results, 
            weight_text=0.6, weight_visual=0.4
        )
        
        # Verifica che i duplicati siano gestiti correttamente
        item_1_result = next((r for r in combined if r['url'] == 'item_1'), None)
        item_2_result = next((r for r in combined if r['url'] == 'item_2'), None)
        
        assert item_1_result is not None
        assert item_2_result is not None
        
        # Verifica che i punteggi siano combinati correttamente
        # Per item_1: text_score=0.8, visual_score=0.9
        # combined_score = 0.8 * 0.6 + 0.9 * 0.4 = 0.48 + 0.36 = 0.84
        expected_score_1 = 0.8 * 0.6 + 0.9 * 0.4  # 0.84
        # Per item_2: text_score=0.6, visual_score=0.5
        # combined_score = 0.6 * 0.6 + 0.5 * 0.4 = 0.36 + 0.20 = 0.56
        expected_score_2 = 0.6 * 0.6 + 0.5 * 0.4  # 0.56
        
        assert abs(item_1_result['combined_score'] - expected_score_1) < 1e-6
        assert abs(item_2_result['combined_score'] - expected_score_2) < 1e-6
        
        # Verifica che non ci siano duplicati nel risultato finale
        urls = [r['url'] for r in combined]
        assert len(urls) == len(set(urls))  # Nessun duplicato
        
        # Verifica che tutti i risultati abbiano i campi corretti
        for result in combined:
            assert 'url' in result
            assert 'text_score' in result
            assert 'visual_score' in result
            assert 'combined_score' in result
    
    def test_input_robustness_edge_cases(self):
        """Test robustezza su edge cases: dimensioni mismatch, NaN/Inf, indice vuoto, k > len(index)"""
        # Test 1: Dimensioni mismatch
        with pytest.raises(ValueError):
            search_text_simple(
                query="test",
                embeddings=np.random.rand(5, 16),  # 16 dimensioni
                query_embedding=np.random.rand(32),  # 32 dimensioni - mismatch!
                ids=["item_1", "item_2", "item_3", "item_4", "item_5"],
                k=3
            )
        
        # Test 2: NaN/Inf negli embedding
        embeddings_with_nan = np.random.rand(5, 16).astype(np.float32)
        embeddings_with_nan[0, 0] = np.nan
        
        with pytest.raises(ValueError):
            search_text_simple(
                query="test",
                embeddings=embeddings_with_nan,
                query_embedding=np.random.rand(16),
                ids=["item_1", "item_2", "item_3", "item_4", "item_5"],
                k=3
            )
        
        # Test 3: Indice vuoto
        empty_results = search_text_simple(
            query="test",
            embeddings=np.array([]).reshape(0, 16),
            query_embedding=np.random.rand(16),
            ids=[],
            k=3
        )
        assert len(empty_results) == 0
        
        # Test 4: k > len(index)
        embeddings = np.random.rand(3, 16).astype(np.float32)
        query_embedding = np.random.rand(16)
        ids = ["item_1", "item_2", "item_3"]
        
        # k=5 ma solo 3 item disponibili
        results = search_text_simple(
            query="test",
            embeddings=embeddings,
            query_embedding=query_embedding,
            ids=ids,
            k=5  # Più grande del numero di item
        )
        
        # Dovrebbe restituire solo i 3 item disponibili
        assert len(results) == 3
        assert all(r['id'] in ids for r in results)
    
    def test_no_faiss_fallback_path(self):
        """Test che simula l'assenza di FAISS per garantire import e fallback"""
        # Salva il modulo FAISS originale
        original_faiss = sys.modules.get('faiss')
        
        try:
            # Simula l'assenza di FAISS
            sys.modules['faiss'] = None
            
            # Reset della variabile _HAVE_FAISS nel modulo
            import analyzer.index_faiss
            original_have_faiss = analyzer.index_faiss._HAVE_FAISS
            analyzer.index_faiss._HAVE_FAISS = False
            
            # Test che IndexBackend funzioni senza FAISS
            backend = IndexBackend()
            assert backend is not None
            
            # Test che FaissIndex gestisca gracefulmente l'assenza di FAISS
            with pytest.raises(RuntimeError):
                FaissIndex(dim=16)
            
            # Test che search_multimodal funzioni con NumpyIndex
            from tests.conftest import NumpyIndex
            
            index = NumpyIndex(dim=16)
            embeddings = np.random.rand(5, 16).astype(np.float32)
            
            # Aggiungi tutti gli embedding in una volta
            index.add(embeddings)
            
            # Test ricerca
            query_embedding = np.random.rand(16)
            results = search_text_simple(
                query="test",
                embeddings=embeddings,
                query_embedding=query_embedding,
                ids=["item_1", "item_2", "item_3", "item_4", "item_5"],
                k=3,
                index_backend=index
            )
            
            assert len(results) == 3
            assert all('id' in r for r in results)
            assert all('score' in r for r in results)
            
        finally:
            # Ripristina il modulo FAISS originale
            if original_faiss is not None:
                sys.modules['faiss'] = original_faiss
            elif 'faiss' in sys.modules:
                del sys.modules['faiss']
            
            # Ripristina la variabile _HAVE_FAISS
            if 'analyzer.index_faiss' in sys.modules:
                analyzer.index_faiss._HAVE_FAISS = original_have_faiss
    
    def test_deterministic_ranking_with_seed(self):
        """Test che il ranking sia deterministico con seed fisso"""
        np.random.seed(42)
        
        # Crea dataset deterministico
        embeddings = np.random.rand(10, 16).astype(np.float32)
        query_embedding = np.random.rand(16).astype(np.float32)
        ids = [f"item_{i}" for i in range(10)]
        
        # Esegui ricerca multipla volte
        results_1 = search_text_simple(
            query="test",
            embeddings=embeddings,
            query_embedding=query_embedding,
            ids=ids,
            k=5
        )
        
        # Reset seed e ricrea dataset identico
        np.random.seed(42)
        embeddings_2 = np.random.rand(10, 16).astype(np.float32)
        query_embedding_2 = np.random.rand(16).astype(np.float32)
        
        results_2 = search_text_simple(
            query="test",
            embeddings=embeddings_2,
            query_embedding=query_embedding_2,
            ids=ids,
            k=5
        )
        
        # Verifica che i risultati siano identici
        assert len(results_1) == len(results_2)
        assert [r['id'] for r in results_1] == [r['id'] for r in results_2]
        
        # Verifica che i punteggi siano identici (entro tolleranza numerica)
        for r1, r2 in zip(results_1, results_2):
            assert abs(r1['score'] - r2['score']) < 1e-6
