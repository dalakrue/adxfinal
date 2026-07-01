"""Canonical AI evidence contract and deterministic intent routing for Field 5."""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
import re
from typing import Any, Mapping, MutableMapping

import pandas as pd

from core.publication_identity_20260625 import freeze_publication_identity
from core.session_context_20260625 import resolve_session_contract

INTENTS = (
    'tp_sl', 'entry', 'forecast_horizon', 'green_path', 'session', 'current_decision',
    'regime', 'reliability_uncertainty', 'history', 'reversal', 'model_comparison',
    'system_health', 'general_system_question',
)


@dataclass(frozen=True)
class ParsedQuestion:
    intent: str
    action: str | None = None
    horizon: int | None = None
    field_number: int | None = None
    last_n_days: int | None = None


def _m(v: Any) -> Mapping[str, Any]:
    return v if isinstance(v, Mapping) else {}


def _f(v: Any, default: float | None = None) -> float | None:
    try:
        x = float(v)
        return x if math.isfinite(x) else default
    except Exception:
        return default


def _canonical(state: Mapping[str, Any]) -> Mapping[str, Any]:
    from core.canonical_lookup_20260626 import resolve_canonical
    return resolve_canonical(state)


def _normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', str(text or '').strip().lower())


def _parse(text: str) -> ParsedQuestion:
    q = _normalize(text)
    action = None
    for candidate in ('buy', 'sell', 'wait'):
        if re.search(rf'\b{candidate}\b', q):
            action = candidate.upper()
            break
    horizon = None
    h = re.search(r'\bh\s*([1236])\b|\b([1236])h\b', q)
    if h:
        horizon = int(next(g for g in h.groups() if g))
    field_number = None
    f = re.search(r'\bfield\s*([1-9])\b', q)
    if f:
        field_number = int(f.group(1))
    last_n_days = None
    n = re.search(r'last\s+(\d+)\s+days?', q)
    if n:
        last_n_days = int(n.group(1))

    rules = [
        ('tp_sl', ('tp', 'sl', 'take profit', 'stop loss')),
        ('entry', ('entry', 'enter', 'entry decision')),
        ('forecast_horizon', ('prediction', 'forecast', 'h1', 'h2', 'h3', 'h6', 'projection')),
        ('green_path', ('green path', 'green line', 'less risky path', 'less-risky path')),
        ('session', ('session', 'london', 'new york', 'overlap', 'asia', 'sydney', 'which session is best')),
        ('current_decision', ('current decision', 'decision now', 'buy or sell')),
        ('regime', ('regime', 'market state', 'transition')),
        ('reliability_uncertainty', ('reliability', 'uncertainty', 'confidence', 'trust')),
        ('history', ('history', 'last 25', 'past', 'previous')),
        ('reversal', ('reverse', 'reversal', 'what will reverse')),
        ('model_comparison', ('model', 'compare', 'spa', 'cpa', 'best model')),
        ('system_health', ('ready', 'run id', 'system health', 'publication', 'sync', 'broker candle')),
    ]
    for intent, phrases in rules:
        if any(phrase in q for phrase in phrases):
            return ParsedQuestion(intent=intent, action=action, horizon=horizon, field_number=field_number, last_n_days=last_n_days)
    return ParsedQuestion(intent='general_system_question', action=action, horizon=horizon, field_number=field_number, last_n_days=last_n_days)


def _history_frame(state: Mapping[str, Any], limit: int = 25) -> list[dict[str, Any]]:
    for key in ('full_metric_history_df_20260618', 'prediction_vs_actual_history_df', 'dv_pp_bt_hist'):
        value = state.get(key)
        if isinstance(value, pd.DataFrame) and not value.empty:
            return value.head(limit).to_dict('records')
    return []


