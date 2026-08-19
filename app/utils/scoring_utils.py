def normalize(value: float, min_val: float, max_val: float, invert: bool = False) -> float:
    """
    Normalizes a value to a 0.0 - 1.0 scale.
    If invert is True, lower original values result in higher normalized scores.
    """
    if max_val == min_val:
        norm = 1.0 if value >= max_val else 0.0
    else:
        norm = (value - min_val) / (max_val - min_val)
        norm = max(0.0, min(1.0, norm))
    
    if invert:
        norm = 1.0 - norm
        
    return norm

def weighted_score(factors: dict, weights: dict) -> float:
    """
    Computes a weighted sum of normalized factors.
    Assumes factors are already 0-100 scaled appropriately.
    Weights should sum to 1.0.
    """
    score = 0.0
    for key, weight in weights.items():
        val = factors.get(key, 0.0)
        score += val * weight
    return max(0.0, min(100.0, score))
