import argparse
import sys

from libreselery.configuration import LibreSeleryConfig
from libreselery import libreselery


def runCli():
    args = _parseArgs()
    args.func(args)


def _runCommand(args):
    # apply args dict to config
    config = LibreSeleryConfig()
    config.apply(vars(args).items())
    # instantiate libreselery and
    # let it initialize configurations,
    # arguments and environments
    selery = libreselery.LibreSelery(config)
    # let libreselery connect to
    # various APIs and servers to
    # allow data gathering
    selery.connect()
    # let libreselery gather data
    # of all involved projects,
    # dependencies and contributors
    (
        mainProjects,
        mainContributors,
        dependencyProjects,
        dependencyContributors,
    ) = selery.gather()
    # please modify the weights
    # calculation to your need
    combined_weights, combined_contributors = selery.weight(
        mainProjects, mainContributors, dependencyProjects, dependencyContributors
    )
    # split between contributors
    # who should receive payout
    recipients, contributor_payout_split = selery.split(
        combined_contributors, combined_weights
    )
    # let libreselery use the given
    # address containing virtual currency
    # to pay out the selected contributors
    receipt, transaction = selery.payout(recipients, contributor_payout_split)
    # visualize the generated transaction data
    # generates images with charts/diagram in
    # the results folder
    selery.visualize(receipt, transaction)
    ### finish libreselery by checking processed information
    selery.finish(receipt)
    # Done.


def _initCommand(args):
    print("Initializing new LibreSelery project")

    config = LibreSeleryConfig()

    config.bitcoin_address = input("Enter your public bitcoin address: ")
    if not config.bitcoin_address:
        print("Invalid bitcoin address")
        exit(-1)

    config.writeYaml("./selery.yml")


def _parseArgs():
    parser = argparse.ArgumentParser(description="libreselery - Automated Funding")
    subparsers = parser.add_subparsers()

    # create the parser for the "init" command
    parser_init = subparsers.add_parser("init", help="init --help")
    parser_init.set_defaults(func=_initCommand)

    # create the parser for the "run" command
    parser_run = subparsers.add_parser("run", help="run --help")
    parser_run.add_argument(
        "-C",
        "--config-dir",
        required=False,
        default="",
        dest="config_dir",
        type=str,
        help="Add all configs from configuration directory",
    )
    parser_run.add_argument(
        "-c",
        "--config",
        required=False,
        dest="config_paths",
        nargs="+",
        default=[],
        help="Add configuration file path",
    )
    parser_run.add_argument(
        "-d", "--directory", required=True, type=str, help="Git directory to scan"
    )
    parser_run.add_argument(
        "-r",
        "--results_dir",
        required=True,
        type=str,
        help="Result directory",
        dest="result_dir",
    )
    parser_run.add_argument(
        "-t",
        "--tooling",
        required=False,
        type=str,
        help="Tooling file path",
        dest="tooling_path",
    )
    parser_run.set_defaults(func=_runCommand)

    args = parser.parse_args()
    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit()
    return args


if __name__ == "__main__":
    runCli()
