###########
# Imports #
###########
# Import data science packages
import matplotlib.pyplot as plt


def audio3():
    ax = plt.gca()

    # Plot formatting
    ax.set_ylim((-10,120))
    ax.invert_yaxis()
    yticks = range(-10,130,10)
    ax.set_yticks(ticks=yticks)
    ax.set_ylabel("Hearing Threshold (dB HL)")
    ax.semilogx()
    ax.set_xlim((200,4500))
    ax.set_xticks(ticks=[250,500,750,1000,1500,2000,3000,4000], labels=[
        '250','500','750','1000','1500','2000','3000','4000'])
    ax.tick_params(axis='x', which='minor', bottom=False)
    ax.set_xlabel("Frequency (Hz)")
    ax.axhline(y=25, color="black", linestyle='--', linewidth=1)
    ax.grid()
    ax.set_title(f"Audiograms")

    # Plot color regions
    audio_colors = ["gray", "green", "gold", "orange", "mediumpurple", 
        "lightsalmon"]
    alpha_val = 0.25
    degree_dict={
        'normal': (-10, 25),
        'mild': (25, 40),
        'moderate': (40, 55),
        'moderately-severe': (55, 70),
        'severe': (70, 90),
        'profound': (90, 120)
    }
    for idx, key in enumerate(degree_dict):
        coords = [
            [0,degree_dict[key][0]], 
            [9500,degree_dict[key][0]], 
            [9500,degree_dict[key][1]], 
            [0,degree_dict[key][1]]
        ]
        # Repeat the first point to create a 'closed loop'
        coords.append(coords[0])
        # Create lists of x and y values 
        xs, ys = zip(*coords) 
        # Fill polygon
        ax.fill(xs,ys, edgecolor='none', 
            facecolor=audio_colors[idx], alpha=alpha_val)

    return ax

FREQS = [250, 500, 750, 1000, 1500, 2000, 3000, 4000]
N2 = [20, 20, 25, 25, 30, 35, 40, 45]
N3 = [35, 35, 35, 40, 45, 50, 55, 60]
N4 = [55, 55, 55, 55, 60, 65, 70, 75]

ax = audio3()
ax.plot(FREQS, N2, linewidth=5, label='N2')
ax.plot(FREQS, N3, linewidth=5, label='N3')
ax.plot(FREQS, N4, linewidth=5, label='N4')
ax.legend()
plt.show()
