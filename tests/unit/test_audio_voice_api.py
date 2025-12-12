"""
Tests pour l'API Audio/Voice
"""

import base64
from unittest.mock import patch

from fastapi.testclient import TestClient

from audio_voice.api import TTSRequest
from main import app

client = TestClient(app)


class TestAudioVoiceAPI:
    """Tests pour l'API Audio/Voice"""

    def test_audio_status(self):
        """Test GET /api/audio/status"""
        response = client.get("/api/audio/status")
        assert response.status_code == 200
        data = response.json()
        # BaseAPI enregistre automatiquement /status qui écrase celui de audio_voice/api.py
        assert "status" in data
        assert "timestamp" in data
        assert "api_name" in data

    def test_synthesize_speech_success(self):
        """Test POST /api/audio/tts avec texte valide"""
        request_data = {"text": "Bonjour, ceci est un test", "voice": "amelie"}
        response = client.post("/api/audio/tts", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["voice"] == "amelie"
        assert data["text"] == "Bonjour, ceci est un test"
        assert "message" in data

    def test_synthesize_speech_default_voice(self):
        """Test POST /api/audio/tts sans spécifier de voix"""
        request_data = {"text": "Test sans voix spécifiée"}
        response = client.post("/api/audio/tts", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["voice"] == "amelie"  # Voix par défaut

    def test_synthesize_speech_empty_text(self):
        """Test POST /api/audio/tts avec texte vide"""
        request_data = {"text": "   ", "voice": "amelie"}
        response = client.post("/api/audio/tts", json=request_data)
        assert response.status_code == 400

    def test_synthesize_speech_missing_text(self):
        """Test POST /api/audio/tts sans texte"""
        request_data = {"voice": "amelie"}
        response = client.post("/api/audio/tts", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_synthesize_speech_text_too_long(self):
        """Test POST /api/audio/tts avec texte trop long"""
        long_text = "a" * 2001  # Plus de 2000 caractères
        request_data = {"text": long_text, "voice": "amelie"}
        response = client.post("/api/audio/tts", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_save_audio_note_success(self):
        """Test POST /api/audio/note avec audio valide"""
        # Créer un audio factice encodé en base64
        fake_audio = b"fake audio data for testing"
        encoded_audio = base64.b64encode(fake_audio).decode("utf-8")

        request_data = {
            "filename": "test_audio.wav",
            "content_base64": encoded_audio,
        }

        with patch("audio_voice.api.Path.mkdir"):
            with patch("builtins.open", create=True):
                response = client.post("/api/audio/note", json=request_data)

                assert response.status_code == 200
                data = response.json()
                assert data["status"] == "saved"
                assert "file_path" in data
                assert data["size_bytes"] == len(fake_audio)
                assert "timestamp" in data

    def test_save_audio_note_auto_filename(self):
        """Test POST /api/audio/note sans nom de fichier (génération automatique)"""
        fake_audio = b"fake audio data"
        encoded_audio = base64.b64encode(fake_audio).decode("utf-8")

        request_data = {"content_base64": encoded_audio}

        with patch("audio_voice.api.Path.mkdir"):
            with patch("builtins.open", create=True):
                response = client.post("/api/audio/note", json=request_data)

                assert response.status_code == 200
                data = response.json()
                assert "file_path" in data
                assert "audio_note_" in data["file_path"]  # Nom généré automatiquement

    def test_save_audio_note_invalid_base64(self):
        """Test POST /api/audio/note avec base64 invalide"""
        request_data = {
            "filename": "test.wav",
            "content_base64": "invalid base64!!!",
        }

        response = client.post("/api/audio/note", json=request_data)
        assert response.status_code == 400
        assert "base64" in response.json()["detail"].lower()

    def test_save_audio_note_missing_content(self):
        """Test POST /api/audio/note sans contenu"""
        request_data = {"filename": "test.wav"}
        response = client.post("/api/audio/note", json=request_data)
        assert response.status_code == 422  # Validation error

    def test_tts_request_model_validation(self):
        """Test validation du modèle TTSRequest"""
        # Texte valide
        valid_request = TTSRequest(text="Test", voice="amelie")
        assert valid_request.text == "Test"
        assert valid_request.voice == "amelie"

        # Texte valide sans voix
        valid_request_no_voice = TTSRequest(text="Test")
        assert valid_request_no_voice.text == "Test"
        assert valid_request_no_voice.voice == "amelie"  # Par défaut

    def test_audio_note_request_model_validation(self):
        """Test validation du modèle AudioNoteRequest"""
        from audio_voice.api import AudioNoteRequest

        fake_audio = b"test audio"
        encoded_audio = base64.b64encode(fake_audio).decode("utf-8")

        # Avec filename
        request_with_filename = AudioNoteRequest(
            filename="test.wav", content_base64=encoded_audio
        )
        assert request_with_filename.filename == "test.wav"
        assert request_with_filename.content_base64 == encoded_audio

        # Sans filename
        request_no_filename = AudioNoteRequest(content_base64=encoded_audio)
        assert request_no_filename.filename is None
        assert request_no_filename.content_base64 == encoded_audio
