# Mapping of string to driver for async device drivers

import dali.driver.hid

drivers = {
    "tridonic": dali.driver.hid.tridonic,
    "hasseb": dali.driver.hid.hasseb,
    "hasseb2": dali.driver.hid.hasseb2,
}
