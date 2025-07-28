# 🧢 Clutch Hitter Analyzer

A Python project that analyzes how "clutch" a baseball player is based on Statcast data.

This tool helps identify players like Bryce Harper and Kyle Schwarber who thrive in high-pressure situations — and exposes players who fade when it matters most.

## 🔍 Features

- Pulls Statcast pitch-by-pitch data using `pybaseball`
- Filters for high-leverage clutch scenarios (e.g. RISP, 2 outs, late innings)
- Visualizes pitch locations on a strike zone plot
- Calculates hard-hit rate in clutch vs overall

## 📦 Requirements

- Python 3.9+
- `pybaseball`
- `pandas`
- `matplotlib`

Install dependencies:

```bash
pip install -r requirements.txt