from pybaseball import playerid_lookup, statcast_batter
import pandas as pd
import matplotlib.pyplot as plt

# Get player ID
player = playerid_lookup('Harper', 'Bryce', fuzzy=True)
mlbam_id = player.iloc[0]['key_mlbam']

# Get Statcast data
df = statcast_batter('2023-03-30', '2023-10-01', player_id=mlbam_id)
print(df)

# DISPLAY STRIKE ZONE TARGET

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

plt.title("Pitch Locations for Player")
plt.xlabel("Horizontal Plate Location (feet)")
plt.ylabel("Vertical Plate Location (feet)")
plt.xlim(-2, 2)
plt.ylim(0, 5)
plt.grid(True)

plt.savefig("strike_zone_plot.png", dpi=300, bbox_inches='tight')