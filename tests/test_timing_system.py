import pytest
import time
import logging
from unittest.mock import Mock
from utils.timing import timed_step, timed_ingest, format_duration


class TestTimingSystem:
    """Test per il sistema di timing dell'ingest"""
    
    def test_timed_step(self):
        """Test del context manager timed_step"""
        logger = Mock()
        
        with timed_step(logger, "Test Step"):
            time.sleep(0.1)  # Simula lavoro
        
        # Verifica che siano stati chiamati i log corretti
        assert logger.info.call_count == 2
        
        # Verifica il primo log (inizio)
        first_call = logger.info.call_args_list[0]
        assert "⏳ Iniziando: Test Step" in first_call[0][0]
        
        # Verifica il secondo log (fine con durata)
        second_call = logger.info.call_args_list[1]
        assert "✅ Completato: Test Step" in second_call[0][0]
        assert "durata:" in second_call[0][0]
        
        # Verifica che la durata sia un numero positivo
        duration_str = second_call[0][0].split("durata: ")[1].split("s")[0]
        duration = float(duration_str)
        assert duration >= 0.1  # Almeno 0.1s per il sleep
    
    def test_timed_ingest(self):
        """Test del context manager timed_ingest"""
        logger = Mock()
        
        with timed_ingest(logger):
            time.sleep(0.1)  # Simula lavoro
        
        # Verifica che siano stati chiamati i log corretti
        assert logger.info.call_count == 2
        
        # Verifica il primo log (avvio)
        first_call = logger.info.call_args_list[0]
        assert "🚀 Ingest avviato" in first_call[0][0]
        
        # Verifica il secondo log (completamento con tempo totale)
        second_call = logger.info.call_args_list[1]
        assert "🏁 Ingest completato in" in second_call[0][0]
        assert "s totali" in second_call[0][0]
        
        # Verifica che il tempo totale sia un numero positivo
        total_str = second_call[0][0].split("in ")[1].split("s totali")[0]
        total_duration = float(total_str)
        assert total_duration >= 0.1  # Almeno 0.1s per il sleep
    
    def test_nested_timing(self):
        """Test di timing annidato (ingest con step)"""
        logger = Mock()
        
        with timed_ingest(logger):
            with timed_step(logger, "Step 1"):
                time.sleep(0.05)
            with timed_step(logger, "Step 2"):
                time.sleep(0.05)
        
        # Verifica che siano stati chiamati tutti i log
        assert logger.info.call_count == 6  # 2 per ingest + 2 per step 1 + 2 per step 2
        
        # Verifica l'ordine dei log
        calls = [call[0][0] for call in logger.info.call_args_list]
        
        assert "🚀 Ingest avviato" in calls[0]
        assert "⏳ Iniziando: Step 1" in calls[1]
        assert "✅ Completato: Step 1" in calls[2]
        assert "⏳ Iniziando: Step 2" in calls[3]
        assert "✅ Completato: Step 2" in calls[4]
        assert "🏁 Ingest completato in" in calls[5]
    
    def test_format_duration(self):
        """Test della funzione format_duration"""
        # Test secondi
        assert format_duration(30.5) == "30.5s"
        assert format_duration(59.9) == "59.9s"
        
        # Test minuti
        assert format_duration(90) == "1m 30s"
        assert format_duration(125.7) == "2m 6s"
        
        # Test ore
        assert format_duration(3661) == "1h 1m"  # 1h 1m 1s
        assert format_duration(7320) == "2h 2m"  # 2h 2m 0s
    
    def test_timing_with_exception(self):
        """Test che il timing funzioni anche con eccezioni"""
        logger = Mock()
        
        try:
            with timed_step(logger, "Failing Step"):
                raise ValueError("Test exception")
        except ValueError:
            pass
        
        # Verifica che siano stati chiamati i log anche con eccezione
        assert logger.info.call_count == 2
        
        # Verifica che il log di completamento sia stato chiamato
        second_call = logger.info.call_args_list[1]
        assert "✅ Completato: Failing Step" in second_call[0][0]
        assert "durata:" in second_call[0][0]


if __name__ == "__main__":
    pytest.main([__file__])
