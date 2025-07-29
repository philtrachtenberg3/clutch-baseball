# 🧢 Clutch Player Project

I need a project to work on and I know baseball pretty well. I'm trying to create something where I can measure someone's "clutchness" in baseball. I have a hypothesis that even though stats may be similar, players like Harper and Schwarber are much more clutch than players like Castellanos. It seems obvious in this example since those are 2 of the best hitters in the league, but the point is there are players I'd much rather have up when I need a hit (even in non-high-impact situations, but where emotionally we need a hit), and it doesn't need to be someone with a .280 average if that person doesn't measure as clutch. There will probably be an analysis here of whether the metric correlates with batting average. The goal is to find undervalued players a la Moneyball, but also to validate it by showing that the top players are at the top.

Right now the query takes way too long to run.

## 🔍 Features

Right now, the app runs locally via Flask. It provides a form for entering a batter's name and date range, then returns a visualized strike zone plot showing pitches colored by pitch group and shaded by result (strike vs. ball).

(ChatGPT):
- Pulls Statcast pitch-by-pitch data using `pybaseball`
- Filters for high-leverage clutch scenarios (e.g. RISP, 2 outs, late innings)
- Visualizes pitch locations on a strike zone plot
- Calculates hard-hit rate in clutch vs overall

## 📊 Example Output

Here’s an example strike zone plot for Bryce Harper:

![Strike Zone Plot](/static/strike_zone_plot_readme.png)

## 📦 Requirements

- Python 3.9+
- `pybaseball`
- `pandas`
- `matplotlib`

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🚀 Running the App

1. Clone this repo:

```bash
git clone https://github.com/philtrachtenberg3/clutch-baseball.git
cd clutch-baseball
