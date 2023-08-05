# -*- coding: utf-8 -*-
"""
@author: Johannes Elfner <johannes.elfner@googlemail.com>
Date: Jun 2018
"""

import numpy as np
import numba as nb


def create_DataClass(instance_dict, calc_att_list):
    specs = {}
    inst_values = {}
    # check for types of isntance attributes and only select supported types.
    # also only select the needed variables, since creating jitclasse with
    # lots of attributes is horribly slow:
    for key, value in instance_dict.items():
        if key in calc_att_list:
            if isinstance(value, (int, float, bool, np.ndarray)):
                specs[key] = nb.typeof(value)
                inst_values[key] = value
            elif isinstance(value, (list, tuple)):
                print('l/t', key)
                if nb.types.string is not nb.typeof(value[0]):
                    specs[key] = nb.typeof(value)
                    inst_values[key] = value
                    print('l/t added', key)

    @nb.jitclass(spec=specs)
    class DataClass:
        def __init__(self):  # , value_list, key_list):
            pass

    #            i = 0
    #            for v in value_list:
    #                try:
    #                    self.__setattr__(key_list[i], v)
    #                except TypeError:
    #                    self.__delattr__(key_list[i])
    #                i += 1

    #    return DataClass(value_list, key_list)
    data_cls = DataClass()
    for key, val in inst_values.items():
        try:
            data_cls.__setattr__(key, val)
        except (TypeError, AttributeError):
            print(key, ' was not added successfully to DataClass!')
    #            try:
    #                data_cls.__delattr__(key)
    #            except AttributeError:
    #                pass

    return data_cls
