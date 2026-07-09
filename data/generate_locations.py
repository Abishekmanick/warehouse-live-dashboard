"""
Generates a sample warehouse layout: zones, aisles, bays and levels,
each location tagged as occupied or free, with a SKU + quantity if occupied.
Run this once to create data/locations.csv, which the dashboard reads from.
"""
import csv
import random

random.seed(42)

ZONES = ["A", "B", "C", "D"]
AISLES_PER_ZONE = 5
BAYS_PER_AISLE = 8
LEVELS_PER_BAY = 4

SAMPLE_SKUS = [
    "SKU-1001-PalletWrap", "SKU-1002-SteelBrackets", "SKU-1003-CardboardBoxesL",
    "SKU-1004-PlasticCrates", "SKU-1005-WoodenPallets", "SKU-1006-FoamPadding",
    "SKU-1007-MetalRods", "SKU-1008-PlasticBins", "SKU-1009-RubberSeals",
    "SKU-1010-GlassPanels", "SKU-1011-CopperWire", "SKU-1012-AluminumSheets",
]


def generate_locations(occupancy_rate: float = 0.62) -> list[dict]:
    rows = []
    for zone in ZONES:
        for aisle in range(1, AISLES_PER_ZONE + 1):
            for bay in range(1, BAYS_PER_AISLE + 1):
                for level in range(1, LEVELS_PER_BAY + 1):
                    location_id = f"{zone}-{aisle:02d}-{bay:02d}-{level:02d}"
                    occupied = random.random() < occupancy_rate
                    row = {
                        "location_id": location_id,
                        "zone": zone,
                        "aisle": aisle,
                        "bay": bay,
                        "level": level,
                        "status": "occupied" if occupied else "free",
                        "sku": random.choice(SAMPLE_SKUS) if occupied else "",
                        "quantity": random.randint(5, 200) if occupied else 0,
                        "capacity": 200,
                    }
                    rows.append(row)
    return rows


def save_csv(rows: list[dict], path: str = "data/locations.csv") -> None:
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    data = generate_locations()
    save_csv(data)
    occupied = sum(1 for r in data if r["status"] == "occupied")
    print(f"Generated {len(data)} locations ({occupied} occupied, {len(data) - occupied} free)")
