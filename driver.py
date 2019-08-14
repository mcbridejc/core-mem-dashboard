def CoreMemDriver(object):
    def __init__(self):
        pass
    
    def spi_read(self, addr):
        """Read SPI register and return 8-bit value
        """
        pass
    
    def spi_write(self, addr, value):
        """Write SPI register with 8-bit value
        """
        pass

    def mem_read(self, addr):
        """Read a byte of memory data
        """
        pass

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

    