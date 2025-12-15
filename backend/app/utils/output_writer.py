import os
import json
from datetime import datetime
import numpy as np


class OutputWriter:
    """
    Saves system outputs to text files (assignment requirement)
    """

    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def _sanitize(self, obj):
        """
        Recursively convert non-JSON-serializable objects
        (e.g., numpy types) into native Python types.
        """
        if isinstance(obj, dict):
            return {k: self._sanitize(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._sanitize(v) for v in obj]
        elif isinstance(obj, np.generic):
            return obj.item()  # numpy -> python scalar
        else:
            return obj

    def save(self, label: str, data: dict):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{label}_{timestamp}.txt"
        path = os.path.join(self.output_dir, filename)

        safe_data = self._sanitize(data)

        with open(path, "w", encoding="utf-8") as f:
            f.write("=== MULTI-AGENT OUTPUT ===\n\n")
            f.write(json.dumps(safe_data, indent=2, ensure_ascii=False))

        return path
