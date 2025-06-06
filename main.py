import os

from supporting_scripts import *

wc = os.getcwd()


"""
**********************************
    Predator-prey model inference
**********************************
"""
pp_model = os.path.join(wc, "model_1_predator-prey")
ode_file_pp = os.path.join(pp_model, "predator-prey_ODE_model.dode")
sim_raw_pp = os.path.join(pp_model, "predator_prey_ODE_sim_columns.csv")

"""
BoolNet
"""
def pp_boolnet():
    print("Running function: pp_boolnet")
    raw_ts = os.path.join(pp_model, "predator_prey_ODE_sim_rows.csv")
    bin_ts = os.path.join(pp_model, "predator_prey_ODE_sim_rows_binarized.csv")
    bin_ts = os.path.join(pp_model, "Leigh1968_harelynx_rows_binarized.csv")
    bin_ts_simple = os.path.join(pp_model,
                                 "Leigh1968_harelynx_rows_binarized_simplified.csv")
    simplify_TS(None, bin_ts, None, bin_ts_simple)
#pp_boolnet()


"""
euler-like transformation
"""
def pp_eulerlike_transform():
    print("Running function: pp_eulerlike_transform")
    aeon_file_pp = os.path.join(pp_model,
                                "euler-like_transformation",
                                "predator-prey_model.aeon")
    ode_eulerlike_transform_to_aeon(ode_file_pp, aeon_file_pp)
#pp_eulerlike_transform()


"""
SAILoR inference from time series and prior networks
"""
def pp_sailor():
    sailor_pp_model_path = os.path.join(pp_model, "SAILoR")
    print("Running function: pp_sailor")
    from SAILoR.SAILoR import ContextSpecificDecoder

    #ode_system_pp = ODESystem(ode_file_pp)
    #ode_system_pp.to_network(prior_network_predator_prey)
    prior_networks_pp = [os.path.join(sailor_pp_model_path, "prior_networks", "prior_network_pp_{:02d}.tsv".format(i))
                         for i in range(1, 16)]

    lynxhare_raw = os.path.join(pp_model, "Leigh1968_harelynx_columns_tabs.csv")
    lynxhare_bin_simplified = os.path.join(pp_model, "Leigh1968_harelynx_columns_binarized_simplified_SAILoR.tsv")

    decoder_simDataset = ContextSpecificDecoder(timeSeriesPath=lynxhare_raw,
                                                referenceNetPaths=prior_networks_pp)
    best = decoder_simDataset.run()
    boolean_expressions = []
    for bfun in best:
        boolean_expressions.append(bfun[4])
    SAILoR_to_aeon(boolean_expressions, os.path.join(sailor_pp_model_path, "predator-prey_hudsonBayDataset.aeon"))

    decoder_simDataset = ContextSpecificDecoder(timeSeriesPath=lynxhare_raw,
                                                referenceNetPaths=prior_networks_pp, binarisedPath=lynxhare_bin_simplified)
    best = decoder_simDataset.run()
    boolean_expressions = []
    for bfun in best:
        boolean_expressions.append(bfun[4])
    SAILoR_to_aeon(boolean_expressions,
                   os.path.join(sailor_pp_model_path, "predator-prey_hudsonBayDataset_binarised.aeon"))

    sim_bin_pp = os.path.join(pp_model, "predator_prey_ODE_sim_columns_binarised_simplified_SAILoR.tsv")
    decoder_simDataset = ContextSpecificDecoder(timeSeriesPath=sim_raw_pp,
                                                referenceNetPaths=prior_networks_pp)
    best = decoder_simDataset.run()
    boolean_expressions = []
    for bfun in best:
        boolean_expressions.append(bfun[4])
    SAILoR_to_aeon(boolean_expressions, os.path.join(sailor_pp_model_path, "predator-prey_simDataset.aeon"))

    decoder_simDataset = ContextSpecificDecoder(timeSeriesPath=sim_raw_pp,
                                                referenceNetPaths=prior_networks_pp, binarisedPath=sim_bin_pp)
    best = decoder_simDataset.run()
    boolean_expressions = []
    for bfun in best:
        boolean_expressions.append(bfun[4])
    SAILoR_to_aeon(boolean_expressions, os.path.join(sailor_pp_model_path, "predator-prey_simDataset_binarised.aeon"))
