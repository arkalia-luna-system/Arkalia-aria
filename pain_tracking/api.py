"""
Pain Tracking API - Module de suivi de la douleur ARIA
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, TypedDict

from fastapi import HTTPException, Query
from pydantic import BaseModel, Field

from core import BaseAPI

# Créer l'API de base
api = BaseAPI(
    prefix="",  # Pas de préfixe ici, il sera ajouté dans main.py
    tags=["Pain Tracking"],
    description="API de suivi de la douleur ARIA",
)

router = api.get_router()
logger = api.logger
db = api.db


def _init_tables() -> None:
    """Initialise les tables de la base de données."""
    try:
        # Créer la table pain_entries
        db.execute_update("""
            CREATE TABLE IF NOT EXISTS pain_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                intensity INTEGER NOT NULL CHECK (intensity >= 0 AND intensity <= 10),
                physical_trigger TEXT,
                mental_trigger TEXT,
                activity TEXT,
                location TEXT,
                action_taken TEXT,
                effectiveness INTEGER CHECK (effectiveness >= 0 AND effectiveness <= 10),
                notes TEXT,
                who_present TEXT,
                interactions TEXT,
                emotions TEXT,
                thoughts TEXT,
                physical_symptoms TEXT,
                created_at TEXT NOT NULL DEFAULT (DATETIME('now'))
            )
            """)

        # Migration: ajouter les nouveaux champs seulement si la table existe déjà SANS ces colonnes
        # Vérifier si les colonnes existent avant de les ajouter
        try:
            # Vérifier si la table existe
            table_exists = db.table_exists("pain_entries")
            if table_exists:
                existing_columns = [
                    row[1]
                    for row in db.execute_query("PRAGMA table_info(pain_entries)")
                ]
                new_columns = {
                    "who_present": "TEXT",
                    "interactions": "TEXT",
                    "emotions": "TEXT",
                    "thoughts": "TEXT",
                    "physical_symptoms": "TEXT",
                }
                for col_name, col_type in new_columns.items():
                    if col_name not in existing_columns:
                        try:
                            db.execute_update(
                                f"ALTER TABLE pain_entries ADD COLUMN {col_name} {col_type}"
                            )
                            logger.debug(f"✅ Colonne {col_name} ajoutée")
                        except Exception as e:
                            error_msg = str(e).lower()
                            # Ignorer seulement les erreurs de colonne déjà existante
                            if (
                                "duplicate column" in error_msg
                                or "already exists" in error_msg
                            ):
                                logger.debug(f"Colonne {col_name} existe déjà, ignoré")
                            else:
                                logger.warning(
                                    f"Erreur lors de l'ajout de la colonne {col_name}: {e}"
                                )
        except Exception as e:
            # Si la table n'existe pas encore, c'est OK (sera créée par CREATE TABLE IF NOT EXISTS)
            logger.debug(f"Vérification colonnes: {e}")

        # Créer les index pour optimiser les requêtes
        try:
            db.execute_update(
                "CREATE INDEX IF NOT EXISTS idx_pain_entries_timestamp ON pain_entries(timestamp)"
            )
        except Exception as e:
            # Index peut déjà exister, ignorer
            api.logger.debug(f"Index idx_pain_entries_timestamp peut déjà exister: {e}")
        try:
            db.execute_update(
                "CREATE INDEX IF NOT EXISTS idx_pain_entries_intensity ON pain_entries(intensity)"
            )
        except Exception as e:
            # Index peut déjà exister, ignorer
            api.logger.debug(f"Index idx_pain_entries_intensity peut déjà exister: {e}")
        try:
            db.execute_update(
                "CREATE INDEX IF NOT EXISTS idx_pain_entries_location ON pain_entries(location)"
            )
        except Exception as e:
            # Index peut déjà exister, ignorer
            api.logger.debug(f"Index idx_pain_entries_location peut déjà exister: {e}")
        try:
            db.execute_update(
                "CREATE INDEX IF NOT EXISTS idx_pain_entries_timestamp_intensity ON pain_entries(timestamp, intensity)"
            )
        except Exception as e:
            # Index peut déjà exister, ignorer
            api.logger.debug(
                f"Index idx_pain_entries_timestamp_intensity peut déjà exister: {e}"
            )
        logger.info("✅ Tables pain_entries initialisées avec index")
    except Exception as e:
        logger.error(f"❌ Erreur initialisation tables: {e}")
        raise


def _fetch_all_entries() -> list[dict]:
    """Récupère toutes les entrées triées par date (récentes d'abord)."""
    _init_tables()
    try:
        # Limiter à 10000 entrées max pour éviter surcharge mémoire
        rows = db.execute_query(
            "SELECT * FROM pain_entries ORDER BY timestamp DESC, id DESC LIMIT 10000"
        )
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"❌ Erreur récupération entrées: {e}")
        raise


