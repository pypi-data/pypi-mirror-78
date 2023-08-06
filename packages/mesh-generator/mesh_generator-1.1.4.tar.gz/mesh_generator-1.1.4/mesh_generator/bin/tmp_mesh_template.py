""" Rewrite tmp_mesh_[t/p/r].dat file to be in scientific notation with single precision."""


def rewrite_tmp_mesh_file(tmp_mesh_path):
    with open(tmp_mesh_path, 'r') as file1:
        mesh_data = file1.readlines()

    # mesh domain s0, s1. Change to sn, 6 digits.
    mesh_data[7] = " " + convert_string_of_float_to_sn(mesh_data[7]) + "\n"

    # mesh segment domain.
    mesh_data[9] = mesh_data[9].replace("/", "")
    mesh_data[9] = convert_string_of_float_to_sn(mesh_data[9])
    mesh_data[9] = " " + mesh_data[9] + "/" + "\n"

    # mesh ratio.
    mesh_data[11] = mesh_data[11].replace("/", "")
    mesh_data[11] = convert_string_of_float_to_sn(mesh_data[11])
    mesh_data[11] = " " + mesh_data[11] + "/" + "\n"

    # mesh phi shift.
    mesh_data[13] = " " + "{0:.6E}".format(float(mesh_data[13])) + "\n"

    # rewrite tmp_mesh_[t/p/r].dat file.
    with open(tmp_mesh_path, 'w') as file2:
        file2.writelines(mesh_data)


def convert_string_of_float_to_sn(input_string):
    """Convert a float string to scientific notation for tmp_mas files.
    :param input_string: str.
    :return: output_string. (scientific notation with 6 digits).
    """
    str_list = input_string.split(", ")
    for ii in range(len(str_list)):
        if ii == 0:
            output_string = "{0:.6E}".format(float(str_list[ii]))
        else:
            output_string = output_string + ", " + "{0:.6E}".format(float(str_list[ii]))
    return output_string


if __name__ == "__main__":
    rewrite_tmp_mesh_file("tests/py_outputs/POT3D/tmp_mesh_r.dat")
    rewrite_tmp_mesh_file("tests/py_outputs/POT3D/tmp_mesh_t.dat")
    rewrite_tmp_mesh_file("tests/py_outputs/POT3D/tmp_mesh_p.dat")
