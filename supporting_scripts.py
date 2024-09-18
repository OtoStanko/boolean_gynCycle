import re
from parameters import *
from variable_handler import Variable_handler
from equations import edes


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



with open("boolean_functions_latex.txt", "w") as boolfuncs_latex:
    for eq in edes:
        vh = Variable_handler(eq)
        vh.infer_boolean_function()
        print(vh.boolean_function_latex, file=boolfuncs_latex, end='\n\n')
        print(vh.name)


"""
# Example usage
num_vars = 3  # Number of input variables
output_column = [0, 1, 1, 0, 1, 0, 1, 0]  # Output column (example)
truth_table = generate_truth_table(num_vars, output_column)
boolean_function = infer_boolean_function(truth_table, num_vars)

print("Truth Table:")
for row in truth_table:
    print(row)

print("\nInferred Boolean Function (SOP):")
print(boolean_function)
"""

"""
with open("parameter_names.txt", "r") as f:
    with open("parameter_names_python.txt", "w") as of:
        for line in f:
            if line != "":
                new_name = variable_latex_to_python(line)
                print(new_name, file=of)
"""
