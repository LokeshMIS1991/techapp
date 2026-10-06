import pandas as pd

def compute_auto_rating_suggestion(worker_id: str, visits_df: pd.DataFrame) -> float:
    """
    Computes an automated performance rating recommendation (out of 10) based on:
    - Photo upload compliance
    - Service payment collection success rate
    """
    if visits_df.empty:
        return 8.0
        
    worker_visits = visits_df[visits_df['Worker_ID'] == worker_id]
    if worker_visits.empty:
        return 8.0
        
    total_visits = len(worker_visits)
    
    # 1. Photo compliance score
    if 'Pre_Work_Photo' in worker_visits.columns and 'Post_Work_Photo' in worker_visits.columns:
        compliant_visits = len(worker_visits[worker_visits['Pre_Work_Photo'].notna() & worker_visits['Post_Work_Photo'].notna()])
        photo_score = (compliant_visits / total_visits) * 10.0
    else:
        photo_score = 10.0
        
    # 2. Collection efficiency score for Service Visits
    service_visits = worker_visits[worker_visits['Work_Type'] == 'Service / Repair']
    if not service_visits.empty and 'Payment_Status' in service_visits.columns:
        collected = len(service_visits[service_visits['Payment_Status'] == 'Collected'])
        collection_score = (collected / len(service_visits)) * 10.0
    else:
        collection_score = 10.0

    # Composite Weighted Score
    final_score = round((photo_score * 0.5) + (collection_score * 0.5), 1)
    return min(max(final_score, 1.0), 10.0)