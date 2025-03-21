import os

from biodivine_aeon import *

from supporting_scripts import create_formula_for_path, find_first_cycle

be_model = os.path.join(os.getcwd(), "model_2_bovine-estrous")
boolnet_be_model_path_full_const = os.path.join(be_model, "BoolNet", "bovine-estrous_full_constraints_colored_edges.aeon")
boolnet_be_model_path_maxK4 = os.path.join(be_model, "BoolNet", "bovine-estrous_maxK4_colored_edges.aeon")
euler_like_automated_be_model_path = os.path.join(be_model, "euler-like_transformation", "bovine-estrous-cycle_model_colored_edges.aeon")
sailor_be_model_path = os.path.join(be_model, "SAILoR", "colored_bovine-estrous_model_binarised.aeon")
sketchBook_be_model_path = os.path.join(be_model, "SketchBook", "candidate_1.aeon")
sketchBook_be_model_path_2 = os.path.join(be_model, "SketchBook", "candidate_2.aeon")
be_model_paths = [boolnet_be_model_path_full_const, boolnet_be_model_path_maxK4,
                  euler_like_automated_be_model_path,
                  sailor_be_model_path, sketchBook_be_model_path,
                  sketchBook_be_model_path_2]


cycles, head = find_first_cycle(os.path.join(be_model, "bov_cycle_ODE_sim_columns_binarized_simplified_auto.csv"))
print([len(cycle) for cycle in cycles])
cycles_intersect = cycles[0]
for i in range(1, len(cycles)):
    cycles_intersect = [val for val in cycles_intersect if val in cycles[i]]
cycles_intersect.append(cycles_intersect[0])
print(len(cycles_intersect))
path_formula_ef, basic_transitions_ef = create_formula_for_path(cycles_intersect, head, on_non_triv_att=False)

msg_ok = ">OK"
msg_nok = ">FAIL"


models_results = dict()
for model_path in be_model_paths:
    print()
    print(len(model_path) * "*")
    print(model_path)
    print(len(model_path) * "*")
    model = BooleanNetwork.from_file(model_path, repair_graph=True)

    print("\nModel update functions")
    for v in model.variables():
        print(model.get_variable_name(v), "=", model.get_update_function(v))
    print("\nModel regulations")
    for regulation in model.regulations():
        print(regulation)

    stg = AsynchronousGraph.mk_for_model_checking(model, 6)
    attractors = Attractors.attractors(stg)
    print("\nModel attractors ({})".format(len(attractors)))
    print(attractors)
    results_classes = []
    for attractor in attractors:
        print(">")
        print("Attractor cardinality:", attractor.cardinality())
        print("Attractor vertices:", attractor.vertices())
        classes = Classification.classify_long_term_behavior(stg, attractor)
        results_classes.append(classes)
        print("class:", classes)

    print("\nPeriodic behaviour analysis:")

    results_ef_ok = 0
    results_ef_nok = 0
    result_ef_whole = False
    result_ovul_pattern = False
    result_ovul_att = False
    print("\nResult of EF path for bovine estrous cycle:")
    for attractor in attractors:
        stg_att = stg.restrict(attractor)
        classes = Classification.classify_long_term_behavior(stg, attractor)
        print("\n***********")
        print("class:", classes)
        cls_keys = list(classes.keys())
        if Class(["disorder"]) not in cls_keys:
            continue
        print(attractor.vertices())
        print_buffer = "\n"
        print_at_the_end = False
        for partial_transition in basic_transitions_ef:
            print_buffer += partial_transition + "\n"
            attractor_mc = ModelChecking.verify(stg_att, partial_transition)
            print_buffer += str(attractor_mc) + "\n"
            if attractor_mc.cardinality() > 0:
                results_ef_ok += 1
                print_at_the_end = True
                print_buffer += msg_ok + "\n"
            else:
                results_ef_nok += 1
                print_buffer += msg_nok + "\n"
        print_buffer += path_formula_ef + "\n"
        attractors_mc = ModelChecking.verify(stg_att, path_formula_ef)
        print_buffer += str(attractors_mc) + "\n"
        if attractors_mc.cardinality() > 0:
            result_ef_whole = True
            print_buffer += msg_ok + "\n"
        else:
            print_buffer += msg_nok + "\n"
        print_buffer += "Existence of a cycle that includes key ovulation hormonal pattern:\n"
        #print("Existence of a cycle that includes key ovulation hormonal pattern:")
        ovulation_behaviour = "!{x}: (Foll & EF (E2 & Inh & Foll & EF (E2 & LH & ~P4 & Inh & ~CL & EF (~LH & ~P4 & CL & EF (~E2 & ~LH & P4 & ~Inh & ~Foll & CL & (EF {x}))))))"
        #print(ovulation_behaviour)
        print_buffer += ovulation_behaviour + "\n"
        attractors_mc = ModelChecking.verify(stg_att, ovulation_behaviour)
        #print(attractors_mc)
        print_buffer += str(attractors_mc) + "\n"
        if attractors_mc.cardinality() > 0:
            result_ovul_pattern = True
            print_at_the_end = True
        ovul_att = "!{x}: (AG EF {x} & AX ~{x} & (Foll & EF (E2 & Inh & Foll & EF (E2 & LH & ~P4 & Inh & ~CL & EF (~LH & ~P4 & CL & EF (~E2 & ~LH & P4 & ~Inh & ~Foll & CL & (EF {x})))))))"
        attractors_mc = ModelChecking.verify(stg_att, ovul_att)
        #print(attractors_mc.colors(), attractors_mc.vertices())
        print_buffer += str(attractors_mc.colors()) + " " + str(attractors_mc.vertices()) + "\n"
        if attractors_mc.cardinality() > 0:
            result_ovul_att = True
            print_at_the_end = True
        if print_at_the_end:
            print(print_buffer)

    model_info = model_path.split(os.sep)
    method = model_info[-2]
    model = model_info[-1]
    models_results[(method, model)] = [results_classes,
                                       str(results_ef_ok) + "/" + str(results_ef_ok + results_ef_nok),
                                       result_ef_whole, result_ovul_pattern, result_ovul_att]

for model_results in models_results.items():
    print(model_results)