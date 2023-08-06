#!/usr/bin/env python3

import argparse
import logging
import sys

from sipyco.pc_rpc import simple_server_loop
from sipyco import common_args

from DP700 import driver

logger = logging.getLogger(__name__)

class PSU(driver.DP700):
    """Class for providing remote functionality of DP700 series power supplies.

    Inherits all methods of :class:`DP700`
    A :class:`PSU` instance can be initialized using the desired port.
    If no serial number is specified, it connects to the port specified by the "self.port" variable.

    :param port: Serial port (Uses pySerial serial_for_url)
    :port type: str
    """

    def __init__(self, port):
        """Constructor method
        """
        self.port = port
        super().__init__(self.port)


def get_argparser():
    parser = argparse.ArgumentParser(description="""Rigol DP700 controller.

    Use this controller to drive DP700 series power supplies.""")
    common_args.simple_network_args(parser, 3251)
    parser.add_argument("-s", "--serialPort", default=None,
                        help="Serial port. See documentation for how to specify port.")
    common_args.verbosity_args(parser)
    return parser


def main():
    args = get_argparser().parse_args()
    common_args.init_logger_from_args(args)

    if not args.serialPort:
        print("You need to specify -s")
        sys.exit(1)

    psu = PSU(args.serialPort)
    
    try:
        logger.info("DP700 open. Serving...")
        simple_server_loop({"DP700": psu}, common_args.bind_address_from_args(args), args.port)
    finally:
        psu.close()

if __name__ == "__main__":
    main()