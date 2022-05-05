#read csv and make bar plot
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('xtick', labelsize=16)
matplotlib.rc('ytick', labelsize=16)

directory = "./reduction.csv"

df =  pd.read_csv(directory)

print(df)

x = df['user'].values
y = df['reduction_per'].values

fig, ax = plt.subplots()

ax.set_yticks([80,82,84,86,88,90,92,94,96,98,100], ['80', '82', '84', '86', '88', '90', '92', '94', '96', '98', '100'])
# ax.set_yticks([0,10,20,30,40,50,60,70,80,90,100], ['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'])
ax.set_xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30], ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'])

ax.set_xlabel('User', fontsize=18)
ax.set_ylabel('Probe reduction (%)', fontsize=18)
ax.grid(axis = 'y', color = "grey", linewidth = "1", linestyle = "--")

colors =  ['lightpink', 'lightsalmon', 'lightgoldenrodyellow', 'lavender', 'lightcoral', 'lightseagreen', 'lightcyan', 'lightgreen', 'lightgray', 'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellow', 'wheat', 'beige', 'lightpink', 'lightsalmon', 'lightgoldenrodyellow', 'lavender', 'lightcoral', 'lightseagreen', 'lightcyan', 'lightgreen', 'lightgray', 'lightskyblue', 'lightslategray', 'lightsteelblue', 'lightyellow', 'wheat', 'beige']

every_nth = 3
for n, label in enumerate(ax.xaxis.get_ticklabels()):
    if n % every_nth != 0:
        label.set_visible(False)

ax.bar(x,y, color='lightsalmon')
ax.set_ylim([80, 100])
plt.tight_layout()
plt.savefig(f"../../reduction.png")
plt.close()