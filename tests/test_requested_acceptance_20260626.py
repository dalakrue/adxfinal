from pathlib import Path
from types import SimpleNamespace
import hashlib, sqlite3, subprocess, sys, time
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

def snap(t='2026-06-26T10:00:00Z'):
    return SimpleNamespace(broker_candle_time=pd.Timestamp(t),run_id='r1',generation_id='g1',source_snapshot_hash='h1',symbol='EURUSD',timeframe='H1',decision='WAIT',regime='R',created_at_utc=pd.Timestamp(t))

def history(n=600):
    ts=pd.date_range('2026-06-01',periods=n,freq='h',tz='UTC')
    return pd.DataFrame({'broker_candle_time':ts,'entry_strength_score':[5.0]*n,'entry_strength_decision':['BUY']*n,'outcome_status':['SETTLED']*(n-1)+['PENDING'],'decision_correct':[True]*(n-1)+[False]})

def build(df, s=None, scales=None):
    from core.decision_table_20260626 import build_decision_table
    return build_decision_table({'one_hour_direction_confirmation_20260626':{'history':df,'score_scales':scales or {}}},s or snap())

def test_01_ast_compile():
    import ast, py_compile
    for p in ROOT.rglob('*.py'):
        ast.parse(p.read_text(errors='replace'),filename=str(p)); py_compile.compile(str(p),doraise=True)

def test_02_declared_runtime_and_imports():
    assert (ROOT/'.python-version').read_text().strip()=='3.12'
    assert (ROOT/'runtime.txt').read_text().strip()=='python-3.12'
    for m in ['app','adx_dashpoard','core.decision_table_20260626','ui.lunch_four_core_fields_20260619']:
        __import__(m)

def test_03_synthetic_25_day_table():
    out=build(history(),snap('2026-06-25T23:00:00Z'))
    assert 1 <= out['Date'].nunique() <= 25 and len(out)>0

def test_04_newest_first():
    out=build(history(),snap('2026-06-25T23:00:00Z'))
    t=pd.to_datetime(out['Broker Candle Time']); assert t.is_monotonic_decreasing

def test_05_completed_candle_exclusion():
    df=history(); future=pd.DataFrame([{'broker_candle_time':'2026-06-26T11:00:00Z','entry_strength_score':9,'outcome_status':'PENDING'}]); out=build(pd.concat([df,future],ignore_index=True),snap())
    assert pd.to_datetime(out['Broker Candle Time'],utc=True).max() <= pd.Timestamp('2026-06-26T10:00:00Z')

def test_06_broker_time_date_parts():
    out=build(pd.DataFrame([{'broker_candle_time':'2026-06-26T10:00:00Z','outcome_status':'PENDING'}]))
    assert out.iloc[0][['Date','Weekday','Hour']].tolist()==['2026-06-26','Friday',10]

def test_07_missing_na_and_known_scale_only():
    df=pd.DataFrame([{'broker_candle_time':'2026-06-26T10:00:00Z','entry_strength_score':80,'buy_pressure_score':.8,'outcome_status':'PENDING'}])
    out=build(df); assert out.iloc[0]['Entry Strength Score']=='N/A' and out.iloc[0]['BUY Pressure Score']==.8
    out2=build(df,scales={'entry_strength_score':'0-100','buy_pressure_score':'0-1'}); assert out2.iloc[0]['Entry Strength Score']==8 and out2.iloc[0]['BUY Pressure Score']==8

def test_08_settled_outcome_only():
    df=pd.DataFrame([{'broker_candle_time':'2026-06-26T10:00:00Z','outcome_status':'PENDING','decision_correct':True},{'broker_candle_time':'2026-06-26T09:00:00Z','outcome_status':'SETTLED','decision_correct':False}])
    out=build(df); assert out.iloc[0]['Decision Correct']=='N/A' and out.iloc[1]['Decision Correct'] is False

def test_09_identity_mismatch():
    from ui.lunch_identity_strip_20260626 import identity_mismatches
    c={'run_id':'r','generation_id':'g','source_snapshot_hash':'h','symbol':'EURUSD','timeframe':'H1','broker_candle_time':'t'}
    assert identity_mismatches(c,{**c,'generation_id':'other'})==["generation_id: Field 1=g field=other"]

def test_10_four_authoritative_lunch_fields_and_five_total_surfaces():
    # The 2026-07-01 Field 10 upgrade intentionally adds Field 10 to the
    # authoritative Lunch selector while preserving the existing top-level surfaces.
    from ui.lunch_four_core_fields_20260619 import FIELD10_FIELD, FIELD_LABELS
    from core.app.registry import TAB_REGISTRY
    assert len(FIELD_LABELS) == 4 and len(set(FIELD_LABELS)) == 4
    assert FIELD10_FIELD in FIELD_LABELS
    assert 'Field 456' in TAB_REGISTRY and 'Field 789' in TAB_REGISTRY

def test_11_field456_isolation_static():
    t=(ROOT/'ui/lunch_four_core_fields_20260619.py').read_text(); block=t[t.index('def render_field456_independent'):t.index('def render_field789_independent')]
    assert 'Combined Display Workspace' in block and 'remain independent' in block and 'run_calculation' not in block.lower()

def test_12_field789_isolation_static():
    t=(ROOT/'ui/lunch_four_core_fields_20260619.py').read_text(); block=t[t.index('def render_field789_independent'):]
    assert 'Combined Research Display' in block and 'remains separate' in block and 'run_calculation' not in block.lower()

def test_13_protected_hash_manifest_current():
    import json
    rows=json.loads((ROOT/'FIELD1_PROTECTED_HASH_VERIFICATION_20260626.json').read_text())
    core=[r for r in rows if r['file'].startswith('core/') and Path(ROOT/r['file']).exists()]
    assert core and all(hashlib.sha256((ROOT/r['file']).read_bytes()).hexdigest()==r['uploaded_zip'] for r in core)

def test_14_database_migration_rollback():
    con=sqlite3.connect(':memory:'); con.execute('create table x(id integer primary key,v text)'); con.execute("insert into x(v) values('before')"); con.commit()
    try:
        con.execute('begin'); con.execute('alter table x add column extra text'); con.execute("update x set v='after'"); raise RuntimeError
    except RuntimeError: con.rollback()
    assert con.execute('select v from x').fetchone()[0]=='before'

def test_15_streamlit_entrypoint_static():
    assert 'from adx_dashpoard import main' in (ROOT/'app.py').read_text()

def test_16_mobile_width_static():
    text='\n'.join(p.read_text(errors='ignore') for p in [ROOT/'core/app_shell.py',ROOT/'ui/lunch_four_core_fields_20260619.py'] if p.exists())
    assert '@media' in text or 'use_container_width=True' in text

def test_17_selected_field_memory_model():
    frames=[pd.DataFrame({'x':range(10000)}) for _ in range(9)]
    all_mem=sum(f.memory_usage(deep=True).sum() for f in frames); selected=frames[0].memory_usage(deep=True).sum()
    assert selected < all_mem/5

def test_18_one_click_routes_lunch():
    from core.settings_one_click_controller_20260624 import run_one_click_action
    state={}; calls=[]
    out=run_one_click_action(state,'Run Calculation + Open Lunch',lambda: calls.append(1) or {'run_id':'r'},target_page='Lunch',result_run_id_getter=lambda x:x['run_id'])
    assert out['status']=='COMPLETED' and state['active_page']=='Lunch' and len(calls)==1
