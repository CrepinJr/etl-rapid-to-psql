import pandas as pd

def transform(data):
    df = pd.DataFrame([{
        "category": data.get("category"),
        "type": data.get("type"),
        "setup": data.get("setup"),
        "delivery": data.get("delivery"),
        "safe": data.get("safe"),
        "lang": data.get("lang")
    }])
    return df
