from __future__ import absolute_import, division, print_function

"""
Author      : Lyubimov, A.Y.
Created     : 10/12/2014
Last Changed: 10/31/2019
Description : IOTA command-line module.
"""
import time
import datetime

import argparse
from contextlib import contextmanager

from libtbx import easy_pickle as ep
import dials.util.command_line as cmd

from iota import iota_version, help_message, logo
from iota.components.iota_utils import main_log, iota_exit


def parse_command_args():
    """Parses command line arguments (only options for now)"""
    parser = argparse.ArgumentParser(
        prog="iota.run",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(help_message),
        epilog=("\n{:-^70}\n".format("")),
    )
    parser.add_argument(
        "path",
        type=str,
        nargs="*",
        default=None,
        help="Path to data or file with IOTA parameters",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="IOTA {}".format(iota_version),
        help="Prints version info of IOTA",
    )
    parser.add_argument(
        "-d",
        "--default",
        action="store_true",
        help="Generate default settings files and stop",
    )
    parser.add_argument(
        "--ha14", action="store_true", help="Run IOTA with old HA14 backend"
    )
    parser.add_argument(
        "--random",
        type=int,
        nargs=1,
        default=0,
        help='Size of randomized subset, e.g. "--random 10"',
    )
    parser.add_argument(
        "--range",
        type=str,
        nargs="?",
        default=None,
        help='Range of images, e.g."--range 1-5,25,200-250"',
    )
    parser.add_argument(
        "-o",
        "--out_type",
        type=str,
        nargs=1,
        default="progress",
        help="Type of stdout; default is progress bar in stdout",
    )
    parser.add_argument(
        "-n",
        "--nproc",
        type=int,
        nargs=1,
        default=0,
        help='Specify a number of cores for a multiprocessor run"',
    )
    parser.add_argument(
        "--analyze",
        type=str,
        nargs="?",
        const=None,
        default=None,
        help="Use for analysis only; specify run number or folder",
    )
    parser.add_argument(
        "--run_path",
        type=str,
        nargs=1,
        default=None,
        help="Path to a pre-initialized run",
    )
    parser.add_argument(
        "--tmp", type=str, nargs=1, default=None, help="Path to temp folder"
    )

    return parser


@contextmanager  # Will print start / stop messages around some processes
def prog_message(msg, prog="", msg2="", out_type="progress"):
    if out_type == "progress":
        cmd.Command.start(msg)
    elif "debug" in out_type:
        print("DEBUG {}: {}".format(prog, msg))
    elif out_type == "gui_verbose":
        print("IOTA {}: {}".format(prog, msg))
    yield
    if out_type == "progress":
        if msg2:
            cmd.Command.end("{} -- DONE".format(msg2))
        else:
            cmd.Command.end("{} -- DONE".format(msg))
    else:
        if msg2:
            if out_type == "debug":
                print("DEBUG {}: {}".format(prog, msg2))
            if out_type == "gui_verbose":
                print("IOTA {}: {}".format(prog, msg2))


from iota.components.iota_base import ProcessingBase


class Process(ProcessingBase):
    """Processing script w/o using the init object."""

    def __init__(self, out_type="silent", **kwargs):
        ProcessingBase.__init__(self, **kwargs)

        self.prog_count = 0
        self.out_type = out_type

    # TODO: may not have a callback option with new MP
    def callback(self, result):
        """Will add object file to tmp list for inclusion in info."""
        if self.out_type == "progress":
            if self.prog_count < self.info.n_input_images:
                prog_step = 100 / self.info.n_input_images
                self.gs_prog.update(self.prog_count * prog_step)
                self.prog_count += 1
            else:
                self.gs_prog.finished()

        if result:
            # Write image object to file from main processing thread
            ep.dump(result.obj_file, result)

            # Write image object path to list
            with open(self.info.obj_list_file, "a") as olf:
                olf.write("{}\n".format(result.obj_file))

    def process(self):
        """Run importer and/or processor."""

        start_time = time.time()

        # Process images
        with prog_message(
            "Processing {} images".format(len(self.info.unprocessed)),
            prog="PROCESSING",
            out_type=self.out_type,
        ):
            if self.out_type == "progress":
                self.prog_count = 0
                self.gs_prog = cmd.ProgressBar(title="PROCESSING")
            img_objects = self.run_process(iterable=self.info.unprocessed)

            proc_time = datetime.timedelta(seconds=int(time.time() - start_time))
            hours, minutes, seconds = str(proc_time).split(":")
            main_log(
                self.info.logfile,
                "Total processing time: {} hours, {} minutes, {} seconds"
                "".format(hours, minutes, seconds),
                print_tag=False,
            )

        # Run analysis if not in GUI mode
        if not "gui" in self.out_type:
            with prog_message(
                "Analyzing results", prog="ANALYSIS", out_type=self.out_type
            ):
                self.info.finished_objects = [o.obj_file for o in img_objects]
                self.run_analysis()

            if "silent" not in self.out_type:
                if self.info.have_results:
                    print("\n".join(self.info.final_table))
                    print("\n".join(self.info.uc_table))
                    print("\n".join(self.info.summary))
                else:
                    print("\n **** NO IMAGES INTEGRATED! ****")

        # Determine total runtime
        if not "gui" in self.out_type:
            runtime = datetime.timedelta(seconds=int(time.time() - start_time))
            hours, minutes, seconds = str(runtime).split(":")
            main_log(
                self.info.logfile,
                "Total run time: {} hours, {} minutes, {} seconds"
                "".format(hours, minutes, seconds),
                print_tag=True,
            )


# ============================================================================ #
def entry_point():
    from iota.components.iota_init import initialize_interface, initialize_new_run

    args, phil_args = parse_command_args().parse_known_args()

    if args.run_path:
        from iota.components.iota_base import ProcInfo

        info = ProcInfo.from_folder(args.run_path[0])
        proc = Process.for_existing_run(info=info, out_type=args.out_type[0])
    else:
        if args.out_type == "progress":
            print(logo)

        if not args.path:
            parse_command_args().print_help()  # Print usage
            if args.default:  # Write out default params and exit
                from iota.components.iota_input import print_params

                help_out, txt_out = print_params()
                print("\n{:-^70}\n".format("IOTA Parameters"))
                print(help_out)
                iota_exit()

        with prog_message("Interpreting input", prog="UI INIT", out_type=args.out_type):
            input_dict, phil, msg = initialize_interface(args, phil_args)
            if not (input_dict or phil):
                iota_exit(silent=(args.out_type == "silent"), msg=msg)

        with prog_message(
            "Initializing run parameters", prog="PARAM INIT", out_type=args.out_type
        ):
            init_ok, info, msg = initialize_new_run(phil=phil, input_dict=input_dict)
            if not init_ok:
                iota_exit(silent=False, msg=msg)

        proc = Process.for_new_run(
            paramfile=info.paramfile, run_no=info.run_number, out_type=args.out_type
        )

    proc.run()


if __name__ == "__main__":
    entry_point()
