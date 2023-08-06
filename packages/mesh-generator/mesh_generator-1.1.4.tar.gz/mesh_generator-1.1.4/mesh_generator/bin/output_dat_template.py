"""
Write output02_mesh_t/p/r.dat file with legacy mesh results.
"""


def write_output_file(legacy_mesh: dict, NUM_OF_FILTER: int, mesh_type: str, output_path: str):
    """
    Print the solution of the legacy test in a output02_mesh_t.dat file where it will be
    similar to the IDL file format so the fortran mesh will be able to read the mesh requirements and
    generate a mesh_res.txt file with all the mesh points


    Arguments:
        :param output_path: full path to the output file written.
        :param mesh_type: 't'/'p'/'r'
        :param legacy_mesh : dictionary of legacy mesh
        :param NUM_OF_FILTER: number of filters applied
    """

    tol_n = 0  # total number of points in legacy mesh
    ratio_in_s = []  # ratio between s0 and legacy upper bound
    ratio_in_ds = []  # ration between ds0 and ds1

    for idx in range(0, len(legacy_mesh['segment_list'])):
        segments = legacy_mesh['segment_list'][idx]
        tol_n += segments["num_points"]
        ratio_in_s.append((segments["s0"] - legacy_mesh["lower_bnd"]) /
                          (legacy_mesh["upper_bnd"] - legacy_mesh["lower_bnd"]))
        if idx == len(legacy_mesh['segment_list']) - 1:
            ratio_in_s.append(segments["s1"] / legacy_mesh["upper_bnd"])
        ratio_in_ds.append(segments["ratio"])

    # open .dat file
    with open(output_path, "w") as f:
        f.write("Mesh coordinate label:\n%s \n" % mesh_type)
        f.write("Flag to specify a periodic mesh [.true.|.false.]:\n%s \n" % _is_periodic(legacy_mesh['periodic']))
        f.write("Number of mesh points:\n%s \n" % tol_n)
        f.write(
            "Lower and upper mesh limits [X0,X1]:\n %s, %s \n" % (legacy_mesh["lower_bnd"], legacy_mesh["upper_bnd"]))

        if not legacy_mesh['periodic']:
            f.write("Position of segments, FRAC [terminated with /]:\n %s" % ratio_in_s[0])
            for i in range(1, len(ratio_in_s)):
                f.write(', ' + str(ratio_in_s[i]))
            f.write('/ \n')

        if legacy_mesh['periodic']:
            f.write("Position of segments, FRAC [terminated with /]:\n %s" % ratio_in_s[0])
            for i in range(1, len(ratio_in_s) - 1):
                f.write(', ' + str(ratio_in_s[i]))
            f.write('/ \n')

        f.write("Ratio of segments, DRATIO [terminated with /]:\n %s" % (ratio_in_ds[0]))
        for i in range(1, len(ratio_in_ds)):
            f.write(', ' + str(ratio_in_ds[i]))
        f.write('/ \n')

        f.write("Amount to shift the mesh:\n %s \n" % legacy_mesh['phi_shift'])

        f.write("Number of times to filter:\n%s \n" % NUM_OF_FILTER)

    return tol_n


def _is_periodic(legacy):
    if not legacy:
        return ".false."
    else:
        return ".true."


if __name__ == "__main__":
    from tests.ar_test import *

    write_output_file(legacy__mesh_phi_2().json_dict())
