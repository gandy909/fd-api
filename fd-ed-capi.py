#!/usr/bin/env python3
# vim: textwidth=0 wrapmargin=0 tabstop=2 shiftwidth=2 softtabstop=2 smartindent smarttab

import os
import time
import yaml, logging, argparse

import requests
import pprint
pp = pprint.PrettyPrinter(indent=2, width=10000)

import org.miggy.edcapi

###########################################################################
"""
 "  Configuration
"""
###########################################################################
__configfile_fd = os.open("fd-api-config.yaml", os.O_RDONLY)
__configfile = os.fdopen(__configfile_fd)
__config = yaml.load(__configfile, Loader=yaml.CLoader)
###########################################################################

###########################################################################
# Logging
###########################################################################
os.environ['TZ'] = 'UTC'
time.tzset()
__default_loglevel = logging.INFO
__logger = logging.getLogger('fd-api')
__logger.setLevel(__default_loglevel)
__logger_ch = logging.StreamHandler()
__logger_ch.setLevel(__default_loglevel)
__logger_formatter = logging.Formatter('%(asctime)s;%(name)s;%(levelname)s;%(module)s.%(funcName)s: %(message)s')
__logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S';
__logger_formatter.default_msec_format = '%s.%03d'
__logger_ch.setFormatter(__logger_formatter)
__logger.addHandler(__logger_ch)
###########################################################################

###########################################################################
# Command-Line Arguments
###########################################################################
__parser = argparse.ArgumentParser()
__parser.add_argument("--loglevel", help="set the log level to one of: DEBUG, INFO (default), WARNING, ERROR, CRITICAL")
__parser.add_argument("--rawoutput", action="store_true", help="Output raw returned data")

__parser_endpoints = __parser.add_mutually_exclusive_group(required=True)
__parser_endpoints.add_argument("--profile", action="store_true", help="Request retrieval of Cmdr's profile")
__parser_endpoints.add_argument("--market", action="store_true", help="Request retrieval of market data")
__parser_endpoints.add_argument("--shipyard", action="store_true", help="Request retrieval of shipyard data")
__parser_endpoints.add_argument("--fleetcarrier", action="store_true", help="Request retrieval of fleetcarrier data")
__parser_endpoints.add_argument("--journal", action="store_true", help="Request retrieval of journal data")

__parser.add_argument("cmdrname", nargs=1, help="Specify the Cmdr Name for this Authorization")
__args = __parser.parse_args()
if __args.loglevel:
  __level = getattr(logging, __args.loglevel.upper())
  __logger.setLevel(__level)
  __logger_ch.setLevel(__level)
cmdrname = __args.cmdrname[0]
###########################################################################

###########################################################################
# Load a relevant Auth State
###########################################################################
def loadAuthState(cmdr: str) -> int:
  ########################################
  # Retrieve and test state
  ########################################
  db = edcapi.database(__logger, __config)
  auth_state = db.getActiveTokenState()
  if auth_state:
    ## Do we have an access_token, and does it work?
    if auth_state['access_token']:
      print("Found un-expired access_token, assuming it's good.")
      return(0)
    else:
      print("Un-expired access_token, but no access_token? WTF!")
      return(-1)
  else:
    print("No auth state with un-expired access_token found, continuing...")
  ########################################
###########################################################################

###########################################################################
# Main
###########################################################################
def main():
  __logger.debug("Start")

  capi = org.miggy.edcapi.edcapi(__logger, __config)

  if __args.profile:
    (rawprofile, profile) = capi.profile.get(cmdrname)
    if not profile:
      return(-1)

    if __args.rawoutput:
      print(rawprofile)
      print('')
    else:
      print(pp.pformat(profile))

  if __args.market:
    (rawmarket, market) = capi.market.get(cmdrname)
    if not market:
      return(-1)

    if __args.rawoutput:
      print(rawmarket)
      print('')
    else:
      print(pp.pformat(market))

  if __args.shipyard:
    (rawshipyard, shipyard) = capi.shipyard.get(cmdrname)
    if not shipyard:
      return(-1)

    if __args.rawoutput:
      print(rawshipyard)
      print('')
    else:
      print(pp.pformat(shipyard))

  if __args.fleetcarrier:
    (rawfleetcarrier, fleetcarrier) = capi.fleetcarrier.get(cmdrname)
    if not fleetcarrier:
      return(-1)

    if __args.rawoutput:
      print(rawfleetcarrier)
      print('')
    else:
      print(pp.pformat(fleetcarrier))

  if __args.journal:
    rawjournal = capi.journal.get(cmdrname)
    if not rawjournal:
      return(-1)

    print('{journal}\n'.format(journal=rawjournal))

###########################################################################
if __name__ == '__main__':
  exit(main())
