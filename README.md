# Live Warehouse Dashboard

A real-time dashboard for tracking warehouse space utilization — locate any item instantly,
see allocated vs free space, and monitor utilization by zone, aisle, and bay.

## Features
- 🔍 **Item locator** — search any SKU and see every location it's stored in
- 📊 **Utilization breakdown** — occupied vs free space by zone
- 🗺️ **Visual space map** — heatmap of aisle/bay occupancy per zone
- 🔄 **Live simulation** — mimics real-time picks/put-aways from a WMS feed

## Tech stack
- Python 3
- Streamlit (dashboard UI)
- Pandas (data handling)
- Plotly (charts and heatmaps)

## Getting started

```bash
pip install -r requirements.txt
python data/generate_locations.py   # generate sample warehouse layout
streamlit run app/dashboard.py
```

## Project structure
```
warehouse-live-dashboard/
├── app/
│   └── dashboard.py        # Streamlit app
├── data/
│   ├── generate_locations.py  # sample data generator
│   └── locations.csv          # generated warehouse layout (created on first run)
├── requirements.txt
└── README.md
```

## Connecting to a real system
Replace `data/locations.csv` with a live query against your WMS, SAP IBP, or OMP
system, and point `load_data()` in `app/dashboard.py` at that source instead of
the CSV file. The rest of the dashboard logic works unchanged.

## Roadmap ideas
- Real-time push updates via WebSocket instead of manual refresh
- Alerting when a zone crosses a utilization threshold
- Pick-path optimization suggestions based on current occupancy
