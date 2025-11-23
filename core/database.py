#!/usr/bin/env python3
"""
ARKALIA ARIA - Gestionnaire de Base de Données
==============================================

Gestionnaire centralisé pour toutes les opérations de base de données.
Utilise le pattern Singleton pour éviter les connexions multiples.
"""

import logging
import sqlite3
import threading
from pathlib import Path

from .exceptions import DatabaseError

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Gestionnaire de base de données centralisé avec pattern Singleton.

    Fournit une interface unifiée pour toutes les opérations SQLite
    avec gestion automatique des connexions et des transactions.
    """

    _instances: dict[str, "DatabaseManager"] = {}
    _lock = threading.Lock()

    def __new__(cls, db_path: str = "aria_pain.db") -> "DatabaseManager":
        """Pattern Singleton par chemin pour éviter les connexions multiples."""
        resolved_path = str(Path(db_path).resolve())
        if resolved_path not in cls._instances:
            with cls._lock:
                if resolved_path not in cls._instances:
                    instance = super().__new__(cls)
                    instance._initialized = False
                    instance._connection = None
                    instance.db_path = Path(resolved_path)
                    cls._instances[resolved_path] = instance
        return cls._instances[resolved_path]

    def __init__(self, db_path: str = "aria_pain.db") -> None:
        """Initialise le gestionnaire de base de données."""
        if getattr(self, "_initialized", False):
            return

        self.db_path = Path(db_path).resolve()
        self._connection: sqlite3.Connection | None = None
        self._lock = threading.Lock()
        self._initialized = True

        # Créer le répertoire si nécessaire
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"🗄️ DatabaseManager initialisé: {self.db_path}")

    def get_connection(self) -> sqlite3.Connection:
        """
        Obtient une connexion à la base de données.

        Returns:
            Connexion SQLite active

        Raises:
            DatabaseError: Si la connexion échoue
        """
        if self._connection is None:
            with self._lock:
                if self._connection is None:
                    try:
                        self._connection = sqlite3.connect(
                            str(self.db_path), check_same_thread=False
                        )
                        self._connection.row_factory = sqlite3.Row
                        logger.debug(f"Connexion SQLite établie: {self.db_path}")
                    except sqlite3.Error as e:
                        logger.error(f"Erreur connexion SQLite: {e}")
                        raise DatabaseError(
                            f"Impossible de se connecter à la base: {e}"
                        ) from e

        return self._connection

    def execute_query(self, query: str, params: tuple = ()) -> list[sqlite3.Row]:
        """
        Exécute une requête SELECT et retourne les résultats.

        Args:
            query: Requête SQL SELECT
            params: Paramètres de la requête

        Returns:
            Liste des lignes de résultats

        Raises:
            DatabaseError: Si la requête échoue
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Erreur requête SELECT: {e}")
            raise DatabaseError(f"Erreur lors de l'exécution de la requête: {e}") from e

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """
        Exécute une requête INSERT/UPDATE/DELETE et retourne le nombre
        de lignes affectées.

        Args:
            query: Requête SQL INSERT/UPDATE/DELETE
            params: Paramètres de la requête

        Returns:
            Nombre de lignes affectées

        Raises:
            DatabaseError: Si la requête échoue
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Erreur requête UPDATE: {e}")
            raise DatabaseError(f"Erreur lors de l'exécution de la requête: {e}") from e

    def execute_many(self, query: str, params_list: list[tuple]) -> int:
        """
        Exécute une requête avec plusieurs jeux de paramètres.

        Args:
            query: Requête SQL
            params_list: Liste des paramètres

        Returns:
            Nombre total de lignes affectées

        Raises:
            DatabaseError: Si la requête échoue
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(f"Erreur requête executemany: {e}")
            raise DatabaseError(f"Erreur lors de l'exécution de la requête: {e}") from e

    def get_count(self, table: str, where_clause: str = "", params: tuple = ()) -> int:
        """
        Compte le nombre d'enregistrements dans une table.

        Args:
            table: Nom de la table
            where_clause: Clause WHERE (optionnelle)
            params: Paramètres de la clause WHERE

        Returns:
            Nombre d'enregistrements

        Raises:
            DatabaseError: Si la requête échoue
        """
        query = f"SELECT COUNT(*) FROM {table}"
        if where_clause:
            query += f" WHERE {where_clause}"

        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()[0]
        except sqlite3.Error as e:
            logger.error(f"Erreur requête COUNT: {e}")
            raise DatabaseError(f"Erreur lors du comptage: {e}") from e

    def table_exists(self, table_name: str) -> bool:
        """
        Vérifie si une table existe.

        Args:
            table_name: Nom de la table

        Returns:
            True si la table existe, False sinon
        """
        query = """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name=?
        """
        try:
            results = self.execute_query(query, (table_name,))
            return len(results) > 0
        except DatabaseError:
            return False

    def close(self) -> None:
        """Ferme la connexion à la base de données."""
        if self._connection:
            with self._lock:
                if self._connection:
                    self._connection.close()
                    self._connection = None
                    logger.info("Connexion SQLite fermée")

    def __del__(self):
        """Ferme automatiquement la connexion lors de la destruction."""
        self.close()
