import json

with open("c:/Users/Vigne/OneDrive/Desktop/Phonepe Pulse/analysis.ipynb", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("c:/Users/Vigne/OneDrive/Desktop/Phonepe Pulse/insights_extracted.txt", "w", encoding="utf-8") as out:
    for cell in data.get("cells", []):
        if cell.get("cell_type") == "markdown":
            source = "".join(cell.get("source", []))
            if "Insight" in source:
                out.write(source + "\n\n" + "="*50 + "\n\n")
