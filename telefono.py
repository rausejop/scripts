#!/usr/bin/env python
# coding: utf-8
"""
    package.module
    ~~~~~~~~~~~~~
    A description which can be long and explain the complete
    functionality of this module even with indented code examples.
    Class/Function however should not be documented here.

    :copyright: year by my name, see AUTHORS for more details
    :license: license_name, see LICENSE for more details

    PEP 8 -- Style Guide for Python Code
    https://www.python.org/dev/peps/pep-0008/

    PEP 257 -- Docstring Conventions
    https://www.python.org/dev/peps/pep-0257/

"""

__author__ = 'Joe Author (joe.author@website.org)'
__copyright__ = 'Copyright (c) 2009-2010 Joe Author'
__license__ = 'New-style BSD'
__vcs_id__ = '$Id$'
__version__ = '1.2.3' #Versioning: http://www.python.org/dev/peps/pep-0386/


#
## Code goes here.
#

def test():
    """ """
    pass


def telefono():
    import phonenumbers
    from phonenumbers import timezone,geocoder,carrier
    PhoneNumber = phonenumbers.parse("(+34) 661152794") #Numero de telefono con su prefijo
    TimeZone= timezone.time_zones_for_number(PhoneNumber)
    Carrier = carrier.name_for_number(PhoneNumber,'es')
    Region = geocoder.description_for_number(PhoneNumber,'es')
    print("Teléfono", "\t\t\t\t\t", "Zona", "\t\t\t\t\t", "Operador", "\t", "País")
    print(PhoneNumber, "\t", TimeZone, "\t", Carrier, "\t", Region)
    return 0


if __name__=='__main__':
    test()
    telefono()

