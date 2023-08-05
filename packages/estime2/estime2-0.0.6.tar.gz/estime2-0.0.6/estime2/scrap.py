
# from age import Age
# from config import (
#     get_option
# )
# from provpoptable import (
#     ProvPopTable,
#     calculate_ages_to_modify_and_counter
# )
from estime2 import (
    Age,
    get_option,
    options,
    ProvPopTable
)
from estime2.provpoptable import calculate_ages_to_modify_and_counter
from pprint import pprint
import numpy as np
import os
import pandas as pd
pd.options.display.max_rows = 15


def run():
    files_above = os.listdir('..')
    starts_with_G = list(map(lambda x: x[0] == 'G', files_above))
    tbl_name = np.array(files_above)[starts_with_G][0]
    tbl = pd.read_excel('../' + tbl_name, sheet_name = 1)
    poptbl = ProvPopTable(tbl)

    pop_age = 'Age'
    pop_end = 'Postcensal Population'
    comp = 'DTH'

    # Get basic options
    comp_neg = poptbl.get_comp_neg()
    comp_pos = poptbl.get_comp_pos()
    comps = comp_neg + comp_pos
    at_least = get_option('pop.at_least')
    pop_groups = ['Sex', 'Age']
    cols_required = pop_groups.copy()
    cols_required.append(comp)

    # Get properties of the youngest problematic record
    I = poptbl.get_I()
    I = I.query('I != 0').sort_values(pop_groups)
    problematic = I.iloc[0, :]
    problematic_sex = problematic['Sex']
    problematic_age = problematic['Age']
    problematic_val = problematic['I']
    calculated_pop = poptbl.calculate_pop()
    comp_in_neg = comp in comp_neg
    comp_in_comp_end = False
    age_is_max = problematic_age.is_max()
    
    # Get the corresponding age(s) of comp to modify & counter-adjust
    ages = calculate_ages_to_modify_and_counter(
        problematic_age,
        comp_in_comp_end
    )    
    to_modify_age = ages['age.to_modify']
    to_counter_age = ages['age.to_counter']

    # Get the maximum amounts modifiable & counter-adjustable
    correctable_in_comp = poptbl\
        .loc[lambda df: df['Sex'] == problematic_sex]\
        [cols_required]
    correctable_in_pop_end = calculated_pop.copy()\
        .loc[lambda df: df['Sex'] == problematic_sex]

    df_comp = correctable_in_comp.copy()
    df_pop_end = correctable_in_pop_end.copy()

    # calculate_modifiable_in_comp
    pop_end_query = None
    if age_is_max:
        pop_end_query = "{0} > {1}".format(pop_age, get_option('age.max'))
    else:
        pop_end_query = "{0} == {1}".format(pop_age, problematic_age)
    df_pop_end_problematic = df_pop_end.query(pop_end_query)
    df_comp_modifiable = None
    if isinstance(to_modify_age, int):
        df_comp_modifiable = df_comp\
            .loc[lambda df: df[pop_age] == to_modify_age]
    elif isinstance(to_modify_age, list):
        df_comp_modifiable = df_comp\
            .loc[lambda df: df[pop_age] <= to_modify_age[1]]\
            .loc[lambda df: df[pop_age] >= to_modify_age[0]]
    else:
        raise NotImplementedError

    # print('Problematic record:')
    # print(df_pop_end_problematic)
    # print('')
    # print('Component value to modify:')
    # print(df_comp_modifiable)

    modifiable_val_in_pop_end = df_pop_end_problematic[pop_end].values[0]
    abs_modifiable_val_in_pop_end = abs(modifiable_val_in_pop_end)
    modifiable = None
    if isinstance(to_modify_age, int):
        modifiable_val_in_comp = df_comp_modifiable[comp].values[0]
        if comp_in_neg:
            modifiable = min(
                abs_modifiable_val_in_pop_end,
                modifiable_val_in_comp
            )
        else:
            modifiable = abs_modifiable_val_in_pop_end
    elif isinstance(to_modify_age, list):
        modifiable_val_in_comp = df_comp_modifiable[comp]
        modifiable_val_in_comp_0 = modifiable_val_in_comp.values[0]
        modifiable_val_in_comp_1 = modifiable_val_in_comp.values[1]
        modifiable_0 = None
        modifiable_1 = None
        if comp_in_neg:
            modifiable_1 = min(
                abs_modifiable_val_in_pop_end, 
                modifiable_val_in_comp_1
            )
            modifiable_0 = None
            leftover = None
            if modifiable_1 == abs_modifiable_val_in_pop_end:
                modifiable_0 = 0
            else:
                leftover = abs_modifiable_val_in_pop_end -\
                    modifiable_val_in_comp_1
                modifiable_0 = min(leftover, modifiable_val_in_comp_0)
        else:
            modifiable_0 = abs_modifiable_val_in_pop_end // 2
            modifiable_1 = abs_modifiable_val_in_pop_end - modifiable_0
        modifiable = [modifiable_0, modifiable_1]
    else:
        raise NotImplementedError
    
    df_comp_modifiable["{0}_J".format(comp)] = modifiable
    del df_comp_modifiable[comp]

    # print('Component value modifiable:')
    # print(df_comp_modifiable)

    # calculate_counter_adjustable_in_comp
    modifiable_in_comp = df_comp_modifiable.copy()
    to_counter_age_min = to_counter_age[0]
    to_counter_age_max = to_counter_age[1]

    df_comp_counter_adjust = df_comp\
        .loc[lambda df: df[pop_age] >= to_counter_age_min]\
        .loc[lambda df: df[pop_age] <= to_counter_age_max]
    if comp_in_comp_end:
        df_pop_end_compare = df_pop_end\
            .loc[lambda df: df[pop_age] >= to_counter_age_min]\
            .loc[lambda df: df[pop_age] <= to_counter_age_max]
    else:
        df_pop_end_compare = df_pop_end\
            .loc[lambda df: df[pop_age] >= to_counter_age_min + 1]\
            .loc[lambda df: df[pop_age] <= to_counter_age_max + 1]
    df_pop_end_compare[pop_end] -= at_least

    pop_end_values = df_pop_end_compare[pop_end].values
    comp_values = df_comp_counter_adjust[comp].values
    counter_adjustable = []
    to_append = None

    for val in zip(pop_end_values, comp_values):
        if val[0] <= 0:
            to_append = 0
        elif comp_in_neg:
            to_append = val[0]
        else:
            to_append = val[1]
        counter_adjustable.append(to_append)

    df_comp_counter_adjust["{0}_J".format(comp)] = counter_adjustable
    del df_comp_counter_adjust[comp]

    # print("Component values counter-adjustable:")
    # print(df_comp_counter_adjust)
    df_comp_counter_adjust_reversed = df_comp_counter_adjust\
        .sort_values(pop_groups, ascending = [True, False])

    comp_J = "{0}_J".format(comp)
    comp_K = "{0}_K".format(comp)
    to_modify_val_total = df_comp_modifiable[comp_J].sum()
    # print('Total value to be modified:')
    # print(to_modify_val_total)

    result = []
    method = get_option('method')
    # print('Counter-adjustable records:')
    if method == '1dist':
        for index, row in df_comp_counter_adjust_reversed.iterrows():
            if row[comp_J] > 0 and to_modify_val_total != 0:
                result.append(1)
                to_modify_val_total -= 1
            else:
                result.append(0)
    else: # i.e. prop
        for index, row in df_comp_counter_adjust_reversed.iterrows():
            if row[comp_J] > 0 and to_modify_val_total != 0:
                min_comp_J_val = min(row[comp_J], to_modify_val_total)
                result.append(min_comp_J_val)
                to_modify_val_total -= min_comp_J_val
            else:
                result.append(0)

    df_comp_counter_adjust_reversed[comp_K] = result
    del df_comp_counter_adjust_reversed[comp_J]
    df_comp_counter_adjust_reversed\
        .sort_values(
            pop_groups, 
            ascending = [True, True], 
            inplace = True
        )

    comp_L = '{0}_L'.format(comp)
    J = df_comp_modifiable
    K = df_comp_counter_adjust_reversed

    if comp_in_neg:
        J[comp_L] = -J[comp_J]
        del J[comp_J]
        K[comp_L] = K[comp_K]
        del K[comp_K]
    else: # i.e. comp is positive
        J[comp_L] = J[comp_J]
        del J[comp_J]
        K[comp_L] = -K[comp_K]
        del K[comp_K]

    L = K.append(J, ignore_index = True)

    self_copy = poptbl.copy()
    self_copy = self_copy.merge(L, on = pop_groups, how = 'left')
    self_copy.fillna(0, inplace = True)
    self_copy[comp_L] = self_copy[comp_L].apply(int)
    self_copy[comp] += self_copy[comp_L]
    del self_copy[comp_L]

    self_copy = ProvPopTable(
        self_copy,
        pop_sex = 'Sex', # self.__pop_sex,
        pop_age = 'Age', # self.__pop_age,
        pop_end = 'Postcensal Population', # self.__pop_end,
        pop_start = 'Initial Population', # self.__pop_start,
        pop_birth = 'BTH', # self.__pop_birth,
        comp_neg_temp_out = get_option('comp_neg.temp_out'), # self.__comp_neg_temp_out,
        comp_neg_emi = get_option('comp_neg.emi'),
        comp_neg_npr_out = get_option('comp_neg.npr_out'),
        comp_neg_death = get_option('comp_neg.death'),
        comp_neg_interprov_out = get_option('comp_neg.interprov_out'),
        comp_pos_temp_in = get_option('comp_pos.temp_in'),
        comp_pos_ret_emi = get_option('comp_pos.ret_emi'),
        comp_pos_npr_in = get_option('comp_pos.npr_in'),
        comp_pos_immi = get_option('comp_pos.immi'),
        comp_pos_interprov_in = get_option('comp_pos.interprov_in'),
        comp_end = get_option('comp.end'),
        reorder_cols = False,
        show_pop_end = pop_end in poptbl.columns.tolist(), # self.columns.tolist(),
        flag = False        
    )

    print("self:")
    print(poptbl)
    print("self.calculate_pop():")
    self_calculate_pop = poptbl.calculate_pop()
    print(self_calculate_pop)
    print("Total end-of-period pop of self:")
    print(self_calculate_pop[pop_end].sum())
    print("self_copy after applying comp_L:")
    print(self_copy)
    print("self_copy.calculate_pop():")
    self_copy_calculate_pop = self_copy.calculate_pop()
    print(self_copy_calculate_pop)
    print("self_copy.get_I():")
    print(all(self_copy.get_I()['I'].values == 0))
    print("Total end-of-period pop of self_copy:")
    print(self_copy_calculate_pop[pop_end].sum())

    print('poptbl.fix_issues():')
    result = poptbl.fix_issues()
    print(result.calculate_pop())

    # test = Age('99+')
    # print(str(test)[-1] == '+')
    # print(Age(102).get_showing_age())

    # pop_groups = ['Sex', 'Age']
    # pop_end = 'Postcensal Population'
    # pop_start = 'Initial Population'
    # pop_birth = 'BTH'
    # comp_neg = ['TEM', 'EMI', 'NPR, 2018-07-01', 'DTH', 'IOM']
    # comp_pos = ['RE', 'NPR, 2019-07-01' ,'IMM', 'IIM']
    # comps = comp_neg + comp_pos
    # comp_end = ['NPR, 2019-07-01']
    # comp_not_end = []
    # for comp in comps:
    #     if comp not in comp_end:
    #         comp_not_end.append(comp)
    # comp_aggs = {}
    # comp_aggs[pop_start] = 'sum'
    # comp_aggs[pop_birth] = 'sum'
    # for comp2 in comp_not_end:
    #     comp_aggs[comp2] = 'sum'

    # result1 = poptbl.loc[
    #     :, 
    #     pop_groups + [pop_start, pop_birth] + comp_not_end
    # ]
    # result1['Age'] += 1
    # result1 = result1\
    #     .groupby(pop_groups)\
    #     .agg(comp_aggs)\
    #     .reset_index()

    # result2 = poptbl.loc[:, pop_groups + comp_end]
    # result2 = result2.loc[lambda df: df['Age'] != -1]

    # result3 = result1\
    #     .merge(
    #         result2, 
    #         how = 'left', 
    #         on = ['Sex', 'Age']
    #     )
    
    # result3[pop_end] = result3[pop_start] + result3[pop_birth]
    # if comp_neg != []:
    #     for col_neg in comp_neg:
    #         result3[pop_end] -= result3[col_neg]
    # if comp_pos != []:
    #     for col_pos in comp_pos:
    #         result3[pop_end] += result3[col_pos]

    # result = result3.loc[:, pop_groups + [pop_end]]

    # pop_end =\
    #     poptbl['Initial Population'] + poptbl['BTH']\
    #         - poptbl['TEM'] - poptbl['EMI'] - poptbl['NPR, 2018-07-01']\
    #         - poptbl['DTH'] - poptbl['IOM'] - poptbl['RAO']\
    #         + poptbl['RE'] + poptbl['NPR, 2019-07-01'] + poptbl['IMM']\
    #         + poptbl['IIM'] + poptbl['RAI']
    # pop_grp = poptbl.loc[:, ['Sex', 'Age']]
    # pop_grp['Age'] += 1
    # pop_grp['End-of-period population'] = pop_end
    # result = poptbl\
    #     .groupby(['Sex', 'Age'])\
    #     .agg({
    #         'Initial Population': 'sum',
    #         'BTH': 'sum',
    #         'TEM': 'sum',
    #         'EMI': 'sum',
    #         'NPR, 2018-07-01': 'sum',
    #         'DTH': 'sum',
    #         'IOM': 'sum',
    #         'RAO': 'sum',
    #         'RE': 'sum',
    #         'NPR, 2019-07-01': 'sum',
    #         'IMM': 'sum',
    #         'IIM': 'sum',
    #         'RAI': 'sum'
    #     })\
    #     .reset_index()
    # print(pop_grp)
    # print(result)
    # print(poptbl.calculate_pop())
    # print(poptbl.loc[lambda df: df['Age'] >= '99+'])
    # template =\
    #     '* `{arg_name}`: (`None` by default) a str; the name of ' +\
    #     'the column corresponding to "{real_name}" in the ' +\
    #     'population table. If `None`, it first checks whether the ' +\
    #     'global option value `{glob_name}` is also `None`. If it ' +\
    #     'is also `None`, the "{real_name}" component is ' +\
    #     'discarded from the population table (i.e. not shown and not ' +\
    #     'used). If it is not `None`, the method then checks whether the ' +\
    #     'value `{glob_name}` is one of the column names in the ' +\
    #     'population table. If it is, the column having the same name as ' +\
    #     '`{glob_name}` is selected as the ' +\
    #     '"{real_name}" column. If not, the method raises ' +\
    #     '`AssertionError`.'
    # print(
    #     template.format(
    #         arg_name = 'comp_pos_npr_in',
    #         real_name = 'Non-permanent residents IN',
    #         glob_name = 'comp_pos.npr_in'
    #     )
    # )
    # print(
    #     template.format(
    #         arg_name = 'comp_pos_immi',
    #         real_name = 'Immigrants',
    #         glob_name = 'comp_pos.immi'
    #     )
    # )
    # print(
    #     template.format(
    #         arg_name = 'comp_pos_interprov_in',
    #         real_name = 'Interprovincial migrant IN',
    #         glob_name = 'comp_pos.interprov_in'
    #     )
    # )

