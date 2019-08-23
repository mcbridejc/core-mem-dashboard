import time
from pyftdi.spi import SpiController

CTRL_REG = 1
DATA_REG = 6
ADDR_REG = 7

CTRL_WRITE_MASK = (1<<0)
CTRL_READ_MASK = (1<<1)
CTRL_UPDATEPOT_MASK = (1<<2)

class CoreMemDriver(object):
    def __init__(self):
        # Instanciate a SPI controller
        self._spi = SpiController()
        # Configure the first interface (IF/1) of the FTDI device as a SPI master
        self._spi.configure('ftdi://ftdi:2232h/2')

        # Get a SPI port to a SPI slave w/ /CS on A*BUS3 and SPI mode 0 @ 12MHz
        self._slave = self._spi.get_port(cs=1, freq=500e3, mode=0)
    
    def spi_read(self, addr):
        """Read SPI register and return 8-bit value
        """
        read = self._slave.exchange([addr], 1)
        return read[0]
    
    def spi_write(self, addr, value):
        """Write SPI register with 8-bit value
        """
        self._slave.exchange([0x80 + addr, value])

    def mem_read(self, addr):
        """Read a byte of memory data
        """
        self.spi_write(ADDR_REG, addr)
        self.spi_write(CTRL_REG, CTRL_WRITE_MASK)
        # TODO: Poll busy
        time.sleep(1)
        return self.spi_read(DATA_REG)

    def mem_write(self, addr, value):
        """Write a byte of memory data
        """
        pass

    def set_vdrive(self, value):
        """Set the VDRIVE digital pot value

        value is 16-bit
        """
        pass

    def set_vthresh(self, value):
        """Set the VTHRESH digital pot value
        
        value is 16-bit
        """
        pass

    def set_sensedelay(self, value):
        """Set the SENSEDELAY register value

        value is 8-bit
        """
        pass
        
    def updatepot(self):
        """Trigger a write to digital pot

        This must be called after changing vdrive or vthresh to flush the new
        value out to the digital pot. 
        """
        pass

    