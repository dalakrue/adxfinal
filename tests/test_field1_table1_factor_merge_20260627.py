from types import SimpleNamespace
import pandas as pd
from core.decision_table_20260626 import build_decision_table


def test_table1_prefers_rich_factor_history_over_one_row_confirmation():
    times = pd.date_range('2026-06-01', periods=30, freq='D', tz='UTC')
    histories = {}
    specs = [
        ('Entry Strength','BUY'), ('SELL Pressure','SELL'), ('BUY Pressure','BUY'),
        ('Net Pressure','BUY'), ('Pullback Readiness','WAIT'), ('M1 Confirmation','BUY'),
        ('Master Decision','BUY'), ('Hold Safety','HOLD'), ('TP Quality','BUY'),
        ('Direction Confirmation','BUY'),
    ]
    for name, decision in specs:
        histories[name] = pd.DataFrame({'Broker Candle Time': times, 'Score /10': range(1,31), 'Decision': decision})
    state = {
        'one_hour_direction_confirmation_20260626': {
            'history': pd.DataFrame([{'broker_candle_time': times[-1], 'confirmation_action':'WAIT'}])
        },
        'lunch_metric_result_cache': {'history_by_factor': histories},
    }
    snapshot = SimpleNamespace(broker_candle_time=times[-1], run_id='r', generation_id='g')
    out = build_decision_table(state, snapshot)
    assert len(out) == 25
    assert out['Entry Strength Decision'].ne('N/A').all()
    assert out['Direction Confirmation Decision'].ne('N/A').all()
