import os
from matplotlib.patches import Patch
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def get_file_values(file_path):
    vet_iteration = []
    vet_value = []
    vet_weight = []
    vet_remaining_capacity = []
    vet_execution_time = []
    total_execution_time = 0

    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        if len(lines) > 1:
            total_execution_time = float(lines.pop())

        for ind, line in enumerate(lines[1:]):
            line = line.strip().split(';')
            vet_iteration.append(int(line[0]))
            vet_value.append(int(line[1]) if line[1] != '' else 0)
            vet_weight.append(int(line[2]) if line[2] != '' else 0)
            vet_remaining_capacity.append(int(line[3]) if line[3] != '' else -1)
            vet_execution_time.append(float(line[4]))

    return vet_iteration, vet_value, vet_weight, vet_execution_time, vet_remaining_capacity

def get_mean_and_std(vet_value, roundNumber = False):
    mean = np.mean(vet_value)
    std_value = np.std(vet_value) # std = desvio-padrao

    if roundNumber == True:
        mean = round(mean, 4)
        std_value = round(std_value, 4)

    return mean, std_value

def get_all_values_metrics(vet_value, vet_weight, vet_execution_time, vet_remaining_capacity):
    value_mean, value_std = get_mean_and_std(vet_value)
    weight_mean, weight_std = get_mean_and_std(vet_weight)
    execution_time_mean, execution_time_std = get_mean_and_std(vet_execution_time, True)
    remaining_capacity_mean, remaining_capacity_std = get_mean_and_std(vet_remaining_capacity)

    value_metrics = {'mean': value_mean, 'std': value_std}
    weight_metrics = {'mean': weight_mean, 'std': weight_std}
    execution_time_metrics = {'mean': execution_time_mean, 'std': execution_time_std}
    remaining_capacity_metrics = {'mean': remaining_capacity_mean, 'std': remaining_capacity_std}

    full_capacity = vet_weight[0] + vet_remaining_capacity[0]

    return value_metrics, weight_metrics, execution_time_metrics, remaining_capacity_metrics