#pp_sailor()


"""
**********************************
    Bovine-estrous cycle inference
**********************************
"""
be_model = os.path.join(wc, "model_2_bovine-estrous")
ode_file_be = os.path.join(be_model, "bovine-estrous-cycle_ODE_model.dode")
sim_raw_be = os.path.join(be_model, "bov_cycle_ODE_sim_columns.csv")


"""
BoolNet
"""
#ode_system_gc = ODESystem(ode_file_be)
#print(ode_system_gc.get_requiredDependencies())
def be_boolnet():
    print("Running function: be_boolnet")
    raw_ts = os.path.join(be_model, "bov_cycle_ODE_sim_rows.csv")
    bin_ts = os.path.join(be_model, "bov_cycle_ODE_sim_rows_binarized.csv")
    bin_ts_simple = os.path.join(be_model,
                                 "bov_cycle_ODE_sim_rows_binarized_simplified_auto.csv")
    simplify_TS(None, bin_ts, None, bin_ts_simple)
#be_boolnet()


"""
euler-like transformation
"""
def be_eulerlike_transform():
    print("Running function: be_eulerlike_transform")
    aeon_file_be = os.path.join(be_model,
                                "euler-like_transformation",
                                "bovine-estrous-cycle_model.aeon")
    ode_eulerlike_transform_to_aeon(ode_file_be, aeon_file_be)


"""
SAILoR inference from time series and prior networks
"""
def be_sailor():
    print("Running function: be_sailor")
    from SAILoR.SAILoR import ContextSpecificDecoder

    prior_network_bovine_estrous = os.path.join(be_model, "SAILoR", "prior_networks", "prior_network_be.tsv")
    ode_system_pp = ODESystem(ode_file_be)
    ode_system_pp.to_network(prior_network_bovine_estrous)

    sim_bin_be = os.path.join(be_model, "bov_cycle_ODE_sim_columns_binarized_simplified_auto_SAILoR.tsv")
    decoder = ContextSpecificDecoder(timeSeriesPath=sim_raw_be,
                                     referenceNetPaths=[prior_network_bovine_estrous],
                                     binarisedPath=sim_bin_be)
    print(decoder)
    best = decoder.run()

    boolean_expressions = []
    for bfun in best:
        boolean_expressions.append(bfun[4])
    print(boolean_expressions)
    SAILoR_to_aeon(boolean_expressions, os.path.join(be_model, "SAILoR", "bovine-estrous_model_binarised.aeon"))
#be_sailor()


"""
**********************************
    Gyn cycle inference
**********************************
"""
gc_model = os.path.join(wc, "model_3_gyn-cycle")
ode_file_gc = os.path.join(gc_model, "gyn-cycle_ODE_model.dode")
sim_raw_gc = os.path.join(gc_model, "copasi_sim_columns.csv")


"""
BoolNet
"""
#ode_system_gc = ODESystem(ode_file_gc)
#print(ode_system_gc.get_requiredDependencies())
def gc_preprocess():
    print("Running function: gc_preprocess")
    sim_raw_gc_rows = os.path.join(gc_model, "gyn_cycle_sim_rows.csv")
    raw_ts = pd.read_csv(sim_raw_gc, delimiter='\t')
    raw_ts = raw_ts.T
    rows_to_drop = ['Ant_c', 'Ago_R_i', 'Ago_R_a', 'Ant_p', 'Ant_d',
                    'Ago_d', 'Ago_c', 'Ant_R', ]
    for row_to_drop in rows_to_drop:
        raw_ts = raw_ts.drop(index=row_to_drop)
    raw_ts = raw_ts.iloc[1:]
    raw_ts.to_csv(sim_raw_gc_rows)


def gc_boolnet():
    print("Running function: gc_boolnet")
    bin_ts = os.path.join(gc_model, "bov_cycle_ODE_sim_rows_binarized.csv")
    bin_ts_simple = os.path.join(gc_model, "bov_cycle_ODE_sim_rows_binarized_simplified_auto.csv")
    simplify_TS(None, bin_ts, None, bin_ts_simple)
#gc_boolnet()


