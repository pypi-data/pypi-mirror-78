import numpy as np


def output_obj_to_table(obj, olist='inputs', oformat='latex', table_ends=False, prefix=""):
    """
    Compile the properties to a table.

    :param olist: list, Names of the parameters to be in the output table
    :param oformat: str, The type of table to be output
    :param table_ends: bool, Add ends to the table
    :param prefix: str, A string to be added to the start of each parameter name
    :return: para, str, table as a string
    """
    para = ""
    property_list = []
    if olist == 'inputs':
        property_list = obj.inputs
    elif olist == 'all':
        for item in obj.__dict__:
            if "_" != item[0]:
                property_list.append(item)
    for item in property_list:
        if hasattr(obj, item):
            value = getattr(obj, item)
            value_str = format_value(value)
            if oformat == "latex":
                delimeter = " & "
            else:
                delimeter = ","
            para += "{0}{1}{2}\\\\\n".format(prefix + format_name(item), delimeter, value_str)
    if table_ends:
        para = add_table_ends(para, oformat)
    return para


def output_df_to_table(df, headers=None, oformat='latex', table_ends=False, prefix="", caption="caption-text", label="table"):
    """
    Compiles a Dataframe to a table.

    :param table_ends: bool, Add ends to the table
    :param prefix: str, A string to be added to the start of each parameter name
    :return: para, str, table as a string
    """
    paras = []
    property_list = []

    if headers is not None:
        latex_headers = headers
    else:
        latex_headers = [format_name(item) for item in df.columns]
    la_header = ' & '.join(latex_headers)

    for i in range(len(df)):
        line = []
        for h, col in enumerate(df.columns):
            line.append(format_value(df[col].iloc[i]))
        paras.append('&'.join(line) + '\\\\')
    para = '\n'.join(paras)
    if table_ends:
        para = add_table_ends(para, oformat, np=len(df.columns), header=la_header, caption=caption, label=label)
    return para


def format_name(name):
    """
    format parameter names for output

    :param name: Cleans a name for output
    :return:
    """
    name = name.replace("_", " ")
    return name


def format_value(value, sf=3):
    """
    convert a parameter value into a formatted string with certain significant figures

    :param value: the value to be formatted
    :param sf: number of significant figures
    :return: str
    """
    if isinstance(value, str):
        return format_name(value)

    elif isinstance(value, list) or isinstance(value, np.ndarray):
        value = list(value)
        for i in range(len(value)):
            vv = format_value(value[i])
            value[i] = vv
        return "[" + ", ".join(value) + "]"

    elif value is None:
        return "N/A"

    else:
        fmt_str = "{0:.%ig}" % sf
        return fmt_str.format(value)


def add_table_ends(para, oformat='latex', caption="caption-text", label="table", np=2, align='c', header=None):
    """
    Adds the latex table ends

    :param para:
    :param oformat:
    :param caption:
    :param label:
    :return:
    """
    if len(align) == 1:
        a_str = "".join([align] * np)
    else:
        a_str = align
    fpara = ""
    if oformat == 'latex':
        fpara += "\\begin{table}[H]\n"
        fpara += "\\centering\n"
        fpara += "\\begin{tabular}{%s}\n" % a_str
        fpara += "\\toprule\n"
        if header:
            fpara += f"{header} \\\\\n"
        fpara += "\\midrule\n"
        fpara += para
        fpara += "\\bottomrule\n"
        fpara += "\\end{tabular}\n"
        fpara += "\\caption{%s \label{tab:%s}}\n" % (caption, label)
        fpara += "\\end{table}\n\n"
    return fpara

