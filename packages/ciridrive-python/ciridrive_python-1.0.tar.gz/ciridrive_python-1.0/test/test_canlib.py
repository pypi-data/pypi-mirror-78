from ciridrive_python import ciridrive
import json

ciri = ciridrive()


def list_to_dict(list_sheet):
    """
        Goal: 
            Transform the received list into a dictionary for each sheet tab
        Args:
            list_sheet: list containing the tab data
        Returns:
            list_final: list containing all the spreadsheet data, organized in dictionaries
    """

    """
    with open("sheet_json.json", "r") as file:
        json_load = json.load(file)

    list_sheet = json_load["Driverless"]
    """
    dict_column, list_final, list_var = {}, [], []

    list_column = [
        "name",
        "id",
        "bit/byte",
        "true/format",
        "type",
        "decimal_place",
        "min",
        "max",
        "unit",
        "offset",
        "multiplier",
    ]

    # Analyzes the first column
    for i, column1 in enumerate(list_sheet[0]):
        # If it has an "end" it will close the function
        if column1 == "END":
            break

        elif column1 != "":
            dict_column[list_column[1]] = list_sheet[1][i]

            # Na versão final mudar isso
            dict_column["lenght_msg"] = list_sheet[2][i].split("B")[0]
            dict_column["name"] = column1.lower()

            line = 1
            # Analyzes the "name" column as long as there is a variable,
            #   populates the dictionary
            while list_sheet[1][i + line] != "":
                if list_sheet[2][i + line + 1] != "":
                    if line <= len(list_sheet[4]):
                        dict_var = {"name": list_sheet[1][i + line].lower()}
                        for id_column, name_column in enumerate(list_column[2:]):
                            dict_var[name_column] = list_sheet[id_column + 2][i + line]

                        list_var.append(dict_var)

                    line += 1
                else:
                    lineBit = line
                    # If the same bit or byte represents more than one variable
                    while list_sheet[2][i + line + 1] == "":
                        dict_var = {"name": list_sheet[1][i + line].lower()}
                        for i_column, name_column in enumerate(list_column[2:]):
                            if name_column == "bit/byte":
                                dict_var[name_column] = list_sheet[i_column + 2][
                                    i + lineBit
                                ]
                            else:
                                dict_var[name_column] = list_sheet[i_column + 2][
                                    i + line
                                ]

                        list_var.append(dict_var)

                        line += 1

                    # Checks whether one more variable for the bit
                    if list_sheet[1][i + line] != "":
                        dict_var = {"name": list_sheet[1][i + line].lower()}
                        for i_column, name_column in enumerate(list_column[2:]):
                            if name_column == "bit/byte":
                                dict_var[name_column] = list_sheet[i_column + 2][
                                    i + lineBit
                                ]
                            else:
                                dict_var[name_column] = list_sheet[i_column + 2][
                                    i + line
                                ]

                        list_var.append(dict_var)

                        line += 1

            # Create dictionary
            dict_column["variable"] = list_var
            list_final.append(dict_column)
            dict_column, dict_var, list_var = {}, {}, []

    return list_final


def list_to_dict_telemetria(list_sheet):
    """
        Goal: 
            Transform the received list into a dictionary for each sheet tab
        Args:
            list_sheet: list containing the tab data
        Returns:
            list_final: list containing all the spreadsheet data, organized in dictionaries
    """

    """
    with open("sheet_json.json", "r") as file:
        json_load = json.load(file)

    list_sheet = json_load["Driverless"]
    """
    dict_column, dict_final = {}, {}

    list_column = [
        "name",
        "id",
        "type",
        "can_id",
        "lenght",
        "decimal_cases",
        "unit",
        "max",
        "min",
        "plotable",
    ]

    dict_convert = {
        "int": int,
        "float": float,
        "bool": bool,
    }

    # Analyzes the first column
    for i, column1 in enumerate(list_sheet[0]):
        # If it has an "end" it will close the function
        if column1 == "END":
            break

        elif column1 != "":
            # dict_column["name"] = column1.lower()

            line = 1
            # Analyzes the "name" column as long as there is a variable,
            #   populates the dictionary
            while list_sheet[1][i + line] != "":
                if list_sheet[2][i + line + 1] != "":
                    if line <= len(list_sheet[4]):
                        dict_var = {}
                        dict_var["type"] = list_sheet[2][i + line]
                        for id_column, name_column in enumerate(list_column[3:]):
                            if name_column == "max" or name_column == "min":
                                if list_sheet[id_column + 3][i + line] != "":
                                    dict_var[name_column] = dict_convert[
                                        dict_var["type"]
                                    ](list_sheet[id_column + 3][i + line])
                                else:
                                    dict_var[name_column] = ""
                            else:
                                dict_var[name_column] = list_sheet[id_column + 3][
                                    i + line
                                ]

                        dict_final[list_sheet[1][i + line].lower()] = dict_var

                    line += 1
                else:
                    lineBit = line
                    # If the same bit or byte represents more than one variable
                    while list_sheet[2][i + line + 1] == "":
                        dict_var = {}
                        dict_var["type"] = list_sheet[2][i + line]
                        for i_column, name_column in enumerate(list_column[3:]):
                            if name_column == "max" or name_column == "min":
                                if list_sheet[i_column + 3][i + line] != "":
                                    dict_var[name_column] = dict_convert[
                                        dict_var["type"]
                                    ](list_sheet[i_column + 3][i + line])
                                else:
                                    dict_var[name_column] = ""
                            else:
                                dict_var[name_column] = list_sheet[i_column + 3][
                                    i + line
                                ]
                        dict_final[list_sheet[1][i + line].lower()] = dict_var

                        line += 1

                    # Checks whether one more variable for the bit
                    if list_sheet[1][i + line] != "":
                        dict_var = {}
                        for i_column, name_column in enumerate(list_column[3:]):
                            if name_column == "max" or name_column == "min":
                                if list_sheet[id_column + 3][i + line] != "":
                                    dict_var[name_column] = dict_convert[
                                        dict_var["type"]
                                    ](list_sheet[id_column + 3][i + line])
                                else:
                                    dict_var[name_column] = ""
                            else:
                                dict_var[name_column] = list_sheet[id_column + 3][
                                    i + line
                                ]
                        dict_final[list_sheet[1][i + line].lower()] = dict_var

                        line += 1

            # Create dictionary
            dict_column[column1.lower()] = dict_final

            dict_var, dict_final = {}, {}

    return dict_column


tab_canlib = ["inicio!B1", "Driverless"]
dict_test = {}
for tab in tab_canlib:
    list_sheet = ciri.sheet_to_json(
        "1CNoVzaXox9Vqzpnxgi4gl-XYKO2783NDejw3IT_Dt3I", tab_name=tab
    )
    print(list_sheet)
    if "inicio" in tab:
        dict_test[tab] = list_sheet[tab][0][0]
        print(dict_test[tab])
    else:
        dict_test[tab] = list_to_dict_telemetria(list_sheet[tab])

# print(dict_test)

with open("test/temp_json_test.json", "w") as file:
    json.dump(dict_test, file)


# 1TagLVILL_uBmsffZoC07pYLQ3ZDSRe5G8Led3oA6Ysc planilha canlib

# 49P7uzm6tAxNeBd