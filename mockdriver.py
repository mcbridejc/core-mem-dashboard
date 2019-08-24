import time
from pyftdi.spi import SpiController
import random
from driver import CoreMemDriver

SENSEDELAY_REG = 0
CTRL_REG = 1
VTHRESH_H_REG = 2
VTHRESH_L_REG = 3
VDRIVE_H_REG = 4
VDRIVE_L_REG = 5
DATA_REG = 6
ADDR_REG = 7

CTRL_WRITE_MASK = (1<<0)
CTRL_READ_MASK = (1<<1)
CTRL_UPDATEPOT_MASK = (1<<2)

class MockCoreMemDriver(CoreMemDriver):
    def __init__(self):
        pass
    
    def read_miso(self):
        """Return the current value of the MISO input pin as a bool
        """
        return False
    
    def wait_for_not_busy(self):
        """Block until the MISO busy signal indicates the chip is ready for a transaction
        """
        # Whenever a SPI transaction is not in progress (i.e. CSn==1), the MISO signal doubles as
        # a busy inidicator. High indicates busy, and low indicates ready. The only time the 
        # chip will assert busy is after a read/write memory operation, as it cannot take another
        # command until it completes the current one. 
        return

    def spi_read(self, addr):
        """Read SPI register and return 8-bit value
        """
        return random.randint(0, 255)
            
    def spi_write(self, addr, value):
        """Write SPI register with 8-bit value
        """
        pass

   
    