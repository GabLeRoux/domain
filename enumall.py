#!/usr/bin/env python

from __future__ import print_function

import argparse

import datetime
import os
import sys

try:
    from config import *
except ImportError:
    recon_path = "./recon-ng/"
    altdns_path = "./altdns/"

sys.path.insert(0, recon_path)
from recon.core import base

if altdns_path:
    sys.path.insert(1, altdns_path)


def run_module(reconBase, module, domain):
    x = reconBase.do_load(module)
    x.do_set("SOURCE " + domain)
    x.do_run(None)


def run_recon(domains, bruteforce, workspace):
    reconb = base.Recon(base.Mode.CLI)
    reconb.init_workspace(workspace)
    reconb.onecmd("TIMEOUT=100")
    module_list = [
        "recon/domains-hosts/bing_domain_web",
        "recon/domains-hosts/google_site_web",
        "recon/domains-hosts/netcraft",
        "recon/domains-hosts/shodan_hostname",
        "recon/netblocks-companies/whois_orgs",
        "recon/hosts-hosts/resolve"
    ]

    wordlist = bruteforce if bruteforce else os.path.join(recon_path, "data/hostnames.txt")

    for domain in domains:
        for module in module_list:
            run_module(reconb, module, domain)

        x = reconb.do_load("recon/domains-hosts/brute_hosts")
        x.do_set("WORDLIST " + wordlist)
        x.do_set("SOURCE " + domain)
        x.do_run(None)

    out_file = "FILENAME " + os.getcwd() + "/" + workspace
    x = reconb.do_load("reporting/csv")
    x.do_set(out_file + ".csv")
    x.do_run(None)

    x = reconb.do_load("reporting/list")
    x.do_set(out_file + ".lst")
    x.do_set("COLUMN host")
    x.do_run(None)


def get_default_workspace():
    stamp = datetime.datetime.now().strftime('%M:%H-%m_%d_%Y')
    return domain_list[0] + stamp


parser = argparse.ArgumentParser()
parser.add_argument("-a", dest="run_altdns", action="store_true",
                    help="After recon-ng, run altdns? (this requires altdns)")
parser.add_argument("-i", dest="filename", type=argparse.FileType('r'),
                    help="input file of domains (one per line)",
                    default=None)
parser.add_argument("domains", help="one or more domains", nargs="*", default=None)
parser.add_argument("-w", dest="wordlist", type=argparse.FileType('r'),
                    help="input file of subdomain wordlist. must be in same directory as this file, or give full path",
                    default=None)
parser.add_argument("-p", dest="permlist", type=argparse.FileType('r'),
                    help="input file of permutations for altdns. if none specified will use default list.",
                    default=None)
parser.add_argument("-b", dest="workspace", type=str,
                    help="workspace name passed to recon-ng",
                    default=None)
args = parser.parse_args()

if args.run_altdns and not os.path.isdir(altdns_path):
    print("Error: no altdns path specified, please download from: https://github.com/infosec-au/altdns and set "
          "aldns_path in config.py")
    exit(0)

domain_list = []

if args.domains:
    domain_list += args.domains

if args.filename:
    lines = args.filename.readlines()
    lines = [line.rstrip('\n') for line in lines]
    domain_list += lines

bruteforce_list = args.wordlist.name if args.wordlist else ""

workspace = args.workspace if args.workspace else get_default_workspace()

run_recon(domain_list, bruteforce_list, workspace)

if args.run_altdns:
    altdns_command = "python " + os.path.join(altdns_path, "altdns.py")
    subdomains = os.path.join(os.getcwd(), workspace + ".lst")
    perm_list = args.permlist.name if args.permlist else os.path.join(altdns_path, "words.txt")
    output = os.path.join(os.getcwd(), workspace + "_output.txt")
    print("running altdns... please be patient :) results will be displayed in " + output)
    # python altdns.py -i subdomainsList -o data_output -w permutationsList -r -s results_output.txt
    os.system('%s -i %s -o data_output -w %s -r -s %s' % (altdns_command, subdomains, perm_list, output))
