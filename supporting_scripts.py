import os.path
import re

from Eulerlike_transformation.EulerlikeTransformer import EulerlikeTransformer
from Eulerlike_transformation.ODESystem import ODESystem
import pandas as pd
import matplotlib.pyplot as plt


def variable_latex_to_python(latex_string):
    latex_string = re.sub(r'\,', '_c_', latex_string)
    latex_string = re.sub(r'\{', '_lcb_', latex_string)
    latex_string = re.sub(r'\}', '_rcb_', latex_string)
    # Replace ^ with underscores
    latex_string = re.sub(r'\^', '_pwr_', latex_string)
    # Replace \mhyphen with underscores
    latex_string = re.sub(r'\\mhyphen ', '_hyp_', latex_string)
    print(latex_string)
    return latex_string


def ode_eulerlike_transform_to_aeon(equations_ode_file_path, output_eaon_file_path):
    """
    Takes in file with each ODE on a separate line in a latex format names and discetized meaning that each continuous
    function is replaced by the variable itself, or 1-var.

    For now also expects \\ and a space before = (equals sign)
    :return: None
    """
    if equations_ode_file_path is None or output_eaon_file_path is None:
        print("File names not provided")
        return
    ode_system = ODESystem(equations_ode_file_path)
    bn = EulerlikeTransformer(ode_system)
    bn.save_bn_to_aeon(output_eaon_file_path)


def parameter_names():
    with open("parameter_names.txt", "r") as f:
        with open("parameter_names_python.txt", "w") as of:
            for line in f:
                if line != "":
                    new_name = variable_latex_to_python(line)
                    print(new_name, file=of)


def gyn_cycle_augusta_run():
    df = pd.read_csv('model_3_gyn-cycle/copasi_simulation_100d.csv', delimiter='\t')
    df = df.T
    import Augusta
    df = df.iloc[1:]
    rows_to_drop = ['Ant_c', 'Ago_R-i', 'Ago_R-a','Ant_p','Ant_d',
                    'Ago_d', 's113', 's114', 's115', 's116',
                    'Ago_c', 'Ant_R', ]
    for row_to_drop in rows_to_drop:
        df = df.drop(index=row_to_drop)
    df = df * 1000
    print(df.index)
    print(df)
    df.to_csv('output.csv', sep=';')
    Augusta.RNASeq_to_BN(count_table_input = 'output.csv')
#hormonal_cycle_augusta_run()


def predator_prey_augusta_run():
    df = pd.read_csv('model_1_predator-prey/predator_prey_ODE_sim_results.csv', delimiter='\t')
    time_column = df.columns[0]
    df = df[df['Time'] >= 4]
    for column in df.columns[1:]:
        #plt.figure(figsize=(10, 6))  # Create a new figure for each column
        plt.plot(df[time_column], df[column], label=column)
    plt.legend()
    plt.grid(True)
    plt.show()
    df = df.T
    df = df.iloc[1:]
    import Augusta
    #df = (df * 100).astype(int)
    print(df.index)
    print(df)
    df.to_csv('predator_prey_ODE_sim_results_T.csv', sep=';')
    Augusta.RNASeq_to_BN(count_table_input = 'predator_prey_ODE_sim_results_T.csv')
#predator_prey_augusta_run()


def gyn_cycle_augusta_visualization():
    df = pd.read_csv('model_3_gyn-cycle/copasi_simulation_100d.csv', delimiter='\t')
    columns_to_drop = ['Ant_c', 'Ago_R-i', 'Ago_R-a','Ant_p','Ant_d',
                        'Ago_d', 's113', 's114', 's115', 's116',
                        'Ago_c', 'Ant_R', 'LH_Pit', 'FSH_pit']
    #df = df.drop(columns=columns_to_drop)
    print(df)
    time_column = df.columns[0]
    columns_to_plot = ['LH_bld', 'FSH_bld', 'P4', 'E2']
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()
    for column, ax in zip(columns_to_plot, axes):
        #plt.figure(figsize=(10, 6))  # Create a new figure for each column
        ax.plot(df[time_column], df[column], label=column)
        ax.set_title(column)
        ax.set_xlabel('days')
        plt.grid(True)
    #plt.title(f"Time Series Plot for {column}")
    #plt.legend()
    plt.tight_layout()
    plt.show()
#gyn_cycle_augusta_visualization()


def hormonal_cycle_euler_transform_to_aeon():
    create_aeon_model("model_3_gyn-cycle/hormonal_cycle_equations.txt", "model_3_gyn-cycle/boolean_functions_aeon.aeon")
    with open("boolean_functions_aeon", "a") as bool_funcs_aeon:
        print("$mass: true", file=bool_funcs_aeon, end='\n')
        print("$freq: !freq", file=bool_funcs_aeon, end='\n')
        print("freq -? freq", file=bool_funcs_aeon, end='\n')


