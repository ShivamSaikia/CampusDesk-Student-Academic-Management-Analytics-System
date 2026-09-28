import csv
import json
import os

def export_csv(filename, headers, rows):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def export_json(filename, headers, rows):
    data = [dict(zip(headers, row)) for row in rows]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