class ActionEff(TypedDict):
    action: str
    avg_effectiveness: float
    samples: int


def _compute_basic_stats(rows: list[dict]) -> dict[str, Any]:
    """Calcule des statistiques simples utiles pour rapport et suggestions."""
    if not rows:
        return {
            "entries_count": 0,
            "avg_intensity": 0.0,
            "top_triggers": [],
            "best_actions": [],
            "time_peaks": [],
        }

    import statistics
    from collections import Counter, defaultdict

    intensities: list[int] = []
    trigger_counter: Counter[str] = Counter()
    action_effectiveness: dict[str, list[int]] = defaultdict(list)
    hour_counter: Counter[str] = Counter()

    for r in rows:
        intensities.append(int(r["intensity"]))
        if r["physical_trigger"]:
            trigger_counter[r["physical_trigger"]] += 1
        if r["action_taken"] and r["effectiveness"] is not None:
            action_effectiveness[r["action_taken"]].append(int(r["effectiveness"]))
        # pics horaires
        ts = r["timestamp"]
        try:
            tpart = ts.split("T")[1] if "T" in ts else "00:00:00"
            hour = tpart.split(":")[0]
        except Exception:
            hour = "00"
        hour_counter[hour] += 1

    avg_intensity = round(statistics.mean(intensities), 2) if intensities else 0.0

    top_triggers = [
        {"trigger": trig, "count": cnt} for trig, cnt in trigger_counter.most_common(5)
    ]

    best_actions: list[ActionEff] = []
    for action, effs in action_effectiveness.items():
        if effs:
            best_actions.append(
                ActionEff(
                    action=action,
                    avg_effectiveness=round(statistics.mean(effs), 2),
                    samples=len(effs),
                )
            )
    best_actions.sort(key=lambda x: x["avg_effectiveness"], reverse=True)
    best_actions = best_actions[:5]

    time_peaks = [{"hour": h, "count": c} for h, c in hour_counter.most_common(5)]

    return {
        "entries_count": len(rows),
        "avg_intensity": avg_intensity,
        "top_triggers": top_triggers,
        "best_actions": best_actions,
        "time_peaks": time_peaks,
    }


# ==== Schémas ====

# Types de validation (définitions supprimées - utilisation directe de Field)


class PainEntryIn(BaseModel):
    intensity: int = Field(..., ge=0, le=10)
    physical_trigger: str | None = Field(default=None, min_length=1, max_length=128)
    mental_trigger: str | None = Field(default=None, min_length=1, max_length=128)
    activity: str | None = Field(default=None, min_length=1, max_length=128)
    location: str | None = Field(default=None, min_length=1, max_length=128)
    action_taken: str | None = Field(default=None, min_length=1, max_length=128)
    effectiveness: int | None = Field(default=None, ge=0, le=10)
    notes: str | None = Field(default=None, max_length=2000)
    who_present: str | None = Field(
        default=None,
        max_length=500,
        description="Personnes présentes lors de l'épisode",
    )
    interactions: str | None = Field(
        default=None,
        max_length=1000,
        description="Qui dit/fait quoi - interactions observées",
    )
    emotions: str | None = Field(
        default=None,
        max_length=1000,
        description="Ce que je ressens - émotions et sensations",
    )
    thoughts: str | None = Field(
        default=None,
        max_length=2000,
        description="Ce que je pense - pensées et réflexions",
    )
    physical_symptoms: str | None = Field(
        default=None, max_length=1000, description="Symptômes physiques détaillés"
    )
    timestamp: str | None = None  # ISO format


class PainEntryOut(PainEntryIn):
    id: int
    timestamp: str
    created_at: str