def generate_value_x_execution_time_graph(vet_file_names, vet_value_ga, vet_value_std_ga, vet_value_grasp, vet_value_std_grasp, 
                                          vet_execution_time_ga, vet_execution_time_grasp):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ga_bar_color = 'blue'
    grasp_bar_color = 'orange'
    ga_line_color = 'red'
    grasp_line_color = 'green'

    # splitting the bars
    width = 0.35
    x = np.arange(len(vet_file_names))
    x1 = x - width/2
    x2 = x + width/2

    # bar graph for values
    ax1.bar(x1, vet_value_ga, width=width, label='Value mean - GA', alpha=0.7, color=ga_bar_color, yerr=vet_value_std_ga, capsize=5)
    ax1.bar(x2, vet_value_grasp, width=width, label='Value mean - GRASP', alpha=0.7, color=grasp_bar_color, yerr=vet_value_std_grasp, capsize=5)

    ax1.set_xlabel('Files')
    ax1.set_ylabel('Value mean')
    ax1.set_xticks(x)
    ax1.set_xticklabels(vet_file_names, rotation=90)

    ax2 = ax1.twinx()
    ax2.plot(x1, vet_execution_time_ga, label='Execution time(s) mean - GA', marker='o', linestyle='--', color=f'tab:{ga_line_color}')
    ax2.plot(x2, vet_execution_time_grasp, label='Execution time(s) mean - GRASP', marker='o', linestyle='--', color=f'tab:{grasp_line_color}')
    ax2.set_ylabel('Execution time(s) mean')

    # legends
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')
    
    plt.title("Value mean x Execution time(s) mean", fontsize=16)

    plt.tight_layout()
    plt.savefig('graph_value_x_time.png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.show()

def generate_weight_value_graph(vet_file_names, vet_weight_ga, vet_weight_std_ga, vet_weight_grasp, vet_weight_std_grasp, 
                                          vet_value_ga, vet_value_grasp):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ga_bar_color = 'blue'
    grasp_bar_color = 'orange'
    ga_line_color = 'red'
    grasp_line_color = 'green'

    # splitting the bars
    width = 0.35
    x = np.arange(len(vet_file_names))
    x1 = x - width/2
    x2 = x + width/2

    # bar graph for weights
    ax1.bar(x1, vet_weight_ga, width=width, label='Weight mean - GA', alpha=0.7, color=ga_bar_color, yerr=vet_weight_std_ga, capsize=5)
    ax1.bar(x2, vet_weight_grasp, width=width, label='Weight mean - GRASP', alpha=0.7, color=grasp_bar_color, yerr=vet_weight_std_grasp, capsize=5)

    ax1.set_xlabel('Files')
    ax1.set_ylabel('Weight mean')
    ax1.set_xticks(x)
    ax1.set_xticklabels(vet_file_names, rotation=90)

    ax2 = ax1.twinx()
    ax2.plot(x1, vet_value_ga, label='Value mean - GA', marker='o', linestyle='--', color=f'tab:{ga_line_color}')
    ax2.plot(x2, vet_value_grasp, label='Value mean - GRASP', marker='o', linestyle='--', color=f'tab:{grasp_line_color}')
    ax2.set_ylabel('Value mean')

    # legends
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')
    
    plt.title("Weight mean x Value mean", fontsize=16)

    plt.tight_layout()
    plt.savefig('graph_weight_x_value.png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.show()

def generate_datatable(vet_file_names, vet_value_ga, vet_weight_ga, vet_execution_time_ga,
                       vet_value_grasp, vet_weight_grasp, vet_execution_time_grasp):
    
    df = pd.DataFrame({
        'File': vet_file_names,
        'Value (GA)': vet_value_ga,
        'Value (GRASP)': vet_value_grasp,
        'Weight (GA)': vet_weight_ga,
        'Weight (GRASP)': vet_weight_grasp,
        'Time(s) (GA)': vet_execution_time_ga,
        'Time(s) (GRASP)': vet_execution_time_grasp
    })

    df.set_index('File', inplace=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    table_data = pd.plotting.table(ax, df, loc='center', cellLoc='center', colColours=['#c9daf8']*len(df.columns))

    ga_color = 'blue'
    grasp_color = 'orange'

    for col_name, cell in table_data.get_celld().items():
        row_number, col_number = col_name

        if col_number == 0 or col_number == 1: #se for valor
            ga_value = vet_value_ga[row_number-1]
            grasp_value = vet_value_grasp[row_number-1]
        if col_number == 2 or col_number == 3: #se for peso
            ga_value = vet_weight_ga[row_number-1]
            grasp_value = vet_weight_grasp[row_number-1]
        if col_number == 4 or col_number == 5: #se for tempo
            ga_value = vet_execution_time_ga[row_number-1]
            grasp_value = vet_execution_time_grasp[row_number-1]

        if col_number % 2 == 0:
            cell.set_facecolor(ga_color)

            if row_number == 0:
                pass
            elif (ga_value < grasp_value and col_number == 4) or (ga_value > grasp_value and col_number != 4):
                cell.set_text_props(fontweight='bold', color='green')
            else:
                cell.set_text_props(fontweight='bold', color='red')

        elif col_number % 2 != 0 and col_number != -1:
            cell.set_facecolor(grasp_color)

            if row_number == 0:
                pass
            elif (grasp_value < ga_value and col_number == 5) or (grasp_value > ga_value and col_number != 5):
                cell.set_text_props(fontweight='bold', color='green')
            else:
                cell.set_text_props(fontweight='bold', color='red')

        cell.set_alpha(0.2)

    legend_elements = [
        Patch(facecolor=ga_color, label='GA'),
        Patch(facecolor=grasp_color, label='GRASP')
    ]

    ax.legend(handles=legend_elements, loc='upper right')

    table_data.auto_set_font_size(False)
    table_data.set_fontsize(12)
    table_data.scale(1.2, 1.2)

    plt.title("General data presented as an average", fontsize=16)

    plt.savefig('dt_general.png', bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.show()

def generate_graphs(results_ga, results_grasp):
    vet_file_names = [result['File'] for result in results_ga]

    vet_value_ga = [result['Value mean'] for result in results_ga]
    vet_value_std_ga = [result['Value std'] for result in results_ga]
    vet_weight_ga = [result['Weight mean'] for result in results_ga]
    vet_weight_std_ga = [result['Weight std'] for result in results_ga]
    vet_execution_time_ga = [result['Execution time(s) mean'] for result in results_ga]
    vet_remaining_capacity_ga = [result['Remaining capacity mean'] for result in results_ga]

    vet_value_grasp = [result['Value mean'] for result in results_grasp]
    vet_value_std_grasp = [result['Value std'] for result in results_grasp]
    vet_weight_grasp = [result['Weight mean'] for result in results_grasp]
    vet_weight_std_grasp = [result['Weight std'] for result in results_grasp]
    vet_execution_time_grasp = [result['Execution time(s) mean'] for result in results_grasp]
    vet_remaining_capacity_grasp = [result['Remaining capacity mean'] for result in results_grasp]

    generate_value_x_execution_time_graph(vet_file_names, vet_value_ga, vet_value_std_ga, vet_value_grasp, vet_value_std_grasp, vet_execution_time_ga, vet_execution_time_grasp)
    
    generate_weight_value_graph(vet_file_names, vet_weight_ga, vet_weight_std_ga, vet_weight_grasp, vet_weight_std_grasp, vet_value_ga, vet_value_grasp)
    
    generate_datatable(vet_file_names, vet_value_ga, vet_weight_ga, vet_execution_time_ga,
                       vet_value_grasp, vet_weight_grasp, vet_execution_time_grasp)

def main():
    results_ga = []
    results_grasp = []

    folder_path_ga = "../output/ga"
    folder_path_grasp = "../output/grasp"

    for ind, file in enumerate(os.listdir(folder_path_ga)):
        file_path = os.path.join(folder_path_ga, file)
        vet_iteration, vet_value, vet_weight, vet_execution_time, vet_remaining_capacity  = get_file_values(file_path)
        value_metrics, weight_metrics, execution_time_metrics, remaining_capacity_metrics = get_all_values_metrics(vet_value, vet_weight, vet_execution_time, vet_remaining_capacity)
        results_ga.append({'File': str(ind+1)+'.out', 'Value mean': value_metrics['mean'], 'Value std': value_metrics['std'],
                           'Weight mean': weight_metrics['mean'], 'Weight std': weight_metrics['std'],
                           'Execution time(s) mean': execution_time_metrics['mean'], 'Execution time(s) std': execution_time_metrics['std'],
                           'Remaining capacity mean': remaining_capacity_metrics['mean'], 'Remaining capacity std': remaining_capacity_metrics['std']})

    for ind, file in enumerate(os.listdir(folder_path_grasp)):
        file_path = os.path.join(folder_path_grasp, file)
        vet_iteration, vet_value, vet_weight, vet_execution_time, vet_remaining_capacity = get_file_values(file_path)
        value_metrics, weight_metrics, execution_time_metrics, remaining_capacity_metrics = get_all_values_metrics(vet_value, vet_weight, vet_execution_time, vet_remaining_capacity)
        results_grasp.append({'File': str(ind+1)+'.out', 'Value mean': value_metrics['mean'], 'Value std': value_metrics['std'],
                           'Weight mean': weight_metrics['mean'], 'Weight std': weight_metrics['std'],
                           'Execution time(s) mean': execution_time_metrics['mean'], 'Execution time(s) std': execution_time_metrics['std'],
                           'Remaining capacity mean': remaining_capacity_metrics['mean'], 'Remaining capacity std': remaining_capacity_metrics['std']})

    generate_graphs(results_ga, results_grasp)

if __name__ == "__main__":
  main()