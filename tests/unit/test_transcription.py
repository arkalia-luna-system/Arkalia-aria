#!/usr/bin/env python3
"""
Tests pour le module de transcription audio
"""

import base64
from unittest.mock import patch

from audio_voice.transcription import AudioTranscriber, get_transcriber


class TestAudioTranscriber:
    """Tests pour AudioTranscriber"""

    def test_transcriber_status_without_whisper(self):
        """Test statut transcripteur sans Whisper installé"""
        with patch("audio_voice.transcription.WHISPER_AVAILABLE", False):
            transcriber = AudioTranscriber()
            status = transcriber.get_status()
            assert status["whisper_available"] is False
            assert status["status"] == "simulation"

    def test_transcribe_file_not_found(self):
        """Test transcription fichier inexistant"""
        transcriber = AudioTranscriber()
        # Le fichier n'existe pas, devrait lever FileNotFoundError
        try:
            transcriber.transcribe_file("nonexistent.wav")
            # Si on arrive ici, c'est en mode simulation et le fichier n'existe pas
            raise AssertionError("Devrait lever FileNotFoundError")
        except FileNotFoundError:
            # C'est le comportement attendu
            pass

    def test_transcribe_base64_simulation(self):
        """Test transcription base64 en mode simulation"""
        # Créer un audio fake encodé base64
        fake_audio = b"fake audio data"
        encoded_audio = base64.b64encode(fake_audio).decode("utf-8")

        transcriber = AudioTranscriber()
        result = transcriber.transcribe_base64(encoded_audio)

        assert "text" in result
        # En mode simulation, devrait avoir un message
        assert "simulation" in result.get("model_used", "") or "warning" in result

    def test_get_transcriber_singleton(self):
        """Test que get_transcriber retourne un singleton"""
        transcriber1 = get_transcriber()
        transcriber2 = get_transcriber()
        # Devrait être la même instance
        assert transcriber1 is transcriber2
