import os
import numpy as np
import matplotlib.pyplot as plt

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

        for line in lines[1:]:
            line = line.strip().split(';')
            vet_iteration.append(int(line[0]))
            vet_value.append(int(line[1]))
            vet_weight.append(int(line[2]))
            vet_remaining_capacity.append(int(line[3]))
            vet_execution_time.append(float(line[4]))

    return vet_iteration, vet_value, vet_weight, vet_execution_time, vet_remaining_capacity

def get_mean_and_std(vet_value):
    mean = np.mean(vet_value)
    std_value = np.std(vet_value) # std = desvio-padrao

    return mean, std_value

def get_all_values_metrics(vet_value, vet_weight, vet_execution_time, vet_remaining_capacity):
    value_mean, value_std = get_mean_and_std(vet_value)
    weight_mean, weight_std = get_mean_and_std(vet_weight)
    execution_time_mean, execution_time_std = get_mean_and_std(vet_execution_time)
    remaining_capacity_mean, remaining_capacity_std = get_mean_and_std(vet_remaining_capacity)

    value_metrics = {'mean': value_mean, 'std': value_std}
    weight_metrics = {'mean': weight_mean, 'std': weight_std}
    execution_time_metrics = {'mean': execution_time_mean, 'std': execution_time_std}
    remaining_capacity_metrics = {'mean': remaining_capacity_mean, 'std': remaining_capacity_std}

    full_capacity = vet_weight[0] + vet_remaining_capacity[0]

    return value_metrics, weight_metrics, execution_time_metrics, remaining_capacity_metrics

def generate_value_x_execution_time_graph(vet_file_names, vet_value_ga, vet_value_std_ga, vet_value_grasp, vet_value_std_grasp, vet_execution_time_ga, vet_execution_time_grasp):
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

    # subtitle
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.tight_layout()
    plt.show() 

def generate_graphs(results_ga, results_grasp):
    vet_file_names = [result['File'] for result in results_ga]

    vet_value_ga = [result['Value mean'] for result in results_ga]
    vet_value_std_ga = [result['Value std'] for result in results_ga]
    vet_weight_ga = [result['Weight mean'] for result in results_ga]
    vet_execution_time_ga = [result['Execution time(s) mean'] for result in results_ga]
    vet_remaining_capacity_ga = [result['Remaining capacity mean'] for result in results_ga]

    vet_value_grasp = [result['Value mean'] for result in results_grasp]
    vet_value_std_grasp = [result['Value std'] for result in results_grasp]
    vet_weight_grasp = [result['Weight mean'] for result in results_grasp]
    vet_execution_time_grasp = [result['Execution time(s) mean'] for result in results_grasp]
    vet_remaining_capacity_grasp = [result['Remaining capacity mean'] for result in results_grasp]

    generate_value_x_execution_time_graph(vet_file_names, vet_value_ga, vet_value_std_ga, vet_value_grasp, vet_value_std_grasp, vet_execution_time_ga, vet_execution_time_grasp)

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