def build_ai_evidence_contract(state: Mapping[str, Any]) -> dict[str, Any]:
    canonical = _canonical(state)
    identity = freeze_publication_identity(state, canonical)
    session = resolve_session_contract(state, canonical).to_dict()
    final = _m(canonical.get('final_decision'))
    regime = _m(canonical.get('regime'))
    forecasts = _m(canonical.get('forecasts'))
    field2 = _m(state.get('session_adaptive_projection_20260625'))
    green_df = state.get('less_risky_projection_20260625')
    green_path = green_df.to_dict('records') if isinstance(green_df, pd.DataFrame) and not green_df.empty else []
    field7 = _m(state.get('field7_session_drift_cpa_20260625') or state.get('field_07_research_summary_v11'))
    field8 = _m(state.get('field8_session_calibration_spa_20260625') or state.get('field8_publication_status_20260624'))
    field9 = _m(state.get('field9_doubly_robust_20260625') or state.get('field9_eurusd_h1_decision_impact'))
    field6 = _m(state.get('field6_session_bayesian_fusion_20260625') or state.get('field6_combined_history_summary_20260622'))
    health = {
        'run_id_present': bool(identity['run_id']),
        'generation_id_present': bool(identity['generation_id']),
        'snapshot_hash_present': bool(identity['snapshot_hash']),
        'broker_candle_time_present': bool(canonical.get('broker_candle_time') or canonical.get('latest_completed_candle_time')),
        'canonical_identity_valid': all(bool(identity[k]) for k in ('run_id', 'generation_id', 'snapshot_hash')),
        'publication_status': 'READY' if all(bool(identity[k]) for k in ('run_id', 'generation_id', 'snapshot_hash')) else 'NOT_READY',
        'calculation_scope': str((state or {}).get('settings_calculation_scope_20260625') or 'FULL').upper(),
    }
    tp = _f(final.get('tp_price'), _f(canonical.get('tp_price')))
    sl = _f(final.get('sl_price'), _f(canonical.get('sl_price')))
    current_price = _f(_m(canonical.get('market')).get('current_price'), _f(canonical.get('current_price')))
    pack = {
        'identity': identity,
        'current_decision': str(final.get('final_decision') or canonical.get('decision') or 'UNAVAILABLE'),
        'entry_decision': str(final.get('entry_decision') or canonical.get('entry_decision') or final.get('final_decision') or 'UNAVAILABLE'),
        'less_risky_decision': str(final.get('less_risky_decision') or canonical.get('less_risky_bias') or 'UNAVAILABLE'),
        'current_price': current_price,
        'tp_sl': {'tp': tp, 'sl': sl},
        'prediction_horizons': forecasts,
        'green_path': green_path,
        'session': {**session, 'source_run_id': identity.get('run_id'), 'generation_id': identity.get('generation_id'), 'snapshot_hash': identity.get('snapshot_hash')},
        'regime_standards': {
            'major_regime': regime.get('major_regime') or regime.get('current_regime') or canonical.get('regime'),
            'reliability': regime.get('reliability') or regime.get('regime_reliability'),
            'three_standard_agreement': regime.get('three_standard_agreement') or regime.get('agreement_score'),
        },
        'reliability': canonical.get('reliability_score') or _m(canonical.get('reliability')).get('score') or regime.get('reliability'),
        'uncertainty': final.get('uncertainty_pct') or final.get('uncertainty') or canonical.get('uncertainty'),
        'reversal_conditions': field9.get('minimum_reversal_conditions') or _m(field9.get('current_summary')).get('reversal_conditions') or canonical.get('reversal_conditions') or 'UNAVAILABLE',
        'field1_history': _history_frame(state, 25),
        'field2_settled_evidence': field2,
        'field3_regime_evidence': regime,
        'field6_fusion_evidence': field6,
        'field7_drift_cpa_evidence': field7,
        'field8_calibration_spa_evidence': field8,
        'field9_counterfactual_value_evidence': field9,
        'system_health': health,
    }
    return pack


def validate_ai_evidence_contract(contract: Mapping[str, Any]) -> dict[str, Any]:
    missing = []
    identity = _m(contract.get('identity'))
    for key in ('run_id', 'generation_id', 'snapshot_hash'):
        if not identity.get(key):
            missing.append(key)
    if not _m(contract.get('session')).get('broker_candle_time'):
        missing.append('broker_candle_time')
    if not contract.get('current_decision'):
        missing.append('current_decision')
    return {"ready": len(missing) == 0, "missing_components": missing}


