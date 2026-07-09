"""
Live Warehouse Dashboard
-------------------------
Streamlit app that visualizes warehouse space utilization in near-real-time:
- Locates any SKU in the warehouse
- Shows allocated vs free space by zone, aisle, and bay
- Simulates "live" updates by periodically re-randomizing a slice of the data
  (swap this out for a real WMS/SAP IBP data feed in production)

Run with:
    streamlit run app/dashboard.py
"""
import random
import time
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "locations.csv"

st.set_page_config(page_title="Live Warehouse Dashboard", layout="wide")


@st.cache_data(ttl=5)
def load_data(_refresh_token: int) -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def simulate_live_update(df: pd.DataFrame, n_changes: int = 15) -> pd.DataFrame:
    """Randomly flips a handful of locations between occupied/free to mimic
    live picks and put-aways coming from a warehouse management system."""
    df = df.copy()
    idx = random.sample(range(len(df)), k=min(n_changes, len(df)))
    for i in idx:
        if df.loc[i, "status"] == "occupied":
            df.loc[i, ["status", "sku", "quantity"]] = ["free", "", 0]
        else:
            df.loc[i, "status"] = "occupied"
            df.loc[i, "sku"] = "SKU-1001-PalletWrap"
            df.loc[i, "quantity"] = random.randint(5, 200)
    df.to_csv(DATA_PATH, index=False)
    return df


def main() -> None:
    st.title("📦 Live Warehouse Dashboard")
    st.caption("Real-time view of storage utilization, free space, and item location.")

    if "refresh_token" not in st.session_state:
        st.session_state.refresh_token = 0

    col_a, col_b = st.columns([1, 5])
    with col_a:
        if st.button("🔄 Simulate live update"):
            df = load_data(st.session_state.refresh_token)
            simulate_live_update(df)
            st.session_state.refresh_token += 1

    df = load_data(st.session_state.refresh_token)

    # --- KPI row ---
    total = len(df)
    occupied = (df["status"] == "occupied").sum()
    free = total - occupied
    util_pct = round(occupied / total * 100, 1)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total locations", total)
    k2.metric("Occupied", int(occupied))
    k3.metric("Free", int(free))
    k4.metric("Utilization", f"{util_pct}%")

    st.divider()

    # --- Locate a SKU ---
    st.subheader("🔍 Locate an item")
    sku_options = sorted([s for s in df["sku"].unique() if s])
    selected_sku = st.selectbox("Choose a SKU", ["-- select --"] + sku_options)
    if selected_sku != "-- select --":
        matches = df[df["sku"] == selected_sku]
        st.write(f"Found in **{len(matches)}** location(s):")
        st.dataframe(
            matches[["location_id", "zone", "aisle", "bay", "level", "quantity"]],
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    # --- Utilization by zone ---
    st.subheader("📊 Utilization by zone")
    zone_summary = (
        df.groupby(["zone", "status"]).size().reset_index(name="count")
    )
    fig = px.bar(
        zone_summary,
        x="zone",
        y="count",
        color="status",
        barmode="stack",
        color_discrete_map={"occupied": "#d62728", "free": "#2ca02c"},
        labels={"count": "Locations", "zone": "Zone"},
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Heatmap grid per zone ---
    st.subheader("🗺️ Space map (select a zone)")
    zone_choice = st.selectbox("Zone", sorted(df["zone"].unique()))
    zone_df = df[df["zone"] == zone_choice].copy()
    zone_df["occupied_flag"] = (zone_df["status"] == "occupied").astype(int)
    pivot = zone_df.pivot_table(
        index="bay", columns="aisle", values="occupied_flag", aggfunc="mean"
    )
    fig2 = px.imshow(
        pivot,
        color_continuous_scale=["#2ca02c", "#d62728"],
        labels=dict(x="Aisle", y="Bay", color="Occupied ratio"),
        aspect="auto",
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.caption(
        "Green = mostly free · Red = mostly occupied. "
        "In production, swap `data/locations.csv` for a live WMS/SAP IBP feed."
    )


if __name__ == "__main__":
    main()
