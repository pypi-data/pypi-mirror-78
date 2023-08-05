#!/usr/bin/env python3
from libra_client.cli.color import set_force_color, bcolors, print_color
from libra_client.cli.ledger_cmds import LedgerCmd
from libra_client.cli.wallet_cmds import WalletCmd
from libra_client.cli.transaction_cmds import TransactionCmd
from libra_client.cli.account_cmds import AccountCmd
from libra_client.cli.command import get_commands_alias, report_error, print_commands
from libra_client.client import NETWORKS
from libra_client import Client
from libra.version import version
import argparse
import sys
import signal


TESTNET = NETWORKS['testnet']['url']


def get_commands(include_dev: bool):
    commands = [AccountCmd(), TransactionCmd(), WalletCmd(), LedgerCmd()]
    return get_commands_alias(commands)


def run_cmd(args):
    if args.color == 'always':
        set_force_color(True)
    if args.color == 'never':
        set_force_color(False)
    (commands, alias_to_cmd) = get_commands(args.url != TESTNET)
    if args.help or len(args.command) == 0:
        print_help(commands)
        return
    cmd = alias_to_cmd.get(args.command[0])
    if cmd is None:
        report_error(f"command `{args.command[0]}` does not exsits.")
        print_help(commands)
        return
    client = Client.new(args.url, args.faucet_account_file)
    client.verbose = args.verbose
    # TODO: some cmd doesn't need client to be initialized.
    cmd.execute(client, args.command)


def get_parser():
    parser = argparse.ArgumentParser(prog='libra', add_help=False)
    parser.add_argument('-h', "--help", action='store_true', default=False)
    parser.add_argument('-u', "--url", default=TESTNET)
    parser.add_argument('-m', "--faucet_account_file")
    parser.add_argument('-v', "--verbose", action='store_true', default=False)
    parser.add_argument('-V', '--version', action='version', version=f'libra {version}')
    parser.add_argument('-c', '--color', choices=['always', 'auto', 'never'], default='auto')
    parser.add_argument('command', nargs='*')
    return parser


def print_help(commands):
    print("USAGE: ")
    print_color("\tlibra", bcolors.OKGREEN, end='')
    print_color(" [options]", bcolors.OKBLUE, end='')
    print_color(" command", bcolors.OKGREEN, end='')
    print_color(" [command parameters ...]", bcolors.OKBLUE)
    print("\nOptional arguments:\n")
    print_color(" -u | --url", bcolors.OKBLUE, end='')
    print(" URL  Host address/name to connect to.", end='')
    print_color(" [default:testnet]", bcolors.WARNING)
    print_color(" -v | --verbose", bcolors.OKBLUE, end='')
    print(" Verbose output")
    print_color(" -V | --version", bcolors.OKBLUE, end='')
    print(" Show program's version number and exit")
    print_color(" -h | --help", bcolors.OKBLUE, end='')
    print(" Show this help message and exit")
    print("\nUse the following commands:\n")
    print_commands(commands)
    print("")


def handler(signum, frame):
    sys.exit(0)


def main():
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)
    parser = get_parser()
    argv = sys.argv[1:]
    if not sys.stdin.isatty():
        argv.extend(sys.stdin.read().strip().split())
    libra_args = parser.parse_args(argv)
    try:
        run_cmd(libra_args)
    except Exception as err:
        report_error("some error occured", err, libra_args.verbose)


if __name__ == '__main__':
    main()