def _evidence_rows(contract: Mapping[str, Any], parsed: ParsedQuestion) -> list[dict[str, Any]]:
    identity = _m(contract.get('identity'))
    rows = []
    def add(source_field: str, metric: str, value: Any):
        rows.append({
            'source field': source_field,
            'metric': metric,
            'value': value,
            'origin time': _m(contract.get('session')).get('broker_candle_time'),
            'run_id': identity.get('run_id'),
            'generation_id': identity.get('generation_id'),
            'snapshot_hash': identity.get('snapshot_hash'),
        })
    add('identity', 'current_decision', contract.get('current_decision'))
    add('identity', 'less_risky_decision', contract.get('less_risky_decision'))
    add('identity', 'current_price', contract.get('current_price'))
    if parsed.horizon:
        forecasts = _m(contract.get('prediction_horizons')).get('horizons')
        item = _m(_m(forecasts).get(f'{parsed.horizon}h') if isinstance(forecasts, Mapping) else {})
        add('field2', f'H{parsed.horizon} forecast', item)
    if parsed.intent == 'green_path':
        green = contract.get('green_path') or []
        add('field2', 'green_path_rows', len(green))
    if parsed.intent == 'session':
        add('field2', 'selected_session', _m(contract.get('session')).get('selected_session'))
    return rows


def _horizon_item(contract: Mapping[str, Any], horizon: int | None) -> Mapping[str, Any]:
    forecasts = _m(contract.get('prediction_horizons')).get('horizons')
    if isinstance(forecasts, Mapping):
        if horizon is None:
            horizon = 3
        return _m(forecasts.get(f'{horizon}h') or forecasts.get(str(horizon)) or forecasts.get(horizon))
    return {}


def _answer(parsed: ParsedQuestion, contract: Mapping[str, Any]) -> str:
    identity = _m(contract.get('identity'))
    current_price = _f(contract.get('current_price'))
    session = _m(contract.get('session'))
    if parsed.intent == 'tp_sl':
        tp = _f(_m(contract.get('tp_sl')).get('tp'))
        sl = _f(_m(contract.get('tp_sl')).get('sl'))
        action = parsed.action or str(contract.get('current_decision') or 'UNAVAILABLE')
        lines = [f'Action: {action}', f'Current price: {current_price if current_price is not None else "UNAVAILABLE"}']
        if tp is not None:
            pips = abs(tp - current_price) * 10000 if current_price is not None else None
            lines.append(f'TP: {tp}')
            lines.append(f'Distance in pips: {pips:.1f}' if pips is not None else 'Distance in pips: UNAVAILABLE')
        else:
            lines.append('TP evidence unavailable')
        if sl is not None:
            lines.append(f'SL: {sl}')
        lines.append(f'Relevant horizon: H{parsed.horizon or 3}')
        lines.append(f'Broker candle: {session.get("broker_candle_time") or "UNAVAILABLE"}')
        lines.append(f'Run ID: {identity.get("run_id") or "UNAVAILABLE"}')
        lines.append('Evidence sources: canonical decision, protected forecast bundle, AI evidence contract')
        return '\n'.join(lines)
    if parsed.intent == 'forecast_horizon':
        item = _horizon_item(contract, parsed.horizon)
        return f"H{parsed.horizon or 3} prediction: {item or 'UNAVAILABLE'}\nBroker candle: {session.get('broker_candle_time')}\nRun ID: {identity.get('run_id')}"
    if parsed.intent == 'green_path':
        green = contract.get('green_path') or []
        if not green:
            validation = validate_ai_evidence_contract(contract)
            missing = list(validation.get('missing_components') or [])
            suffix = f" Missing components: {missing}." if missing else ''
            return 'Green-path evidence unavailable for this run because the exact published central path, current price, or valid bounds are not all available.' + suffix
        row = green[0]
        return (
            f"The green line is lower than the main path because shrinkage pulls the session-adjusted central path back toward the current price. "
            f"Current price={row.get('Current Price')}; base central={row.get('Base Central Path')}; session-adjusted={row.get('Session-Adjusted Path')}; "
            f"green={row.get('Green Less-Risky Path')}; path trust={row.get('Path Trust')}; tier={row.get('Green Tier')}; reason codes={row.get('Reason Codes')}."
        )
    if parsed.intent == 'session':
        evidence = _m(contract.get('field2_settled_evidence'))
        stats = evidence.get('stats') if isinstance(evidence.get('stats'), pd.DataFrame) else pd.DataFrame()
        if stats.empty:
            return 'No settled session performance evidence is available yet, so no best session is claimed.'
        rows = []
        for _, r in stats.sort_values(['direction_accuracy', 'sample_count'], ascending=[False, False]).iterrows():
            rows.append(f"{r['session']}: n={int(r['sample_count'])}, direction_accuracy={float(r['direction_accuracy']):.3f}, coverage={float(r['interval_coverage']):.3f}")
        return 'Settled session comparison:\n' + '\n'.join(rows[:5])
    if parsed.intent == 'current_decision':
        return f"Current decision: {contract.get('current_decision')}\nLess-risky decision: {contract.get('less_risky_decision')}\nRun ID: {identity.get('run_id')}"
    if parsed.intent == 'regime':
        return f"Regime evidence: {contract.get('regime_standards')}"
    if parsed.intent == 'reliability_uncertainty':
        return f"Reliability: {contract.get('reliability')}\nUncertainty: {contract.get('uncertainty')}"
    if parsed.intent == 'history':
        return f"Field 1 history rows available: {len(contract.get('field1_history') or [])}\nMost recent sample: {(contract.get('field1_history') or ['UNAVAILABLE'])[0]}"
    if parsed.intent == 'reversal':
        return f"Minimum reversal conditions: {contract.get('reversal_conditions')}"
    if parsed.intent == 'model_comparison':
        return f"Field 7 evidence: {contract.get('field7_drift_cpa_evidence')}\nField 8 evidence: {contract.get('field8_calibration_spa_evidence')}"
    if parsed.intent == 'system_health':
        validation = validate_ai_evidence_contract(contract)
        valid = bool(validation.get("ready"))
        missing = list(validation.get("missing_components") or [])
        return f"System health: {'READY' if valid else 'NOT READY'}\nMissing components: {missing or 'NONE'}\nIdentity: {identity}\nBroker candle: {session.get('broker_candle_time')}"
    return 'General answer — not canonical market evidence. This assistant only supports the saved EURUSD H1 system evidence domain.'


