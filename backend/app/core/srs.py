from datetime import datetime, timedelta

def calculate_sm2(quality: int, repetitions: int, previous_interval: int, previous_ease_factor: float):
    """
    SM-2 Spaced Repetition Algorithm.
    quality: 1 (red, failed), 2 (yellow, hard), 3 (green, easy)
    """
    # Map our quality (1-3) to typical SM-2 (0-5)
    # 1 -> 1 (Incorrect)
    # 2 -> 3 (Correct but difficult)
    # 3 -> 5 (Perfect response)
    
    q_mapped = 1
    if quality == 2:
        q_mapped = 3
    elif quality == 3:
        q_mapped = 5

    if q_mapped < 3:
        # Failed to recall
        repetitions = 0
        interval = 1
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = int(round(previous_interval * previous_ease_factor))
        repetitions += 1

    ease_factor = previous_ease_factor + (0.1 - (5 - q_mapped) * (0.08 + (5 - q_mapped) * 0.02))
    
    if ease_factor < 1.3:
        ease_factor = 1.3

    return {
        "interval": interval,
        "repetitions": repetitions,
        "ease_factor": ease_factor
    }

def get_next_review_date(interval: int) -> datetime:
    return datetime.utcnow() + timedelta(days=interval)
