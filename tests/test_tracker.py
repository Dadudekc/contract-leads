from lead_harvester.tracker import KPITracker, KPIMetrics
import os
import tempfile


def test_tracker_aggregate():
    with tempfile.TemporaryDirectory() as tmp:
        db = os.path.join(tmp, "kpi.db")
        tracker = KPITracker(db_path=db)
        tracker.log_run(KPIMetrics(leads_found=10, leads_contacted=5, leads_closed=2, revenue=200.0, avg_quality=12.0))
        tracker.log_run(KPIMetrics(leads_found=5, leads_contacted=2, leads_closed=1, revenue=50.0, avg_quality=8.0))
        agg = tracker.aggregate()
        assert agg["leads_found"] == 15
        assert agg["leads_contacted"] == 7
        assert agg["leads_closed"] == 3
        assert agg["revenue"] == 250.0
        assert round(agg["avg_quality"], 2) == 10.67
        assert round(agg["response_rate"], 2) == round(7/15*100, 2)
        assert round(agg["close_rate"], 2) == round(3/7*100, 2)