def answer_canonical_question(question: str, state: MutableMapping[str, Any]) -> dict[str, Any]:
    contract = build_ai_evidence_contract(state)
    validation = validate_ai_evidence_contract(contract)
    valid = bool(validation.get("ready"))
    missing = list(validation.get("missing_components") or [])
    parsed = _parse(question)
    answer = _answer(parsed, contract)
    if parsed.intent == 'general_system_question':
        answer = 'This AI assistant answers only from the saved EURUSD H1 canonical evidence domain. Ask about TP/SL, entry, horizon, green path, session, decision, regime, reliability, history, reversal, model comparison, or system health.'
    evidence = _evidence_rows(contract, parsed)
    evidence_hash = sha256(json.dumps({'contract': contract.get('identity'), 'intent': parsed.intent, 'question': question}, sort_keys=True, default=str).encode('utf-8')).hexdigest()
    return {
        'answer': answer,
        'status': 'ANSWER' if parsed.intent != 'general_system_question' else 'GENERAL',
        'intent': parsed.intent,
        'run_id': _m(contract.get('identity')).get('run_id') or 'UNAVAILABLE',
        'normalized_query': _normalize(question),
        'evidence': contract,
        'evidence_used': evidence,
        'evidence_hash': evidence_hash,
        'full_recalculation_performed': False,
        'ready': valid,
        'missing_components': missing,
        'parsed': parsed.__dict__,
    }


# Backward-compatible helpers.
def normalize_query(question: str) -> str:
    return _normalize(question)


def detect_intent(question: str) -> str:
    return _parse(question).intent


def build_intent_evidence(question: str, state: Mapping[str, Any]) -> dict[str, Any]:
    parsed = _parse(question)
    return {'intent': parsed.intent, 'query': _normalize(question), 'evidence': build_ai_evidence_contract(state)}


__all__ = [
    'INTENTS', 'normalize_query', 'detect_intent', 'build_intent_evidence',
    'build_ai_evidence_contract', 'validate_ai_evidence_contract', 'answer_canonical_question'
]