def run2():

    method = get_option('method')

    files_above = os.listdir('..')
    starts_with_G = list(map(lambda x: x[0] == 'G', files_above))
    tbl_name = np.array(files_above)[starts_with_G][0]
    tbl = pd.read_excel('../' + tbl_name, sheet_name = 1)
    self = ProvPopTable(tbl)

    comp_neg_to_use = self.get_comp_neg()
    comp_pos_to_use = self.get_comp_pos()
    comp_neg_to_use.remove(get_option('comp_neg.interprov_out'))
    comp_pos_to_use.remove(get_option('comp_pos.interprov_in'))
    comps = comp_neg_to_use + comp_pos_to_use

    pop_groups = [get_option('pop.sex'), get_option('pop.age')]
    all_cols = self.columns.tolist()
    show_pop_end = get_option('pop.end') in all_cols
    self_copy = self.copy()

    not_fixed = True
    i = 0
    while not_fixed:
        comp = comps[i]; print(comp)
        i += 1

        comp_L = '{0}_L'.format(comp)
        if i == 1:
            self_copy = ProvPopTable(
                self_copy,
                pop_sex = 'Sex', 
                pop_age = 'Age',
                pop_end = 'Postcensal Population',
                pop_start = 'Initial Population',
                pop_birth = 'BTH',
                comp_neg_temp_out = get_option('comp_neg.temp_out'),
                comp_neg_emi = get_option('comp_neg.emi'),
                comp_neg_npr_out = get_option('comp_neg.npr_out'),
                comp_neg_death = get_option('comp_neg.death'),
                comp_neg_interprov_out = get_option('comp_neg.interprov_out'),
                comp_pos_temp_in = get_option('comp_pos.temp_in'),
                comp_pos_ret_emi = get_option('comp_pos.ret_emi'),
                comp_pos_npr_in = get_option('comp_pos.npr_in'),
                comp_pos_immi = get_option('comp_pos.immi'),
                comp_pos_interprov_in = get_option('comp_pos.interprov_in'),
                comp_end = get_option('comp.end'),
                reorder_cols = False,
                show_pop_end = show_pop_end,
                flag = False  
            )
        L = self_copy.get_L(comp, method); 
        L['Age'] = L['Age'].apply(str); print(L)
        self_copy['Age'] = self_copy['Age'].apply(str)
        self_copy = self_copy.merge(L, on = pop_groups, how = 'left')
        self_copy.fillna(0, inplace = True)
        self_copy[comp_L] = self_copy[comp_L].apply(int)

        print('Before adding:')
        print(self_copy)
        
        self_copy[comp] += self_copy[comp_L]

        print('After adding, before deleting comp_L:')
        print(self_copy)
        
        del self_copy[comp_L]

        print('After adding, after deleting comp_L:')
        print(self_copy)

        self_copy = ProvPopTable(
            self_copy,
            pop_sex = 'Sex', 
            pop_age = 'Age',
            pop_end = 'Postcensal Population',
            pop_start = 'Initial Population',
            pop_birth = 'BTH',
            comp_neg_temp_out = get_option('comp_neg.temp_out'),
            comp_neg_emi = get_option('comp_neg.emi'),
            comp_neg_npr_out = get_option('comp_neg.npr_out'),
            comp_neg_death = get_option('comp_neg.death'),
            comp_neg_interprov_out = get_option('comp_neg.interprov_out'),
            comp_pos_temp_in = get_option('comp_pos.temp_in'),
            comp_pos_ret_emi = get_option('comp_pos.ret_emi'),
            comp_pos_npr_in = get_option('comp_pos.npr_in'),
            comp_pos_immi = get_option('comp_pos.immi'),
            comp_pos_interprov_in = get_option('comp_pos.interprov_in'),
            comp_end = get_option('comp.end'),
            reorder_cols = False,
            show_pop_end = show_pop_end,
            flag = False  
        )

        not_fixed = not (all(self_copy.get_I()['I'].values == 0) or i == len(comps))


    print(self_copy)

def run3():
    files_above = os.listdir('..')
    starts_with_G = list(map(lambda x: x[0] == 'G', files_above))
    tbl_name = np.array(files_above)[starts_with_G][0]
    tbl = pd.read_excel('../' + tbl_name, sheet_name = 1)
    poptbl = ProvPopTable(tbl)
    print(poptbl)
    print(poptbl.calculate_pop())

    result = poptbl.fix_issues(return_all_mods = True)
    pprint(result)
    try:
        print(result.calculate_pop())
    except:
        print(result[0].calculate_pop())
    # return result
