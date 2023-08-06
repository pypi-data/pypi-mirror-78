"""
General purpose tcl script creation module
"""
import typing

_opt_str = typing.Optional[str]


def create_project(file, project_name, filename, comp_name, includes, defines,
                   standard, solution_name, part, period, pipeline, ctrl_hs,
                   depth_constraint):
    """
    Generate a tcl script for an HLS component creation
    :param filename: name of the file containing hls code
    :param period: clock period in ns
    :param part: part code to use
    :param solution_name: name of the solution to create inside the project
    :param file: the file on which the script will be written
    :param project_name: the name of the vivado project to generate
    :param comp_name: the name of the high level component
    :param includes: list of include directories
    :param defines: list of defines
    :param standard: c++ standard code to use
    :param pipeline: should vivado pipeline the design
    :param ctrl_hs: should the design be wrapped with ap_ctrl_hs control signals
    :depth_constraint: depth_constraint to set
    """
    file.write("open_project {}\n".format(project_name))
    file.write("set_top {}\n".format(comp_name))
    includes_str = "" if includes is None else " ".join(
        ["-I{}".format(str(s).replace("\\", "/")) for s in includes]
    )
    if defines:
        def format_def(define):
            if len(define) == 2:
                k, v = define
                return f"-D{k}={v}"
            else:
                return f"{define[0]}"

        def_str = " ".join(map(format_def, defines))
    else:
        def_str = ""
    file.write(f'add_files {filename} -cflags "-std={standard} {includes_str} {def_str}"\n')
    file.write('open_solution "{}"\n'.format(solution_name))
    file.write('set_part {{{}}} -tool vivado\n'.format(part))
    file.write('create_clock -period {} -name default\n'.format(
        period
    ))
    # Register function inputs and output to get accurate timings

    file.write('set_clock_uncertainty 0.0 default\n')
    ctrl_mode = 'ap_ctrl_hs' if ctrl_hs else 'ap_ctrl_none'
    file.write(f'set_directive_interface -mode {ctrl_mode} [get_top]\n')
    file.write('config_schedule -relax_ii_for_timing=0 -effort high\n')
    file.write('set_directive_inline -recursive [get_top]\n')
    reg_type = "scalar_out"
    if pipeline:
        file.write('set_directive_pipeline -II 1 [get_top]\n')
    if depth_constraint is not None:
        if depth_constraint == 1:
            reg_type = 'scalar_all'
            depth_constraint = 2
        file.write('set_directive_latency -min {} -max {} [get_top]\n'.format(depth_constraint, depth_constraint))
    file.write(f'config_interface -register_io {reg_type}\n')

def csynth_solution_script(file):
    """Generate a script in file for synthetizing solution solution_name of project project_name"""
    file.write('csynth_design\n')


def export_ip_script(file,
                     impl: bool,
                     hdl: str,
                     display_name: _opt_str = None,
                     descr: _opt_str = None,
                     version: _opt_str = None,
                     ip_lib: _opt_str = None,
                     vendor: _opt_str = None,
                     ):
    """Generate a script in file for exporting solution solution_name of project project_name"""
    options = [
        "-format ip_catalog",
        f"-rtl {hdl}",
        "-flow {}".format("impl" if impl else "syn")
    ]
    if display_name is not None:
        options.append(f"-display_name {display_name}")
    if descr is not None:
        options.append(f'-description "{descr}"')
    if ip_lib is not None:
        options.append(f'-library {ip_lib}')
    if vendor is not None:
        options.append(f'-vendor {vendor}')
    if version is not None:
        options.append(f'-version {version}')

    command = "export_design {}\n".format(" ".join(options))
    file.write(command)