def simplify_parameters_file(in_file, out_file):
    remove_left_brackets = '_lcb_'
    remove_right_brackets = '_rcb_'
    remove_power = '_pwr_'
    my_hyphen = '_hyp_'
    with open(in_file, 'r') as file:
        content = file.read()
    updated_content = content.replace(remove_left_brackets, '')
    updated_content = updated_content.replace(remove_right_brackets, '')
    updated_content = updated_content.replace(remove_power, '')
    updated_content = updated_content.replace(my_hyphen, 'mhyphen')
    with open(out_file, 'w') as file:
        file.write(updated_content)
#gc_param_file = os.path.join(os.getcwd(), "old_files", "parameters_gc.txt")
#gc_param_simplified = os.path.join(os.getcwd(), "old_files", "parameters_gc_simplified.txt")
#simplify_parameters_file(gc_param_file, gc_param_simplified)


def SAILoR_to_aeon(list_of_boolean_functions, aeon_file_path):
    """
    $LH_pit: !P4
    P4 -? LH_pit
    """
    with open(aeon_file_path, 'w') as file:
        for boolean_function in list_of_boolean_functions:
            variable, rhs = boolean_function.split(" = ")
            equation = re.sub(r'and', '&', rhs)
            equation = re.sub(r'or', '|', equation)
            equation = re.sub(r'not ', '!', equation)
            print("$" + variable + ":", equation, file=file)
            pattern = r'\b!?\w+\b'
            variables = re.findall(pattern, equation)
            unique_variables = sorted(set(variables))
            if unique_variables[0] == '0' or unique_variables[0] == '1':
                continue
            for input_variable in unique_variables:
                print(input_variable + " -? " + variable, file=file)


def simplify_TS(raw_ts, binarized_ts, simplified_raw, simplified_bin):
    binarized_data = pd.read_csv(binarized_ts, sep=",", index_col=0)

    simplified_ts_states = list()
    indexes = []
    for i in range(len(binarized_data.columns)):
        column = binarized_data.columns[i]
        state = list(binarized_data[column])
        if len(simplified_ts_states) == 0:
            simplified_ts_states.append(state)
            indexes.append(i)
            continue
        if simplified_ts_states[-1] != state:
            simplified_ts_states.append(state)
            indexes.append(i)
    print(simplified_ts_states)
    print(indexes)
    names = list(binarized_data.index)
    df = pd.DataFrame(simplified_ts_states).T
    df.index = names
    df.to_csv(simplified_bin)


def visualize_lynx_hare():
    df = pd.read_csv("model_1_predator-prey/Leigh1968_harelynx.csv")

    # Assume the first column is the 'Year' and the rest are values for different labels
    years = df.iloc[:, 0]  # First column (Years)
    values = df.iloc[:, 1:]  # All other columns (Values)

    # Plot each value series against years
    plt.figure(figsize=(10, 6))
    for column in values.columns:
        plt.plot(years, values[column], label=column)

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('# of furs sold to Hudson Bay company')
    plt.title('Hudson Bay company Lynx-Hare dataset (1847 - 1903)')

    # Optional: Add a legend to indicate what each line represents
    plt.legend(loc='upper left')

    # Show the plot
    plt.grid(True)  # Optional: Add grid for better readability
    plt.show()
#visualize_lynx_hare()


def visualize_lynx_hare_discrete():
    df = pd.read_csv("model_1_predator-prey/Leigh1968_harelynx.csv")
    # Assume the first column is the 'Year' and the rest are values for different labels
    years = df.iloc[:, 0]  # First column (Years)
    values = df.iloc[:, 1:]  # All other columns (Values)

    df_disc = pd.read_csv("model_1_predator-prey/Leigh1968_harelynx_rows_binarized.csv",
                          header=0, index_col=0)
    df_disc = df_disc.T

    features = ["Hares", "Lynxes"]
    for feature in features:
        plt.figure(figsize=(10, 6))
        ts = values[feature]
        ts = ts / max(ts)
        plt.plot(years, ts, label="raw {}".format(feature))
        plt.plot(years, df_disc[feature], label="discretized {}".format(feature))

        # Add labels and title
        plt.xlabel('Year')
        plt.ylabel('# of furs sold to Hudson Bay company')
        plt.title('Hudson Bay company {} dataset (1847 - 1903) raw vs discretized values'.format(feature))

        # Optional: Add a legend to indicate what each line represents
        plt.legend(loc='upper left')

        # Show the plot
        plt.grid(True)  # Optional: Add grid for better readability
        plt.show()
#visualize_lynx_hare_discrete()