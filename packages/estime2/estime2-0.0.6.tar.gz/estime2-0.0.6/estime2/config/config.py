
from collections import namedtuple
from estime2.helper import raise_if_not_subset
import re



RegisteredOption = namedtuple(
    "RegisteredOption", 
    "key defval doc validator"
)
age_down_to = 40
age_max = 99
comp_neg_temp_out = 'TEM'
comp_neg_emi = 'EMI'
comp_neg_npr_out = 'NPR, 2018-07-01'
comp_neg_death = 'DTH'
comp_neg_interprov_out = 'IOM'
comp_neg_intraprov_out = 'RAO'
comp_pos_temp_in = None
comp_pos_ret_emi = 'RE'
comp_pos_npr_in = 'NPR, 2019-07-01'
comp_pos_immi = 'IMM'
comp_pos_interprov_in = 'IIM'
comp_pos_intraprov_in = 'RAI'
comp_end = [comp_pos_npr_in]
method_all = ['1dist', 'prop']
method = '1dist'
pop_age = 'Age'
pop_birth = 'BTH'
pop_at_least = 1
pop_end = 'Postcensal Population'
pop_sex = 'Sex'
pop_start = 'Initial Population'



def is_int(x, opname):
    if not isinstance(x, int):
        type_x = type(x)
        raise TypeError(f"{opname} must be an int, not of {type_x}.")
    return None

def is_str(x, opname, can_be_None = True):
    if x is None:
        if can_be_None:
            return None
        else:
            msg = "{0} cannot be None; it must be a str."
            msg = msg.format(opname)
            raise TypeError(msg)
    if not isinstance(x, str):
        msg = "{0} must be a str, not of {1}."
        msg = msg.format(opname, type(x))
        raise TypeError(msg)
    return None

def is_length_n(x, opname, n):
    if len(x) != n:
        msg = "{0} must be of length {1}, not {2}."\
            .format(opname, n, len(x))
        raise ValueError(msg)
    return None

def is_list_int_ordered(x):
    if not isinstance(x, list):
        msg1 = "age.interval must be a list, not of type {}."
        raise TypeError(msg1.format(type(x)))
    is_length_n(x, 'age.interval', 2)
    if x != sorted(x):
        msg3 = "age.interval must be ordered."
        raise ValueError(msg3)
    if not isinstance(x[0], int):
        msg4_1 = "The lower bound must be of type int, not {}."
        raise ValueError(msg4_1.format(type(x[0])))
    if not isinstance(x[1], int):
        msg4_2 = "The upper bound must be of type int, not {}."
        raise ValueError(msg4_2.format(type(x[1])))
    if x[0] > 0:
        msg5_1 =\
            "The lower bound of age.interval must be nonpositive, " +\
            "but the current value is {}."
        raise ValueError(msg5_1.format(x[0]))
    if x[1] < 0:
        msg5_2 =\
            "The upper bound of age.interval must be nonnegative, " +\
            "but the current value is {}."
        raise ValueError(msg5_2.format(x[1]))
    return None

def is_list_str(x, opname, n = None):
    if not isinstance(x, list):
        msg1 =\
            "{0} must be a list, not of {1}."\
            .format(opname, type(x))
        raise TypeError(msg1)
    if x == []:
        msg2 = "{0} must not be an empty list.".format(opname)
        raise ValueError(msg2)
    if n is not None:
        is_length_n(x, opname, n)
    for i, item in enumerate(x):
        if not isinstance(item, str):
            msg3 =\
                "{0} has an item at index {1} that is not of type str " +\
                "but of {2}."\
                .format(opname, i, type(item))
            raise ValueError(msg3)
    return None

def is_nonnegative(x):
    if not isinstance(x, int):
        msg1 = "pop.at_least must be an integer, not of {}."
        raise TypeError(msg1.format(type(x)))
    if x < 0:
        msg2 = "pop.at_least must be a nonnegative integer, not {}."
        raise ValueError(msg2.format(x))
    return None

