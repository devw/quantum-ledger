"""File handling utilities."""

from pathlib import Path


class OutputManager:
    """Manages output file paths and operations."""
    
    def __init__(self, output_dir: str = "/tmp"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def get_path(self, filename: str) -> Path:
        """Get full path for output file."""
        return self.output_dir / filename
    
    def save_text(self, content: str, filename: str) -> Path:
        """Save text content to file."""
        output_path = self.get_path(filename)
        with open(output_path, 'w') as f:
            f.write(content)
        print(f"  ✓ Saved: {output_path}")
        return output_path