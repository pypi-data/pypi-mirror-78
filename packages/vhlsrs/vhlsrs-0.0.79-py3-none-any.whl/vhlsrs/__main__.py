import argparse
import configparser
from enum import Enum
import logging
from pathlib import Path
from sys import stdout

from . import exp_strategy
from . import vivado_exp

DEFAULT_PART = "xc7k160tfbg484-1"
DEFAULT_STANDARD = "c++14"

class CommandType(Enum):
    IMPLEMENTATION = 0
    MINIMIZE = 1


def parse_includes(include_str, ini_path):
    preprocessed = [Path(s.strip()) for s in include_str.split(',')]
    final = []
    for p in preprocessed:
        if p.is_absolute():
            final.append(p)
        else:
            absolute = (ini_path / p).resolve()
            final.append(absolute)
    return final


def parse_defines(defines_str):
    defines_list = defines_str.split(',')
    defines = []
    for d in defines_list:
        if '=' in d:
            d = d.split('=')
            defines.append((d[0].strip(), d[1].strip()))
        else:
            defines.append(d.strip())
    return defines

def run_minimize(exp, pipeline_depth): 
    if pipeline_depth is not None:
        print("Pipeline_depth was given to run_minimize : it will be ignored")
    handler = exp_strategy.CSVHandler('{}.csv'.format(exp.name.strip()))
    exp_strategy.minimize_latency(
        exp,
        [handler]
    )

def run_implement(exp, pipeline_depth):
    result = exp.run_exp(depth_constraint=pipeline_depth).get_results()
    print(result)

def run_meta_exp(name, config, config_path, command, export_hls, export_ip):
    comp_path = config['comp_path']
    comp_name = config['top_level_comp']
    clock_period = float(config['period'])
    part = config['part'] if 'part' in config else DEFAULT_PART
    standard = config['standard'] if 'standard' in config else DEFAULT_STANDARD
    includes = parse_includes(config['includes'], config_path) if 'includes' in config else []
    defines = parse_defines(config['defines']) if 'defines' in config else {}
    keep_env = (config['keep_env'].strip().lower() == "true") if 'keep_env' in config else False
    ip_lib = config['ip_lib'] if 'ip_lib' in config else None
    version = config['ip_version'] if 'ip_version' in config else None
    description = config['ip_descr'] if 'ip_descr' in config else None
    vendor = config['ip_vendor'] if 'ip_vendor' in config else None
    latency = int(config['latency']) if 'latency' in config else None
    hdl_name = config['hdl'] if 'hdl' in config else 'vhdl'
    hdl = vivado_exp.HDL.VERILOG if hdl_name == 'verilog' else vivado_exp.HDL.VHDL
    no_pipeline = (config['no_pipeline'].strip().lower() == "true") if 'no_pipeline' in config else False
    ap_ctrl_hs = (config['ctrl_hs'].strip().lower() == "true") if 'ctrl_hs' in config else False
    exp_type_dict = {'hls' : vivado_exp.ExperienceType.CSYNTH_ONLY,
                     'syn' : vivado_exp.ExperienceType.SYNTHESIS,
                     'impl': vivado_exp.ExperienceType.IMPLEMENTATION}
    exp_type = exp_type_dict[config['exp_type']] if 'exp_type' in config else vivado_exp.ExperienceType.IMPLEMENTATION
    exp = vivado_exp.Experiment(
        name,
        comp_path,
        comp_name,
        clock_period,
        part,
        standard,
        hdl,
        exp_type,
        not no_pipeline,
        ap_ctrl_hs,
        keep_env,
        description=description,
        version=version,
        ip_lib=ip_lib,
        vendor=vendor
    )
    exp.add_defines(defines)
    exp.add_includes(includes)
    if export_hls:
        exp.add_before_del(vivado_exp.build_get_hls(exp))

    if export_ip:
        exp.add_before_del(vivado_exp.build_get_export_ip(exp))

    dispatch = {
        CommandType.MINIMIZE : run_minimize,
        CommandType.IMPLEMENTATION : run_implement,
    }
    dispatch[command](exp, latency)

def handle_args(args):
    ini_file = Path(args.exp_file).resolve()
    if (not ini_file.exists()) or (not ini_file.is_file()):
        raise FileNotFoundError('File {} does not exists or is not a regular '
                                'file'.format(ini_file))
    config = configparser.ConfigParser()
    config.read(ini_file)
    logger = logging.getLogger('vrs_log')
    handler = logging.StreamHandler(stdout)
    log_level = logging.DEBUG if args.debug else logging.INFO
    logger.setLevel(log_level)
    handler.setLevel(log_level)
    logger.addHandler(handler)
    association = {
        'impl' : CommandType.IMPLEMENTATION,
        'minimize' : CommandType.MINIMIZE,
    }
    command = association[args.command]
    export_hls = args.export_hls_files
    export_ip = args.export_ip
    for s in config.sections():
        run_meta_exp(s, config[s], ini_file.parent.resolve(), command,
                     export_hls, export_ip)


def main():
    parser = argparse.ArgumentParser(description="Perform synthesis and"
                                                 "implementation of vivado HLS components")
    parser.add_argument("--debug", "-d", action="store_true", help="Activate "
                                                                   "debug output")
    parser.add_argument("command", choices=["impl", "minimize"], help="which command to run")
    parser.add_argument("--export-hls-files", "-f", action="store_true",
                        help="Copy HLS files in current directory")
    parser.add_argument("--export-ip", "-i", action="store_true", help="Copy vivado IP in current directory")
    parser.add_argument("exp_file", help="Experiment description ini file")

    args = parser.parse_args()
    handle_args(args)


if __name__ == "__main__":
    main()
