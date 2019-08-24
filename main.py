
import click

from app import run_server

from driver import CoreMemDriver
from mockdriver import MockCoreMemDriver

@click.command()
def main():
    print("Creating CoreMemDriver...")
    spi_driver = CoreMemDriver()
    #spi_driver = MockCoreMemDriver()
    print("Done")

    run_server(spi_driver)

if __name__ == '__main__':
    main()