def is_list_containing(x, opname):
    if not isinstance(x, list):
        msg1 =\
            "{0} must be a list, not of {1}."\
            .format(opname, type(x))
        raise TypeError(msg1)
    for i, item in enumerate(x):
        if not isinstance(item, str):
            msg2 =\
                "{0} has an item at index {1} that is not of type str " +\
                "but of {2}."\
                .format(opname, i, type(item))
            raise ValueError(msg2)
    comps = [
        comp_neg_temp_out, comp_neg_emi, comp_neg_npr_out, 
        comp_neg_death, comp_neg_interprov_out, comp_neg_intraprov_out,
        comp_pos_temp_in, comp_pos_ret_emi, comp_pos_npr_in,
        comp_pos_immi, comp_pos_interprov_in, comp_pos_intraprov_in
    ]
    msg3 = "{0} is not a subset of all the components.".format(x)
    assert set(x).issubset(comps), msg3

    return None

def is_method(x):
    is_str(x, 'method', False)
    raise_if_not_subset([x], method_all, x, str(method_all))

    return None

is_int_age_max = lambda x: is_int(x, 'age.max')
is_int_age_down_to = lambda x: is_int(x, 'age.down_to')
is_str_comp_neg_temp_out = lambda x: is_str(x, 'comp_neg.temp_out')
is_str_comp_neg_emi = lambda x: is_str(x, 'comp_neg.emi')
is_str_comp_neg_npr_out = lambda x: is_str(x, 'comp_neg.npr_out')
is_str_comp_neg_death = lambda x: is_str(x, 'comp_neg.death')
is_str_comp_neg_interprov_out = lambda x: is_str(x, 'comp_neg.interprov_out')
is_str_comp_neg_intraprov_out = lambda x: is_str(x, 'comp_neg.intraprov_out')
is_str_comp_pos_temp_in = lambda x: is_str(x, 'comp_pos.temp_in')
is_str_comp_pos_ret_emi = lambda x: is_str(x, 'comp_pos.ret_emi')
is_str_comp_pos_npr_in = lambda x: is_str(x, 'comp_pos.npr_in')
is_str_comp_pos_immi = lambda x: is_str(x, 'comp_pos.immi')
is_str_comp_pos_interprov_in = lambda x: is_str(x, 'comp_pos.interprov_in')
is_str_comp_pos_intraprov_in = lambda x: is_str(x, 'comp_pos.intraprov_in')
is_str_pop_age = lambda x: is_str(x, 'pop.age', False)
is_str_pop_birth = lambda x: is_str(x, 'pop.birth', False)
is_str_pop_end = lambda x: is_str(x, 'pop.end', False)
is_str_pop_sex = lambda x: is_str(x, 'pop.sex', False)
is_str_pop_start = lambda x: is_str(x, 'pop.start', False)
is_list_containing_comp_end = lambda x: is_list_containing(x, 'comp.end')



