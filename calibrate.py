import driver
d = driver.CoreMemDriver()

d.spi_write(0, 26)

testAddr = 2

d.mem_write(testAddr, 0)

# while True:
#     print("0: %x\n" % d.mem_read(0))


while True:
    d.mem_write(testAddr, 0)
    print("0: %x\n" % d.mem_read(testAddr))
    d.mem_write(testAddr, 0xff)
    print("ff: %x\n" % d.mem_read(testAddr))