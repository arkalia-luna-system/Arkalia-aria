"""
Pain Tracking API - Module de suivi de la douleur ARIA
"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from typing import Any, TypedDict

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()

DB_FILENAME = "aria_pain.db"


def _db_path() -> str:
    # Permettre de configurer l'emplacement via variable d'environnement
    env_path = os.getenv("ARIA_DB_PATH")
    if env_path:
        return env_path
    # Par défaut, placer la base dans le répertoire data/ à la racine du projet si disponible
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(project_root, "data")
    try:
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, DB_FILENAME)
    except Exception:
        # Fallback: stockage local au module
        return os.path.join(os.path.dirname(__file__), DB_FILENAME)


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def _init_tables() -> None:
    conn = _get_conn()
    try:
        conn.execute(
            """
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
                created_at TEXT NOT NULL DEFAULT (DATETIME('now'))
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def _fetch_all_entries() -> list[sqlite3.Row]:
    """Récupère toutes les entrées triées par date (récentes d'abord)."""
    _init_tables()
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT * FROM pain_entries ORDER BY timestamp DESC, id DESC"
        ).fetchall()
        return rows
    finally:
        conn.close()


class ActionEff(TypedDict):
    action: str
    avg_effectiveness: float
    samples: int


def _compute_basic_stats(rows: list[sqlite3.Row]) -> dict[str, Any]:
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
    _init_tables()
    ts = datetime.now().isoformat()

    conn = _get_conn()
    try:
        cur = conn.execute(
            """
            INSERT INTO pain_entries (
                timestamp, intensity, physical_trigger, action_taken
            ) VALUES (?, ?, ?, ?)
            """,
            (ts, int(entry.intensity), entry.physical_trigger, entry.action_taken),
        )
        conn.commit()
        new_id = cur.lastrowid
        row = conn.execute(
            "SELECT * FROM pain_entries WHERE id = ?", (new_id,)
        ).fetchone()
        assert row is not None
        return PainEntryOut(**dict(row))
    finally:
        conn.close()


@router.post("/entry", response_model=PainEntryOut)
async def create_pain_entry(entry: PainEntryIn) -> PainEntryOut:
    """Création d'une entrée détaillée"""
    _init_tables()
    ts = entry.timestamp or datetime.now().isoformat()

    conn = _get_conn()
    try:
        cur = conn.execute(
            """
            INSERT INTO pain_entries (
                timestamp, intensity, physical_trigger, mental_trigger, activity,
                location, action_taken, effectiveness, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            ),
        )
        conn.commit()
        new_id = cur.lastrowid
        row = conn.execute(
            "SELECT * FROM pain_entries WHERE id = ?", (new_id,)
        ).fetchone()
        assert row is not None
        return PainEntryOut(**dict(row))
    finally:
        conn.close()


@router.get("/entries", response_model=list[PainEntryOut])
async def list_pain_entries() -> list[PainEntryOut]:
    """Liste toutes les entrées de douleur"""
    _init_tables()
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT * FROM pain_entries ORDER BY timestamp DESC, id DESC"
        ).fetchall()
        return [PainEntryOut(**dict(r)) for r in rows]
    finally:
        conn.close()


@router.get("/entries/recent", response_model=list[PainEntryOut])
async def list_recent(limit: int = 20) -> list[PainEntryOut]:
    """Liste les entrées récentes"""
    _init_tables()
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT * FROM pain_entries ORDER BY timestamp DESC, id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [PainEntryOut(**dict(r)) for r in rows]
    finally:
        conn.close()


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

    return {
        "window_days": window,
        "summary": stats,
        "suggestions": suggestions,
        "follow_up_questions": questions_precision,
        "generated_at": datetime.now().isoformat(),
    }


@router.get("/export/csv")
async def export_csv():
    """Export CSV pour professionnels de santé"""
    _init_tables()
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT * FROM pain_entries ORDER BY timestamp DESC"
        ).fetchall()

        # Génération CSV simple
        csv_content = "Date,Heure,Intensité,Déclencheur Physique,Déclencheur Mental,Activité,Localisation,Action,Efficacité,Notes\n"

        for row in rows:
            timestamp = row["timestamp"]
            date, time = timestamp.split("T") if "T" in timestamp else (timestamp, "")
            csv_content += f"{date},{time},{row['intensity']},{row['physical_trigger'] or ''},{row['mental_trigger'] or ''},{row['activity'] or ''},{row['location'] or ''},{row['action_taken'] or ''},{row['effectiveness'] or ''},{row['notes'] or ''}\n"

        return {
            "content": csv_content,
            "filename": f"pain_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "entries_count": len(rows),
        }
    finally:
        conn.close()