_global_config = {
    'age': {
        'down_to': age_down_to,
        'max': age_max
    },
    'comp': {
        'end': comp_end
    },
    'comp_neg': {
        'temp_out': comp_neg_temp_out,
        'emi': comp_neg_emi,
        'npr_out': comp_neg_npr_out,
        'death': comp_neg_death,
        'interprov_out': comp_neg_interprov_out,
        'intraprov_out': comp_neg_intraprov_out
    },
    'comp_pos': {
        'temp_in': comp_pos_temp_in,
        'ret_emi': comp_pos_ret_emi,
        'npr_in': comp_pos_npr_in,
        'immi': comp_pos_immi,
        'interprov_in': comp_pos_interprov_in,
        'intraprov_in': comp_pos_intraprov_in
    },
    'method': method,
    'pop': {
        'age': pop_age,
        'birth': pop_birth,
        'at_least': pop_at_least,
        'end': pop_end,
        'sex': pop_sex,
        'start': pop_start
    }
}
_registered_options = {
    'age.down_to': RegisteredOption(
        key = 'age.down_to',
        defval = age_down_to,
        doc =\
            "\n (int)\n    " +\
            "A bottom level of the neighbouring ages for the " +\
            "problematic age. Counter-adjustments are applied " +\
            "from the maximum neighbouring age and " +\
            "all the way down to the maximum of -1 and " +\
            "age of modification - age.down_to.",
        validator = is_int_age_down_to
    ),
    'age.max': RegisteredOption(
        key = 'age.max',
        defval = age_max,
        doc =\
            "\n (int)\n    " +\
            'A maximum individual age. Any age bigger than ' +\
            'this option is classified as the "plus category." ' +\
            'That is, if `age.max` == 99 (default), then any age ' +\
            'greater than or equal to 100 is classified as `100+`.', 
        validator = is_int_age_max
    ),
    'comp.end': RegisteredOption(
        key = 'comp.end',
        defval = comp_end,
        doc =\
            '\n (list of str)\n '+\
            'A list of components that denote the end-of-period ' +\
            'figures. This must be a subset of all the components.',
        validator = is_list_containing_comp_end
    ),
    'comp_neg.temp_out': RegisteredOption(
        key = 'comp_neg.temp_out',
        defval = comp_neg_temp_out,
        doc =\
            "\n (str or None)\n " +\
            'A name that denotes "Temporary emigrants OUT" ' +\
            "during the period in a population table. ",
        validator = is_str_comp_neg_temp_out
    ),
    'comp_neg.emi': RegisteredOption(
        key = 'comp_neg.emi',
        defval = comp_neg_emi,
        doc =\
            "\n (str or None)\n " +\
            'A name that denotes "Emigrants" ' +\
            "during the period in a population table.",
        validator = is_str_comp_neg_emi
    ),
    'comp_neg.npr_out': RegisteredOption(
        key = 'comp_neg.npr_out',
        defval = comp_neg_npr_out,
        doc =\
            "\n (str or None)\n " +\
            'A name that denotes "Non-permanent residents" (OUT) ' +\
            "at the end of the period in a population table.",
        validator = is_str_comp_neg_npr_out
    ),
    'comp_neg.death': RegisteredOption(
        key = 'comp_neg.death',
        defval = comp_neg_death,
        doc =\
            "\n (str or None)\n " +\
            'A name that denotes "Deaths" ' +\
            "during the period in a population table.",
        validator = is_str_comp_neg_death
    ),
    'comp_neg.interprov_out': RegisteredOption(
        key = 'comp_neg.interprov_out',
        defval = comp_neg_death,
        doc =\
            "\n (str or None)\n " +\
            'A name that denotes "Interprovincial migration OUT" ' +\
            "during the period in a population table.",
        validator = is_str_comp_neg_interprov_out
    ),
    'comp_neg.intraprov_out': RegisteredOption(
        key = 'comp_neg.intraprov_out',
        defval = comp_neg_death,
        doc =\
            "\n (str or None)\n " +\
            'A name that denotes "Intraprovincial migration OUT" ' +\
            "during the period in a population table.",
        validator = is_str_comp_neg_intraprov_out
    ),
    'comp_pos.temp_in': RegisteredOption(
        key = 'comp_pos.temp_in',
        defval = comp_pos_temp_in,
        doc =\
            "\n (str or None)\n " +\
            'A name that denotes "Temporary emigrants IN" ' +\
            "during the period in a population table.",
        validator = is_str_comp_pos_temp_in
    ),
    'comp_pos.ret_emi': RegisteredOption(
        key = 'comp_pos.ret_emi',
        defval = comp_pos_ret_emi,
        doc =\
            "\n (str or None)\n " +\
            'A name that denotes "Returning emigrants" ' +\
            "during the period in a population table.",
        validator = is_str_comp_pos_ret_emi
    ),
    'comp_pos.npr_in': RegisteredOption(
        key = 'comp_pos.npr_in',
        defval = comp_pos_npr_in,
        doc =\
            "\n (str or None)\n " +\
            'A name that denotes "Non-permanent residents" (IN) ' +\
            "at the start of the period in a population table.",
        validator = is_str_comp_pos_ret_emi
    ),
    'comp_pos.immi': RegisteredOption(
        key = 'comp_pos.immi',
        defval = comp_pos_immi,
        doc =\
            "\n (str or None)\n " +\
            'A name that denotes "Immigrants" ' +\
            "during the period in a population table.",
        validator = is_str_comp_pos_immi
    ),
    'comp_pos.interprov_in': RegisteredOption(
        key = 'comp_pos.interprov_in',
        defval = comp_pos_interprov_in,
        doc =\
            "\n (str or None)\n " +\
            'A name that denotes "Interprovincial migration IN" ' +\
            "during the period in a population table.",
        validator = is_str_comp_pos_interprov_in
    ),
    'comp_pos.intraprov_in': RegisteredOption(
        key = 'comp_pos.intraprov_in',
        defval = comp_pos_interprov_in,
        doc =\
            "\n (str or None)\n " +\
            'A name that denotes "Intraprovincial migration IN" ' +\
            "during the period in a population table.",
        validator = is_str_comp_pos_intraprov_in
    ),
    'method': RegisteredOption(
        key = "method",
        defval = method,
        doc =\
            "\n (str)\n    " +\
            "A method to apply counter-adjustments to a population " +\
            "table. Must be either one of '1dist' or 'prop'.",
        validator = is_method
    ),
    'pop.age': RegisteredOption(
        key = "pop.age",
        defval = pop_age,
        doc =\
            "\n (str)\n    " +\
            'A name that denotes the age in a population table. ' +\
            'This option cannot be None.',
        validator = is_str_pop_age
    ),
    'pop.birth': RegisteredOption(
        key = "pop.birth",
        defval = pop_birth,
        doc =\
            "\n (str)\n    " +\
            'A name that denotes the birth in a population table. ' +\
            'This option cannot be None.',
        validator = is_str_pop_birth
    ),
    'pop.at_least': RegisteredOption(
        key = "pop.at_least",
        defval = pop_at_least,
        doc =\
            "\n (int)\n    " +\
            "A minimum end-of-period population estimate that needs\n" +\
            "to be kept." +\
            "This option cannot be None.",
        validator = is_nonnegative
    ),
    'pop.end': RegisteredOption(
        key = "pop.end",
        defval = pop_end,
        doc =\
            "\n (str or None)\n    " +\
            'A name that denotes the end-of-period population ' +\
            'in a population table.',
        validator = is_str_pop_end
    ),
    'pop.sex': RegisteredOption(
        key = "pop.sex",
        defval = pop_sex,
        doc =\
            "\n (str or None)\n    " +\
            'A name that denotes the sex in a population table. ' +\
            'If None, it assumes that records in a population table ' +\
            'all have the same sex.' +\
            'This option cannot be None.',
        validator = is_str_pop_sex
    ),
    'pop.start': RegisteredOption(
        key = "pop.start",
        defval = pop_start,
        doc =\
            "\n (str)\n    " +\
            'A name that denotes the start-of-period population ' +\
            'in a population table. ' +\
            'This option cannot be None.',
        validator = is_str_pop_start
    )
}



