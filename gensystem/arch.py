"""Map architecture to relevant files using namedtuples."""

from collections import namedtuple

Arch = namedtuple('Arch', 'name minimal stage3 hardened nomultilib')

AMD64 = Arch(
    'amd64',
    'current-install-amd64-minimal::install-amd64-minimal-\d{8}.iso$',
    'current-stage3-amd64::stage3-amd64-\d{8}.tar.bz2$',
    'current-stage3-amd64-hardened::stage3-amd64-hardened-\d{8}.tar.bz2$',
    'current-stage3-amd64-nomultilib::stage3-amd64-nomultilib-\d{8}.tar.bz2$')
