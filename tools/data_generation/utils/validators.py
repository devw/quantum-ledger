# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

def validate_range(value: float, min_val: float, max_val: float, metric_name: str = "value") -> None:
    """
    Validate that a value is within expected range.
    
    Args:
        value: Value to validate
        min_val: Minimum acceptable value
        max_val: Maximum acceptable value
        metric_name: Name of metric for error messages
        
    Raises:
        ValueError: If value is outside range
    """
    if not (min_val <= value <= max_val):
        raise ValueError(f"{metric_name} = {value:.2f} is outside range [{min_val}, {max_val}]")