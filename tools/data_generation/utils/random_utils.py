# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

import random

def set_random_seed(seed: int = None) -> None:
    """
    Set random seed for reproducibility.
    
    Args:
        seed: Random seed (None = truly random)
    """
    if seed is not None:
        random.seed(seed)