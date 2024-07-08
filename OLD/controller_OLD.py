""" Plot summary audiogram from filtered database exported 
    from Subject Browser.

    Written by: Travis M. Moore
    Created: May 18, 2023
    Last edited: May 19, 2023
"""

###########
# Imports #
###########
# Import data science packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#################
# Organize Data #
#################
# Import data
#_path = r'C:\Users\MooTra\OneDrive - Starkey\Documents\Projects\DEM\Recruiting\filtered_db_2023_Apr_14_1243.csv'
#_path = r'C:\Users\MooTra\OneDrive - Starkey\Desktop\Full Clean.csv'
#_path = r'C:\Users\MooTra\OneDrive - Starkey\Desktop\Full minus monaural.csv'
_path = r'C:\Users\MooTra\OneDrive - Starkey\Desktop\Full only bilateral.csv'
audios = pd.read_csv(_path)

# right_ac = range(8,18)
# left_ac = range(22,32)
# cols = list(right_ac) + list(left_ac)

# ac_thresholds = audios.iloc[:,cols].copy()
# ac_thresholds.replace('-', np.NaN, inplace=True)
# ac_thresholds = ac_thresholds.astype(float)
# x = pd.DataFrame(ac_thresholds.mean()).transpose()
# x.insert(loc=0, column='Subject Id', value='average')


def get_thresholds(sub_id, data):
    """ Make a dictionary of subject thresholds.
    """
    # Get AC thresholds
    sides = ["RightAC", "LeftAC"]
    freqs = [250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
    ac = {}
    for side in sides:
        for freq in freqs:
            colname = side + " " + str(freq)
            try:
                ac[side + ' ' + str(freq)] = int(
                    data[data['Subject Id'] == sub_id][colname].values[0])
            except ValueError:
                # Don't include missing values
                pass
    return ac


def plot_audio(sub_id, data, ax):
    # Get AC and BC thresholds
    ac = get_thresholds(sub_id, data)

    # Plot AC thresholds
    x = list(ac.items())
    right_ac_freqs = [int(j[0].split()[1]) for j in x if 'Right' in j[0]]
    right_ac_thresh = [j[1] for j in x if 'Right' in j[0]]
    left_ac_freqs = [int(j[0].split()[1]) for j in x if 'Left' in j[0]]
    left_ac_thresh = [j[1] for j in x if 'Left' in j[0]]

    if sub_id == 'average':
        ax.plot(right_ac_freqs)
    ax.plot(right_ac_freqs, right_ac_thresh)
    ax.plot(left_ac_freqs, left_ac_thresh)


def audio3():
    ax = plt.gca()

    # Plot formatting
    ax.set_ylim((-10,120))
    ax.invert_yaxis()
    yticks = range(-10,130,10)
    ax.set_yticks(ticks=yticks)
    ax.set_ylabel("Hearing Threshold (dB HL)")
    ax.semilogx()
    ax.set_xlim((200,9500))
    ax.set_xticks(ticks=[250,500,1000,2000,4000,8000], labels=[
        '250','500','1000','2000','4000','8000'])
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.set_xlabel("Frequency (Hz)")
    ax.axhline(y=25, color="black", linestyle='--', linewidth=1)
    ax.grid()
    ax.set_title(f"Study Audiograms")

    # # Plot color regions
    # audio_colors = ["gray", "green", "gold", "orange", "mediumpurple", 
    #     "lightsalmon"]
    # alpha_val = 0.25
    # degree_dict={
    #     'normal': (-10, 25),
    #     'mild': (25, 40),
    #     'moderate': (40, 55),
    #     'moderately-severe': (55, 70),
    #     'severe': (70, 90),
    #     'profound': (90, 120)
    # }
    # for idx, key in enumerate(degree_dict):
    #     coords = [
    #         [0,degree_dict[key][0]], 
    #         [9500,degree_dict[key][0]], 
    #         [9500,degree_dict[key][1]], 
    #         [0,degree_dict[key][1]]
    #     ]
    #     # Repeat the first point to create a 'closed loop'
    #     coords.append(coords[0])
    #     # Create lists of x and y values 
    #     xs, ys = zip(*coords) 
    #     # Fill polygon
    #     ax.fill(xs,ys, edgecolor='none', 
    #         facecolor=audio_colors[idx], alpha=alpha_val)

    return ax


# Collapse across left/right
freqs = [250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
right_ac = audios.iloc[:, 8:18].copy()
right_ac.columns = freqs
left_ac = audios.iloc[:, 22:32].copy()
left_ac.columns = freqs
data = pd.concat([right_ac, left_ac], ignore_index=True)

# Replace missing values with NaN
data.replace('-', np.NaN, inplace=True)
data = data.astype(float)

# Create plot artist
ax = audio3()

# Plot individual thresholds
for ii in range(0, len(data)):
    # Create mask to account for NaNs
    vals = data.iloc[ii,:]
    print(vals)
    mask = np.isfinite(vals)
    ax.plot(vals[mask].index, vals[mask], color='dimgrey')

# Plot average thresholds
avg = data.mean()
ax.plot(avg.index, avg, color='red', linestyle='--', linewidth=5)

plt.show()





# ax = audio3()

# for sub in audios['Subject Id'].unique():
#     plot_audio(sub, ax)

# plt.show()