class CallableDynamicDoc:
    def __init__(self, func):
        self.__func__ = func

    def __call__(self, *args, **kwargs):
        return self.__func__(*args, **kwargs)

class DictWrapper:
    def __init__(self, d, prefix = ""):
        object.__setattr__(self, "d", d)
        object.__setattr__(self, "prefix", prefix)

    def __setattr__(self, key, val):
        prefix = object.__getattribute__(self, "prefix")
        if prefix:
            prefix += "."
        prefix += key
        if key in self.d and not isinstance(self.d[key], dict):
            _set_option(prefix, val)
        else:
            raise KeyError("Value cannot be set to nonexisting options.")

    def __getattr__(self, key):
        prefix = object.__getattribute__(self, "prefix")
        if prefix:
            prefix += "."
        prefix += key
        try:
            v = object.__getattribute__(self, "d")[key]
        except KeyError:
            raise KeyError("No such option exists.")
        if isinstance(v, dict):
            return DictWrapper(v, prefix)
        else:
            return _get_option(prefix)

    def __dir__(self):
        return list(self.d.keys())



def _get_option(pat: str):
    key = _get_single_key(pat)

    # walk the nested dict
    root, k = _get_root(key)
    return root[k]

def _get_registered_option(key: str):

    return _registered_options.get(key)

