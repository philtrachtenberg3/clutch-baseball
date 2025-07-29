from flask import Flask, render_template, request
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.patches import Patch
from datetime import datetime
from pybaseball import playerid_lookup, statcast_batter

app = Flask(__name__)

# --- Pitch grouping map ---
pitch_groups = {
    'FF': 'Fastball', 'FT': 'Fastball', 'SI': 'Fastball', 'FC': 'Fastball',
    'SL': 'Breaking', 'CU': 'Breaking', 'KC': 'Breaking', 'KN': 'Breaking', 'SV': 'Breaking',
    'CH': 'Changeup', 'FS': 'Changeup',
    'EP': 'Other', 'PO': 'Other', 'FO': 'Other'
}

strike_descriptions = {
    "called_strike", "swinging_strike", "swinging_strike_blocked",
    "foul", "foul_tip", "foul_bunt", "missed_bunt", "hit_into_play"
}

@app.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'img_path': None,
        'first': None,
        'last': None,
        'start': None,
        'end': None,
        'loading': False,
        'error': None
    }

    if request.method == 'POST':
        first = request.form.get('first_name') or "Bryce"
        last = request.form.get('last_name') or "Harper"
        start = request.form.get('start_date') or "2023-03-30"
        end = request.form.get('end_date') or "2023-10-01"

        context.update({'first': first, 'last': last, 'start': start, 'end': end, 'loading': True})

        try:
            player = playerid_lookup(last, first, fuzzy=True)
            if player.empty:
                context['error'] = f"Player '{first} {last}' not found."
                return render_template('form.html', **context)

            mlbam_id = player.iloc[0]['key_mlbam']
            df = statcast_batter(start, end, player_id=mlbam_id)
            df_zone = df[df['plate_x'].notnull() & df['plate_z'].notnull()].copy()
            df_zone['pitch_group'] = df_zone['pitch_type'].map(pitch_groups).fillna('Other')

            plt.figure(figsize=(6, 7))
            unique_groups = df_zone['pitch_group'].unique()
            palette = sns.color_palette("hls", len(unique_groups))
            color_map = dict(zip(unique_groups, palette))

            for group in unique_groups:
                group_data = df_zone[df_zone['pitch_group'] == group]
                for _, row in group_data.iterrows():
                    alpha_val = 0.8 if row['description'] in strike_descriptions else 0.3
                    plt.scatter(row['plate_x'], row['plate_z'],
                                c=[color_map[group]], alpha=alpha_val,
                                edgecolor='black', s=60)

            plt.axhline(1.5, color='black', linestyle='--')
            plt.axhline(3.5, color='black', linestyle='--')
            plt.axvline(-0.83, color='black', linestyle='--')
            plt.axvline(0.83, color='black', linestyle='--')

            plt.title(f"Pitch Locations for {first} {last} ({start} - {end})")
            plt.xlabel("Horizontal Plate Location (feet)")
            plt.ylabel("Vertical Plate Location (feet)")
            plt.xlim(-2, 2)
            plt.ylim(0, 5)
            plt.grid(True)

            legend_handles = [
                Patch(facecolor=color_map[group], edgecolor='black', label=group)
                for group in unique_groups
            ]
            plt.legend(handles=legend_handles, title="Pitch Type", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()

            img_path = f'static/strike_zone_plot.png'
            plt.savefig(img_path, dpi=300, bbox_inches='tight')
            plt.close()

            context['img_path'] = img_path
            context['loading'] = False

        except Exception as e:
            context['error'] = f"Error: {e}"
            context['loading'] = False

    return render_template('form.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
