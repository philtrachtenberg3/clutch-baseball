from pybaseball import playerid_lookup, statcast_batter
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- Defaults ---
DEFAULT_FIRST = "Bryce"
DEFAULT_LAST = "Harper"
DEFAULT_START = "2023-03-30"
DEFAULT_END = "2023-10-01"

# Get user input
batter_last_name = input("What is the batter's last name? ") or DEFAULT_LAST
batter_first_name = input("What is the batter's first name? ") or DEFAULT_FIRST
start_date_range = input("What is the start date (YYYY-MM-DD)? ") or DEFAULT_START
end_date_range = input("What is the end date (YYYY-MM-DD)? ") or DEFAULT_LAST

# Optional: warn if date is badly formatted
def validate_date(date_str, fallback):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        print(f"❌ '{date_str}' is not valid. Using default: {fallback}")
        return fallback

start_date_range = validate_date(start_date_range, DEFAULT_START)
end_date_range = validate_date(end_date_range, DEFAULT_END)

# --- Get Player ID ---
print(f"\nFetching data for {batter_first_name} {batter_last_name}...")
player = playerid_lookup(batter_last_name, batter_first_name, fuzzy=True)

# Check if a player is found
if player.empty:
    print("❌ No player found.")
    exit()

mlbam_id = player.iloc[0]['key_mlbam']

# Get Statcast data
df = statcast_batter(start_date_range, end_date_range, player_id=mlbam_id)
print(df)
# ---- DISPLAY STRIKE ZONE TARGET ----

# Filter out rows without location data
df_zone = df[df['plate_x'].notnull() & df['plate_z'].notnull()]

# Plot pitch locations
plt.figure(figsize=(5, 6))
plt.scatter(df_zone['plate_x'], df_zone['plate_z'], alpha=0.5, c='red', edgecolor='black')

# Draw the strike zone
# Strike zone is roughly from 1.5 to 3.5 feet in height and -0.83 to 0.83 in width
plt.axhline(1.5, color='black', linestyle='--')
plt.axhline(3.5, color='black', linestyle='--')
plt.axvline(-0.83, color='black', linestyle='--')
plt.axvline(0.83, color='black', linestyle='--')

plt.title(f"Pitch Locations for {batter_first_name} {batter_last_name} ({start_date_range} - {end_date_range})")
plt.xlabel("Horizontal Plate Location (feet)")
plt.ylabel("Vertical Plate Location (feet)")
plt.xlim(-2, 2)
plt.ylim(0, 5)
plt.grid(True)

# Print target to .png file
plt.savefig("strike_zone_plot.png", dpi=300, bbox_inches='tight')