class QuickEntry(BaseModel):
    """Saisie ultra-rapide - 3 questions seulement"""

    intensity: int = Field(..., ge=0, le=10)
    physical_trigger: str = Field(
        ..., min_length=1, max_length=128
    )  # Déclencheur en un mot
    action_taken: str = Field(..., min_length=1, max_length=128)  # Action immédiate


# ==== Endpoints ====


@router.get("/status")
async def pain_tracking_status() -> dict:
    """Statut du module pain tracking"""
    return {
        "module": "pain_tracking",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "quick_entry",
            "detailed_entry",
            "history",
            "export_csv",
            "export_psy_html",
            "suggestions",
        ],
    }


@router.post("/quick-entry", response_model=PainEntryOut)
async def create_quick_entry(entry: QuickEntry) -> PainEntryOut:
    """Saisie ultra-rapide - 3 questions seulement"""
    # Invalider le cache après création d'entrée
    api.cache.invalidate_pattern("pain_entries_")
    api.cache.invalidate_pattern("pain_suggestions_")
    _init_tables()
    ts = datetime.now().isoformat()

    try:
        # Insérer l'entrée
        db.execute_update(
            """
            INSERT INTO pain_entries (
                timestamp, intensity, physical_trigger, action_taken
            ) VALUES (?, ?, ?, ?)
            """,
            (ts, int(entry.intensity), entry.physical_trigger, entry.action_taken),
        )

        # Récupérer l'entrée créée
        rows = db.execute_query("SELECT * FROM pain_entries ORDER BY id DESC LIMIT 1")
        if not rows:
            raise HTTPException(
                status_code=500, detail="Erreur lors de la création de l'entrée"
            )

        logger.info(f"✅ Entrée rapide créée: intensité {entry.intensity}")
        return PainEntryOut(**dict(rows[0]))
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"❌ Erreur validation données: {e}")
        raise HTTPException(
            status_code=400, detail=f"Données invalides: {str(e)}"
        ) from e
    except Exception as e:
        logger.error(f"❌ Erreur création entrée rapide: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}") from e


