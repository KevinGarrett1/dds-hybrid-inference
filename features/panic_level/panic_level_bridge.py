# panic_level_bridge.py
import pandas as pd
from jsonschema import validate

def load_panic_level_features(path: str):
    """Load and validate panic_level feature file."""
    df = pd.read_csv(path)

    schema = {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "panic_level": {"type": "number", "minimum": 0.0, "maximum": 1.0}
        },
        "required": ["text", "panic_level"]
    }

    for _, row in df.head(10).iterrows():
        validate(instance=row.to_dict(), schema=schema)

    print("✅ panic_level features validated successfully")
    return df