"""
euler-like transformation
"""
def gc_eulerlike_transform():
    print("Running function: gc_eulerlike_transform")
    aeon_file_gc = os.path.join(gc_model,
                                "euler-like_transformation",
                                "gyn-cycle_model_fixedNames.aeon")
    ode_eulerlike_transform_to_aeon(ode_file_gc, aeon_file_gc)
#gc_eulerlike_transform()


"""
SAILoR inference from time series and prior networks
"""
def gc_sailor():
    print("Running function: gc_sailor")
    from SAILoR.SAILoR import ContextSpecificDecoder
    prior_network_gyn_cycle = os.path.join(gc_model, "SAILoR", "prior_networks", "prior_network_gc.tsv")
    ode_system_gc = ODESystem(ode_file_gc)
    ode_system_gc.to_network(prior_network_gyn_cycle)

    sim_raw_gc_columns = os.path.join(gc_model, "gyn_cycle_sim_columns.csv")
    sim_bin_gc = os.path.join(gc_model, "gyn_cycle_sim_columns_binarized_simplified_auto_SAILoR.tsv")
    decoder = ContextSpecificDecoder(timeSeriesPath=sim_raw_gc_columns,
                                     referenceNetPaths=[prior_network_gyn_cycle, prior_network_gyn_cycle, prior_network_gyn_cycle,
                                                        prior_network_gyn_cycle, prior_network_gyn_cycle, prior_network_gyn_cycle],
                                     binarisedPath=sim_bin_gc)
    print(decoder)
    best = decoder.run()

    boolean_expressions = []
    for bfun in best:
        boolean_expressions.append(bfun[4])
    print(boolean_expressions)
    SAILoR_to_aeon(boolean_expressions, os.path.join(gc_model, "SAILoR", "gyn-cycle_model.aeon"))
#gc_sailor()


def gc_sketchbook():
    print("Running function: gc_sketchbook")
    sb = os.path.join(gc_model, "SketchBook")
    cycles, head = find_first_cycle(os.path.join(gc_model, "gyn_cycle_sim_columns_binarized_simplified_auto.csv"))
    cycles_intersect = cycles[0]
    for i in range(1, len(cycles)):
        cycles_intersect = [val for val in cycles_intersect if val in cycles[i]]
    cycles_intersect.append(cycles_intersect[0])
    trs = create_formulae_for_SketchBook_transitions(cycles_intersect, head)
    for i in trs:
        print(i)

    print()
    cycles, head = find_first_cycle(
        os.path.join(sb, "LH_submodel", "gyn_cycle_sim_columns_binarized_simplified_LH.csv"))
    cycles_intersect = cycles[0]
    for i in range(1, len(cycles)):
        cycles_intersect = [val for val in cycles_intersect if val in cycles[i]]
    cycles_intersect.append(cycles_intersect[0])
    trs = create_formulae_for_SketchBook_transitions(cycles_intersect, head)
    for i in trs:
        print(i)

    print()
    cycles, head = find_first_cycle(
        os.path.join(sb, "FSH_submodel", "gyn_cycle_sim_columns_binarized_simplified_FSH.csv"))
    cycles_intersect = cycles[0]
    for i in range(1, len(cycles)):
        cycles_intersect = [val for val in cycles_intersect if val in cycles[i]]
    cycles_intersect.append(cycles_intersect[0])
    trs = create_formulae_for_SketchBook_transitions(cycles_intersect, head)
    for i in trs:
        print(i)

    print()
    cycles, head = find_first_cycle(
        os.path.join(sb, "GnRH_submodel", "gyn_cycle_sim_columns_binarized_simplified_GnRH.csv"))
    cycles_intersect = cycles[0]
    for i in range(1, len(cycles)):
        cycles_intersect = [val for val in cycles_intersect if val in cycles[i]]
    cycles_intersect.append(cycles_intersect[0])
    trs = create_formulae_for_SketchBook_transitions(cycles_intersect, head)
    for i in trs:
        print(i)
gc_sketchbook()

#gc_bin_ts = os.path.join(gc_model, "gyn_cycle_sim_rows_red_binarized.csv")
#gc_bin_ts_simple = os.path.join(gc_model, "gyn_cycle_sim_rows_red_binarized_simplified.csv")
#simplify_TS(None, gc_bin_ts, None, gc_bin_ts_simple)
#ode_system_gc = ODESystem(ode_file_gc)
#print(ode_system_gc)