@router.post("/entry", response_model=PainEntryOut)
async def create_pain_entry(entry: PainEntryIn) -> PainEntryOut:
    """Création d'une entrée détaillée"""
    # Invalider le cache après création d'entrée
    api.cache.invalidate_pattern("pain_entries_")
    api.cache.invalidate_pattern("pain_suggestions_")
    _init_tables()
    ts = entry.timestamp or datetime.now().isoformat()

    try:
        # Insérer l'entrée détaillée
        db.execute_update(
            """
            INSERT INTO pain_entries (
                timestamp, intensity, physical_trigger, mental_trigger, activity,
                location, action_taken, effectiveness, notes,
                who_present, interactions, emotions, thoughts, physical_symptoms
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ts,
                int(entry.intensity),
                entry.physical_trigger,
                entry.mental_trigger,
                entry.activity,
                entry.location,
                entry.action_taken,
                int(entry.effectiveness) if entry.effectiveness is not None else None,
                entry.notes,
                entry.who_present,
                entry.interactions,
                entry.emotions,
                entry.thoughts,
                entry.physical_symptoms,
            ),
        )

        # Récupérer l'entrée créée
        rows = db.execute_query("SELECT * FROM pain_entries ORDER BY id DESC LIMIT 1")
        if not rows:
            raise HTTPException(
                status_code=500, detail="Erreur lors de la création de l'entrée"
            )

        logger.info(f"✅ Entrée détaillée créée: intensité {entry.intensity}")
        return PainEntryOut(**dict(rows[0]))
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"❌ Erreur validation données: {e}")
        raise HTTPException(
            status_code=400, detail=f"Données invalides: {str(e)}"
        ) from e
    except Exception as e:
        logger.error(f"❌ Erreur création entrée détaillée: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}") from e


@router.get("/entries", response_model=dict)
async def list_pain_entries(
    limit: int = Query(50, ge=1, le=200, description="Nombre d'entrées à retourner"),
    offset: int = Query(0, ge=0, description="Nombre d'entrées à sauter"),
) -> dict[str, Any]:
    """
    Liste les entrées de douleur avec pagination.

    Args:
        limit: Nombre d'entrées à retourner (défaut: 50, max: 200)
        offset: Nombre d'entrées à sauter (défaut: 0)
    """
    _init_tables()
    try:
        # Limiter le nombre max pour éviter surcharge
        limit = min(limit, 200)
        offset = max(offset, 0)

        # Récupérer les entrées avec pagination
        rows = db.execute_query(
            "SELECT * FROM pain_entries ORDER BY timestamp DESC, id DESC LIMIT ? OFFSET ?",
            (limit, offset),
        )

        # Compter le total
        total_rows = db.execute_query("SELECT COUNT(*) as count FROM pain_entries")
        total = total_rows[0]["count"] if total_rows else 0

        logger.info(f"📋 {len(rows)} entrées récupérées (total: {total})")
        return {
            "entries": [PainEntryOut(**dict(row)) for row in rows],
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total,
        }
    except Exception as e:
        logger.error(f"❌ Erreur récupération entrées: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") from e


@router.get("/entries/recent", response_model=list[PainEntryOut])
async def list_recent(limit: int = 20) -> list[PainEntryOut]:
    """Liste les entrées récentes"""
    _init_tables()
    try:
        # Vérifier le cache (clé basée sur limit)
        cache_key = f"pain_entries_recent_{limit}"
        cached_result = api.cache.get(cache_key)
        if cached_result is not None:
            logger.debug(f"📦 Entrées récentes depuis cache (limit={limit})")
            return cached_result

        rows = db.execute_query(
            "SELECT * FROM pain_entries ORDER BY timestamp DESC, id DESC LIMIT ?",
            (limit,),
        )
        result = [PainEntryOut(**dict(row)) for row in rows]
        logger.info(f"📋 {len(rows)} entrées récentes récupérées")

        # Mettre en cache (TTL 2 minutes car données récentes)
        api.cache.set(cache_key, result, ttl=120)
        return result
    except Exception as e:
        logger.error(f"❌ Erreur récupération entrées récentes: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") from e


@router.get("/export/psy-report")
async def export_psy_report() -> dict[str, Any]:
    """Export HTML prêt à imprimer pour psychologue.

    Retourne un objet JSON contenant le HTML et un nom de fichier recommandé.
    """
    rows = _fetch_all_entries()
    stats = _compute_basic_stats(rows)

    # Construction HTML simple et lisible
    def html_escape(s: str) -> str:
        return (
            s.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

    rows_html = []
    for r in rows[:200]:  # limiter pour impression
        rows_html.append(
            f"<tr>"
            f"<td>{html_escape(str(r['timestamp']))}</td>"
            f"<td>{int(r['intensity'])}</td>"
            f"<td>{html_escape(str(r['physical_trigger'] or ''))}</td>"
            f"<td>{html_escape(str(r['mental_trigger'] or ''))}</td>"
            f"<td>{html_escape(str(r['activity'] or ''))}</td>"
            f"<td>{html_escape(str(r['location'] or ''))}</td>"
            f"<td>{html_escape(str(r['action_taken'] or ''))}</td>"
            f"<td>{html_escape(str(r['effectiveness'] or ''))}</td>"
            f"<td>{html_escape(str(r['notes'] or ''))}</td>"
            f"<td>{html_escape(str(r.get('who_present') or ''))}</td>"
            f"<td>{html_escape(str(r.get('interactions') or ''))}</td>"
            f"<td>{html_escape(str(r.get('emotions') or ''))}</td>"
            f"<td>{html_escape(str(r.get('thoughts') or ''))}</td>"
            f"<td>{html_escape(str(r.get('physical_symptoms') or ''))}</td>"
            f"</tr>"
        )

    def li_kv(title: str, value: str) -> str:
        return f"<li><strong>{html_escape(title)}:</strong> {html_escape(value)}</li>"

    top_triggers_html = "".join(
        f"<li>{html_escape(t['trigger'])} — {t['count']} fois</li>"
        for t in stats["top_triggers"]
    )
    best_actions_html = "".join(
        f"<li>{html_escape(a['action'])} — efficacité moyenne {a['avg_effectiveness']} (n={a['samples']})</li>"
        for a in stats["best_actions"]
    )
    time_peaks_html = "".join(
        f"<li>{html_escape(p['hour'])}h — {p['count']} entrées</li>"
        for p in stats["time_peaks"]
    )

    html = f"""
<!doctype html>
<html lang=fr>
<head>
  <meta charset=utf-8>
  <title>Rapport Psychologue - ARIA</title>
  <style>
    body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif; margin: 24px; }}
    h1, h2 {{ margin: 0 0 8px 0; }}
    .muted {{ color: #666 }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    th, td {{ border: 1px solid #ddd; padding: 6px 8px; font-size: 13px; }}
    th {{ background: #fafafa; text-align: left; }}
    ul {{ padding-left: 18px; }}
  </style>
  <meta name=viewport content="width=device-width, initial-scale=1">
  <meta name=generator content="ARIA">
  <meta name=created content="{datetime.now().isoformat()}">
  <meta name=entries content="{stats['entries_count']}">
  <meta name=avg_intensity content="{stats['avg_intensity']}">
  <meta name=privacy content="local-first">
  <meta name=category content="pain-tracking">
  <meta name=audience content="psychologist">
  <meta name=language content="fr">
  <meta name=format content="html-printable">
  <meta name=security content="anonymized">
  <meta name=confidentiality content="high">
  <meta name=compliance content="RGPD-local-only">
  <meta name=version content="1.0">
  <meta name=tool content="arkalia-aria">
  <meta name=report-type content="psy">
  <meta name=summary content="Synthèse douleur, déclencheurs, interventions et historique">
  <meta name=export content="psy-report">
  <meta name=owner content="user-local">
  <meta name=hash content="">
  <meta name=notes content="">
  <meta name=tags content="douleur,psychologie,suivi">
  <meta name=retention content="user-controlled">
  <meta name=classification content="private">
  <meta name=scope content="personal-health">
  <meta name=origin content="local-db">
  <meta name=created-by content="arkalia-aria">
  <meta name=generated-by content="arkalia-aria">
  <meta name=license content="MIT">
  <meta name=terms content="local-use">
  <meta name=exported-at content="{datetime.now().isoformat()}">
</head>
<body>
  <h1>Rapport Psychologue</h1>
  <div class=muted>Généré par ARIA — {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>

  <h2>1. Synthèse</h2>
  <ul>
    {li_kv('Nombre d’entrées', str(stats['entries_count']))}
    {li_kv('Intensité moyenne', str(stats['avg_intensity']))}
  </ul>

  <div class=grid>
    <div>
      <h2>2. Top déclencheurs</h2>
      <ul>{top_triggers_html or '<li>Aucun</li>'}</ul>
    </div>
    <div>
      <h2>3. Actions les plus efficaces</h2>
      <ul>{best_actions_html or '<li>Aucune</li>'}</ul>
    </div>
  </div>

  <h2>4. Pics horaires</h2>
  <ul>{time_peaks_html or '<li>Aucun</li>'}</ul>

  <h2>5. Historique détaillé (dern. 200)</h2>
  <table>
    <thead>
      <tr>
        <th>Date/Heure</th><th>Intensité</th><th>Déclencheur</th><th>Mental</th>
        <th>Activité</th><th>Localisation</th><th>Action</th><th>Efficacité</th><th>Notes</th>
        <th>Qui présent</th><th>Interactions</th><th>Émotions</th><th>Pensées</th><th>Symptômes physiques</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows_html)}
    </tbody>
  </table>
</body>
</html>
"""

    return {
        "html": html,
        "filename": f"psy_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
        "entries_count": stats["entries_count"],
    }


@router.get("/suggestions")
async def pain_suggestions(window: int = 30) -> dict[str, Any]:
    """Génère des suggestions intelligentes basées sur des règles simples.

    window: nombre de jours récents à analyser (non strict ici, heuristique simple).
    """
    # Vérifier le cache (clé basée sur window)
    cache_key = f"pain_suggestions_{window}"
    cached_result = api.cache.get(cache_key)
    if cached_result is not None:
        logger.debug(f"📦 Suggestions depuis cache (window={window})")
        return cached_result

    rows = _fetch_all_entries()
    stats = _compute_basic_stats(rows)

    suggestions: list[str] = []

    # Règles déterministes simples et utiles en clinique
    if stats["avg_intensity"] >= 6:
        suggestions.append(
            "Intensité moyenne élevée: envisager des techniques de relaxation quotidiennes."
        )

    if stats["top_triggers"]:
        t0 = stats["top_triggers"][0]
        if t0["count"] >= 3:
            suggestions.append(
                f"Déclencheur fréquent identifié: {t0['trigger']} — prévoir stratégies d’évitement/atténuation."
            )

    if stats["best_actions"]:
        a0 = stats["best_actions"][0]
        if a0["avg_effectiveness"] >= 6:
            suggestions.append(
                f"Action efficace à privilégier: {a0['action']} (efficacité moyenne {a0['avg_effectiveness']})."
            )

    if stats["time_peaks"]:
        p0 = stats["time_peaks"][0]
        suggestions.append(
            f"Pic horaire récurrent: {p0['hour']}h — adapter les routines avant ce créneau."
        )

    questions_precision: list[str] = []
    if not stats["top_triggers"]:
        questions_precision.append(
            "Avez-vous remarqué un déclencheur physique récurrent ces derniers jours ?"
        )
    if not stats["best_actions"]:
        questions_precision.append(
            "Quelles actions avez-vous essayées et avec quel effet (0-10) ?"
        )

    result = {
        "window_days": window,
        "summary": stats,
        "suggestions": suggestions,
        "follow_up_questions": questions_precision,
        "generated_at": datetime.now().isoformat(),
    }

    # Mettre en cache (TTL 5 minutes car calcul coûteux)
    api.cache.set(cache_key, result, ttl=300)
    return result


@router.get("/export/csv")
async def export_csv():
    """Export CSV pour professionnels de santé"""
    _init_tables()
    try:
        # Limiter à 10000 entrées max pour éviter surcharge mémoire lors de l'export
        rows = db.execute_query(
            "SELECT * FROM pain_entries ORDER BY timestamp DESC LIMIT 10000"
        )

        # Génération CSV simple
        csv_content = "Date,Heure,Intensité,Déclencheur Physique,Déclencheur Mental,Activité,Localisation,Action,Efficacité,Notes,Qui présent,Interactions,Émotions,Pensées,Symptômes physiques\n"

        for row in rows:
            row_dict = dict(row)
            timestamp = row_dict["timestamp"]
            date, time = timestamp.split("T") if "T" in timestamp else (timestamp, "")
            csv_content += f"{date},{time},{row_dict['intensity']},{row_dict.get('physical_trigger') or ''},{row_dict.get('mental_trigger') or ''},{row_dict.get('activity') or ''},{row_dict.get('location') or ''},{row_dict.get('action_taken') or ''},{row_dict.get('effectiveness') or ''},{row_dict.get('notes') or ''},{row_dict.get('who_present') or ''},{row_dict.get('interactions') or ''},{row_dict.get('emotions') or ''},{row_dict.get('thoughts') or ''},{row_dict.get('physical_symptoms') or ''}\n"

        logger.info(f"📊 Export CSV généré: {len(rows)} entrées")
        return {
            "content": csv_content,
            "filename": f"pain_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "entries_count": len(rows),
        }
    except Exception as e:
        logger.error(f"❌ Erreur export CSV: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") from e


@router.get("/export/pdf")
async def export_pdf():
    """Export PDF pour professionnels de santé"""
    _init_tables()
    try:
        # Limiter à 10000 entrées max pour éviter surcharge mémoire lors de l'export
        rows = db.execute_query(
            "SELECT * FROM pain_entries ORDER BY timestamp DESC LIMIT 10000"
        )

        # Génération PDF simple (format texte)
        pdf_content = f"""RAPPORT DE DOULEUR - ARKALIA ARIA
Date d'export: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Nombre d'entrées: {len(rows)}

"""

        # En-têtes
        pdf_content += "DATE\tHEURE\tINTENSITÉ\tDÉCLENCHEUR PHYSIQUE\tDÉCLENCHEUR MENTAL\tACTIVITÉ\tLOCALISATION\tACTION\tEFFICACITÉ\tNOTES\tQUI PRÉSENT\tINTERACTIONS\tÉMOTIONS\tPENSÉES\tSYMPTÔMES PHYSIQUES\n"
        pdf_content += "-" * 200 + "\n"

        # Données
        for row in rows:
            row_dict = dict(row)
            timestamp = row_dict["timestamp"]
            date, time = timestamp.split("T") if "T" in timestamp else (timestamp, "")
            pdf_content += f"{date}\t{time}\t{row_dict['intensity']}\t{row_dict.get('physical_trigger') or ''}\t{row_dict.get('mental_trigger') or ''}\t{row_dict.get('activity') or ''}\t{row_dict.get('location') or ''}\t{row_dict.get('action_taken') or ''}\t{row_dict.get('effectiveness') or ''}\t{row_dict.get('notes') or ''}\t{row_dict.get('who_present') or ''}\t{row_dict.get('interactions') or ''}\t{row_dict.get('emotions') or ''}\t{row_dict.get('thoughts') or ''}\t{row_dict.get('physical_symptoms') or ''}\n"

        logger.info(f"📄 Export PDF généré: {len(rows)} entrées")
        return {
            "content": pdf_content,
            "filename": f"pain_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            "entries_count": len(rows),
        }
    except Exception as e:
        logger.error(f"❌ Erreur export PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") from e


@router.get("/export/excel")
async def export_excel():
    """Export Excel pour professionnels de santé"""
    _init_tables()
    try:
        # Limiter à 10000 entrées max pour éviter surcharge mémoire lors de l'export
        rows = db.execute_query(
            "SELECT * FROM pain_entries ORDER BY timestamp DESC LIMIT 10000"
        )

        # Génération Excel (format CSV avec séparateur tab)
        excel_content = "Date\tHeure\tIntensité\tDéclencheur Physique\tDéclencheur Mental\tActivité\tLocalisation\tAction\tEfficacité\tNotes\tQui présent\tInteractions\tÉmotions\tPensées\tSymptômes physiques\n"

        for row in rows:
            row_dict = dict(row)
            timestamp = row_dict["timestamp"]
            date, time = timestamp.split("T") if "T" in timestamp else (timestamp, "")
            excel_content += f"{date}\t{time}\t{row_dict['intensity']}\t{row_dict.get('physical_trigger') or ''}\t{row_dict.get('mental_trigger') or ''}\t{row_dict.get('activity') or ''}\t{row_dict.get('location') or ''}\t{row_dict.get('action_taken') or ''}\t{row_dict.get('effectiveness') or ''}\t{row_dict.get('notes') or ''}\t{row_dict.get('who_present') or ''}\t{row_dict.get('interactions') or ''}\t{row_dict.get('emotions') or ''}\t{row_dict.get('thoughts') or ''}\t{row_dict.get('physical_symptoms') or ''}\n"

        logger.info(f"📊 Export Excel généré: {len(rows)} entrées")
        return {
            "content": excel_content,
            "filename": f"pain_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            "entries_count": len(rows),
        }
    except Exception as e:
        logger.error(f"❌ Erreur export Excel: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") from e


@router.delete("/entries/{entry_id}")
async def delete_pain_entry(entry_id: int):
    """Supprime une entrée de douleur (RGPD - Droit à l'oubli)"""
    _init_tables()
    try:
        # Vérifier que l'entrée existe
        existing = db.execute_query(
            "SELECT id FROM pain_entries WHERE id = ?", (entry_id,)
        )
        if not existing:
            raise HTTPException(status_code=404, detail="Entrée non trouvée")

        # Supprimer l'entrée
        db.execute_query("DELETE FROM pain_entries WHERE id = ?", (entry_id,))

        logger.info(f"🗑️ Entrée {entry_id} supprimée (RGPD)")
        return {
            "message": f"Entrée {entry_id} supprimée avec succès",
            "entry_id": entry_id,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur suppression entrée {entry_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") from e


@router.delete("/entries")
async def delete_all_pain_entries():
    """Supprime toutes les entrées de douleur (RGPD - Droit à l'oubli complet)"""
    _init_tables()
    try:
        # Compter les entrées avant suppression
        count_result = db.execute_query("SELECT COUNT(*) as count FROM pain_entries")
        count = count_result[0]["count"] if count_result else 0

        # Supprimer toutes les entrées
        db.execute_query("DELETE FROM pain_entries")

        logger.info(f"🗑️ Toutes les entrées supprimées (RGPD): {count} entrées")
        return {
            "message": "Toutes les entrées supprimées avec succès",
            "deleted_count": count,
        }
    except Exception as e:
        logger.error(f"❌ Erreur suppression complète: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") from e