def _get_root(key: str):
    path = key.split(".")
    cursor = _global_config
    for p in path[:-1]:
        cursor = cursor[p]
    return cursor, path[-1]

def _get_single_key(pat: str):
    keys = _select_options(pat)
    if len(keys) == 0:
        raise KeyError("No such keys: {pat!r}".format(pat = pat))
    if len(keys) > 1:
        raise KeyError("Pattern matched multiple keys.")
    key = keys[0]
    
    return key

def _reset_option(*args):
    nargs = len(args)
    pat = None
    keys = None
    if nargs == 1:
        pat = args[0]
        keys = _select_options(pat)
    else:
        for patt in args:
            _reset_option(patt)
        return None

    if len(keys) == 0:
        raise KeyError("No such key(s)")

    if len(keys) > 1 and len(pat) < 4 and pat != "all":
        raise ValueError(
            "You must specify at least 4 characters when "
            "resetting multiple keys; use the special keyword "
            '"all" to reset all the options to their default value'
        )

    for k in keys:
        _set_option(k, _registered_options[k].defval)

def _select_options(pat: str):
    if pat in _registered_options:
        return [pat]
    keys = sorted(_registered_options.keys())
    if pat == 'all':
        return keys
    
    return [k for k in keys if re.search(pat, k, re.I)]

def _set_option(*args, **kwargs):
    nargs = len(args)
    if not nargs or nargs % 2 != 0:
        msg = "Must provide an even number of non-keyword arguments."
        raise ValueError(msg)
    silent = kwargs.pop("silent", False)
    if kwargs:
        msg2 = '_set_option() got an unexpected keyword argument "{kwarg}"'
        raise TypeError(msg2.format(list(kwargs.keys())[0]))
    for k, v in zip(args[::2], args[1::2]):
        key = _get_single_key(k)
        o = _get_registered_option(key)
        if o and o.validator:
            o.validator(v)
        
        root, k = _get_root(key)
        root[k] = v



class option_context:
    '''
    A context manager to temporarily set options in the `with` statment
    context. You need to invoke as:

    `option_context(pat, val, [(pat, val), ...])`

    Examples
    --------
    >>> with option_context('pop.at_least', 0, 'age.interval', [-5, 0]):
    ...
    '''


    def __init__(self, *args):
        if not (len(args) % 2 == 0 and len(args) >= 2):
            msg =\
                "Need to invoke as " +\
                "option_context(pat, val, [(pat, val), ...])."
            raise ValueError(msg)
        self.ops = list(zip(args[::2], args[1::2]))

    def __enter__(self):
        self.undo = [(pat, _get_option(pat)) for pat, val in self.ops]
        for pat, val in self.ops:
            _set_option(pat, val)

    def __exit__(self, *args):
        if self.undo:
            for pat, val in self.undo:
                _set_option(pat, val)



get_option = CallableDynamicDoc(_get_option)
options = DictWrapper(_global_config)
reset_option = CallableDynamicDoc(_reset_option)
set_option = CallableDynamicDoc(_set_option)
