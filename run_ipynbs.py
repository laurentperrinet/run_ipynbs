#!/usr/bin/env python

"""
Strongly inspired from https://gist.github.com/minrk/2620876.

Developed under Python 3.3 but should easly work on Python 2.7.

Author: HadiM <hadrien.mary@gmail.com>
License: GPLv3
Date: 12.12.2013
Version: 1.0
Url: https://github.com/hadim/run_ipynbs

See README.md for more details : https://github.com/hadim/run_ipynbs/blob/master/README.md
"""

import os
import logging
import argparse
from queue import Empty

logformat = '%(asctime)s' + ':'
logformat += '%(levelname)s' + ':'
#logformat += '%(name)s' + ':'
# logformat += '%(funcName)s' + ': '
logformat += ' %(message)s'

log = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(logformat, "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.DEBUG)
log.propagate = False

try:
    from IPython.kernel import KernelManager
    log.info('Use standard KernelManager')
except ImportError:
    from IPython.zmq.blockingkernelmanager import BlockingKernelManager as KernelManager
    log.info('Use BlockingKernelManager')

from IPython.nbformat.current import reads, NotebookNode


def run_cell(shell, iopub, cell, output=False):

    shell.execute(cell.input)

    shell.get_msg()  # timeout=20
    outs = []

    while True:
        try:
            msg = iopub.get_msg(timeout=0.2)
        except Empty:
            break
        msg_type = msg['msg_type']
        if msg_type in ('status', 'pyin'):
            continue
        elif msg_type == 'clear_output':
            outs = []
            continue

        content = msg['content']
        out = NotebookNode(output_type=msg_type)

        if msg_type == 'stream':
            out.stream = content['name']
            out.text = content['data']

            if output:
                print(out.text, end="")

        elif msg_type in ('display_data', 'pyout'):
            out['metadata'] = content['metadata']
            for mime, data in content['data'].items():
                attr = mime.split('/')[-1].lower()
                # this gets most right, but fix svg+html, plain
                attr = attr.replace('+xml', '').replace('plain', 'text')
                setattr(out, attr, data)
            if msg_type == 'pyout':
                out.prompt_number = content['execution_count']

        elif msg_type == 'pyerr':
            out.ename = content['ename']
            out.evalue = content['evalue']
            out.traceback = content['traceback']
        else:
            log.error("Unhandled iopub msg : ", msg_type)

        outs.append(out)

    return outs


def run_notebook(nb, output=False):
    """
    """

    km = KernelManager()
    km.start_kernel(extra_arguments=['--pylab=inline'], stderr=open(os.devnull, 'w'))
    try:
        kc = km.client()
        kc.start_channels()
        iopub = kc.iopub_channel
    except AttributeError:
        # IPython 0.13
        kc = km
        kc.start_channels()
        iopub = kc.sub_channel
    shell = kc.shell_channel

    # run %pylab inline, because some notebooks assume this
    # even though they shouldn't
    shell.execute("pass")
    shell.get_msg()
    while True:
        try:
            iopub.get_msg(timeout=1)
        except Empty:
            break

    cells = 0
    failures = 0
    for ws in nb.worksheets:
        for cell in ws.cells:

            if cell.cell_type != 'code':
                continue

            log.info('Run cell #%i' % cells)
            cells += 1

            outs = run_cell(shell, iopub, cell, output=output)

            if outs and outs[0]['output_type'] == "pyerr":
                log.error('Fail to execute cell #%i\n' % cells + '\n'.join(outs[0]['traceback']))
                failures += 1
                continue

            log.info('Done')

    log.info("%i cells runned with %i cells failed" % (cells, failures))

    kc.stop_channels()
    km.shutdown_kernel()
    del km

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('ipynbs', type=str, nargs='+', help='Ipynb files you want to run')
    parser.add_argument("--output", "-o", action="store_true", help="Display cells output while they run")
    args = parser.parse_args()

    for ipynb in args.ipynbs:

        log.info("Running %s" % ipynb)
        with open(ipynb) as f:
            nb = reads(f.read(), 'json')
        run_notebook(nb, output=args.output)
