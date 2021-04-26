DEFINED_TYPES = {"int" : int,
                 "float" : float,
                 "bool" : bool,
                 "tuple" : tuple,
                 "string" : str,
                 "none" : str,
                 "str" : str}

def loadConfig(filename, converters_dict={}):
    """Load and return a configuration in a configuration file.
        IN:
            filename (string): configuration path
            converters_dict (dict): dictionary of converter functions for custom types
        OUT:
            params (dict), param_types (dict)
    """
    params = {} # dictionary of parameters
    param_types = {} # dictionary of parameter types
    with open(filename) as f:
        for line in f.readlines():
            if len(line) > 1: # whitespace
                if line[0] != "#": # comment
                    l1 = line.split(" : ")
                    if len(l1) < 2:
                        raise ValueError("@loadConfig: error in line: " + line)
                    varname = l1[0].strip()
                    l2 = l1[1].split("=")
                    if len(l2) < 2:
                        raise ValueError("@loadConfig: error in line: " + line)
                    vartype = l2[0].strip()
                    value = l2[1].split("#")[0].strip() # comment after line allowed

                    conv_val = None
                    if vartype == "int":
                        conv_vartype = int
                        conv_val = int(value)
                    elif vartype == "float":
                        conv_vartype = float
                        conv_val = float(value)
                    elif vartype == "bool":
                        conv_vartype = bool
                        if value == "True" or value == "T" or value == "1":
                            conv_val = True
                        elif value == "False" or value == "F" or value == "0":
                            conv_val = False
                        else:
                            raise ValueError("@config.loadConfig: invalid bool value: " + value)
                    elif vartype == "tuple":
                        conv_vartype = tuple
                        conv_val = tuple(value)
                    elif vartype == "string" or vartype == "none" or vartype == "str":
                        conv_vartype = str
                        conv_val = value
                    elif len(vartype) >= 4:
                        if vartype == "list":
                            conv_vartype = list
                            ls = value[1:-1].split(",") # e.g. [3, 2, 1]
                            for i, l in enumerate(ls):
                                ls[i] = l.strip()
                            conv_val = ls
                        elif vartype[4] == "(":
                            try:
                                inner = DEFINED_TYPES[vartype[5:-1]] # convert inner arguments
                            except KeyError:
                                try:
                                    inner = converters_dict[vartype[5:-1]]
                                except KeyError:
                                    raise TypeError("@loadConfig: unsupported inner parameter type: "
                                                    + vartype[5:-1])
                            conv_vartype = list
                            ls = value[1:-1].split(",")
                            for i, l in enumerate(ls):
                                ls[i] = inner(l.strip()) # does this even work - apparently it does
                            conv_val = ls
                    elif vartype in converters_dict.keys():
                        conv_vartype = vartype # not a class reference, a string
                        conv_val = converters_dict[vartype](value)
                    else:
                        raise TypeError("@loadConfig: unsupported parameter type: " + vartype)

                    params[varname] = conv_val
                    param_types[varname] = conv_vartype
    return params, param_types

if __name__ == "__main__":
    print(loadConfig("./config.txt"))
                
                    
