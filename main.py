import os

from supporting_scripts import *

wc = os.getcwd()


"""**********************************
    Predator-prey model abstractions
**********************************"""
pp_model = os.path.join(wc, "predator-prey_model")
ode_file_pp = os.path.join(pp_model, "predator-prey_ODE_model.dode")
sim_raw_pp = os.path.join(pp_model, "predator_prey_ODE_sim_results.csv")

"""
euler-like transformation from .ode file to .aeon file
""" 
def pp_eulerlike_transform():
    aeon_file_pp = os.path.join(pp_model,
                                "euler-like_transformation",
                                "predator-prey_model.aeon")
    ode_eulerlike_transform_to_aeon(ode_file_pp, aeon_file_pp)


"""
SAILoR inference from time series and prior networks
"""
def pp_sailor():
    from SAILoR.SAILoR import ContextSpecificDecoder

    prior_network_predator_prey = os.path.join(pp_model, "prior_network_pp.tsv")
    ode_system_pp = ODESystem(ode_file_pp)
    ode_system_pp.to_network(prior_network_predator_prey)

    decoder = ContextSpecificDecoder(timeSeriesPath=sim_raw_pp,
                                     referenceNetPaths=[prior_network_predator_prey])
    print(decoder)
    best = decoder.run()

    boolean_expressions = []
    for bfun in best:
        boolean_expressions.append(bfun[4])
    print(boolean_expressions)
    SAILoR_to_aeon(boolean_expressions, os.path.join(pp_model, "SAILoR", "gyn-cycle_model.aeon"))


"""
BoolNet
"""
def pp_boolnet():
    raw_ts = os.path.join(pp_model, "predator_prey_ODE_sim_results_rows.csv")
    bin_ts = os.path.join(pp_model, "predator_prey_ODE_sim_binarized_k_means.csv")
    bin_ts_simple = os.path.join(pp_model,
                                 "predator_prey_ODE_sim_binarized_k_means_simplified_auto.csv")
    simplify_TS(None, bin_ts, None, bin_ts_simple)


"""**********************************
    Bovine-estrous cycle abstractions
**********************************"""
be_model = os.path.join(wc, "bovine-estrous_model")
ode_file_be = os.path.join(be_model, "bovine-estrous-cycle_ODE_model.dode")

"""
euler-like transformation from .ode file to .aeon file
"""
def be_eulerlike_transform():
    aeon_file_be = os.path.join(be_model,
                                "euler-like_transformation",
                                "bovine-estrous-cycle_model.aeon")
    ode_eulerlike_transform_to_aeon(ode_file_be, aeon_file_be)


"""**********************************
    Gyn cycle abstractions
**********************************"""
gc_model = os.path.join(wc, "gyn-cycle_model")
ode_file_gc = os.path.join(gc_model, "gyn-cycle_ODE_model.dode")
sim_raw_gc = os.path.join(gc_model, "copasi_simulation_100d.csv")

"""
euler-like transformation from .ode file to .aeon file
"""
def gc_eulerlike_transform():
    aeon_file_gc = os.path.join(gc_model,
                                "euler-like_transformation",
                                "gyn-cycle_model.aeon")
    ode_eulerlike_transform_to_aeon(ode_file_gc, aeon_file_gc)


"""
SAILoR inference from time series and prior networks
"""
def gc_sailor():
    from SAILoR.SAILoR import ContextSpecificDecoder
    prior_network_gyn_cycle = os.path.join(gc_model, "prior_network_gc.csv")
    ode_system_gc = ODESystem(ode_file_gc)
    ode_system_gc.to_network(prior_network_gyn_cycle)

    decoder = ContextSpecificDecoder(timeSeriesPath=sim_raw_gc,
                                     referenceNetPaths=[prior_network_gyn_cycle, prior_network_gyn_cycle, prior_network_gyn_cycle,
                                                        prior_network_gyn_cycle, prior_network_gyn_cycle, prior_network_gyn_cycle])
    print(decoder)
    best = decoder.run()

    boolean_expressions = []
    for bfun in best:
        boolean_expressions.append(bfun[4])
    print(boolean_expressions)
    SAILoR_to_aeon(boolean_expressions, os.path.join(gc_model, "SAILoR", "gyn-cycle_model.aeon"))


"""
BoolNet
"""
#ode_system_gc = ODESystem(ode_file_gc)
#print(ode_system_gc.get_requiredDependencies())
def gc_preprocess():
    sim_raw_gc_rows = os.path.join(gc_model, "gyn-cycle_sim_rows.csv")
    raw_ts = pd.read_csv(sim_raw_gc, delimiter='\t')
    raw_ts = raw_ts.T
    rows_to_drop = ['Ant_c', 'Ago_R_i', 'Ago_R_a', 'Ant_p', 'Ant_d',
                    'Ago_d', 'Ago_c', 'Ant_R', ]
    for row_to_drop in rows_to_drop:
        raw_ts = raw_ts.drop(index=row_to_drop)
    raw_ts = raw_ts.iloc[1:]
    raw_ts.to_csv(sim_raw_gc_rows)


def gc_boolnet():
    bin_ts = os.path.join(gc_model, "simulation_binarized_rows.csv")
    bin_ts_simple = os.path.join(gc_model, "simulation_binarized_rows_simplified_auto.csv")
    simplify_TS(None, bin_ts, None, bin_ts_simple)
#gc_boolnet()


"""
Augusta
"""
def gc_augusta():
    from Augusta.Augusta import RNASeq_to_BN
    df = pd.read_csv(sim_raw_gc, delimiter='\t')
    df = df.T
    df = df.iloc[1:]
    rows_to_drop = ['Ant_c', 'Ago_R_i', 'Ago_R_a','Ant_p','Ant_d',
                    'Ago_d', 'Ago_c', 'Ant_R', ]
    for row_to_drop in rows_to_drop:
        df = df.drop(index=row_to_drop)
    df = df * 10
    print(df.index)
    print(df)
    df.to_csv('output.csv', sep=';')
    RNASeq_to_BN(count_table_input = 'output.csv')


