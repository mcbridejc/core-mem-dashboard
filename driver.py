import time
from pyftdi.spi import SpiController
import datetime

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

class CoreMemDriver(object):
    def __init__(self):
        # Instanciate a SPI controller
        self._spi = SpiController()
        # Configure the first interface (IF/1) of the FTDI device as a SPI master
        self._spi.configure('ftdi://ftdi:2232h/2')

        # Get a SPI port to a SPI slave w/ /CS on A*BUS3 and SPI mode 0 @ 12MHz
        self._slave = self._spi.get_port(cs=1, freq=500e3, mode=0)
    
    def read_miso(self):
        """Return the current value of the MISO input pin as a bool
        """
        # MISO is on D2 bit of port
        if self._spi.read_gpio() & (1<<2):
            return True
        else:
            return False
    
    def wait_for_not_busy(self):
        """Block until the MISO busy signal indicates the chip is ready for a transaction
        """
        # Whenever a SPI transaction is not in progress (i.e. CSn==1), the MISO signal doubles as
        # a busy inidicator. High indicates busy, and low indicates ready. The only time the 
        # chip will assert busy is after a read/write memory operation, as it cannot take another
        # command until it completes the current one. 

        MAXWAIT = 0.5 # time to wait in seconds
        timeout = time.monotonic() + MAXWAIT
        while time.monotonic() < timeout:
            time.sleep(0.01)
            if not self.read_miso():
                return
            
        raise RuntimeError("Timeout waiting for BUSY signal to go low")
        

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
        self.wait_for_not_busy()
        self.spi_write(ADDR_REG, addr)
        self.spi_write(CTRL_REG, CTRL_READ_MASK)
        self.wait_for_not_busy()
        return self.spi_read(DATA_REG)

    def mem_write(self, addr, value):
        """Write a byte of memory data
        """
        self.wait_for_not_busy()
        self.spi_write(ADDR_REG, addr)
        self.spi_write(DATA_REG, value)
        self.spi_write(CTRL_REG, CTRL_WRITE_MASK)
        

    def set_vdrive(self, value):
        """Set the VDRIVE digital pot value

        value is 16-bit
        """
        self.spi_write(VDRIVE_H_REG, value >> 8)
        self.spi_write(VDRIVE_L_REG, value & 0xff)

    def read_vdrive(self):
        value = 0
        value += self.spi_read(VDRIVE_H_REG) << 8
        value += self.spi_read(VDRIVE_L_REG)
        return value

    def set_vthresh(self, value):
        """Set the VTHRESH digital pot value
        
        value is 16-bit
        """
        self.spi_write(VTHRESH_H_REG, value >> 8)
        self.spi_write(VTHRESH_L_REG, value & 0xff)

    def read_vthresh(self):
        value = 0
        value += self.spi_read(VTHRESH_H_REG) << 8
        value += self.spi_read(VTHRESH_L_REG)
        return value

    def set_sensedelay(self, value):
        """Set the SENSEDELAY register value

        value is 8-bit
        """
        self.spi_write(SENSEDELAY_REG, value)

    def read_sensedelay(self):
        return self.spi_read(SENSEDELAY_REG)
        
    def updatepot(self):
        """Trigger a write to digital pot

        This must be called after changing vdrive or vthresh to flush the new
        value out to the digital pot. 
        """
        self.wait_for_not_busy()
        self.spi_write(CTRL_REG, CTRL_UPDATEPOT_MASK)