# This file is Copyright (c) 2018 William D. Jones <thor0505@comcast.net>
# License: BSD

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform, XC3SProg, VivadoProgrammer

_io = [
    ("user_led", 0, Pins("E18"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("F13"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("E13"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("H15"), IOStandard("LVCMOS33")),

    ("rgb_leds", 0,
        Subsignal("r", Pins("J15 E15")),
        Subsignal("g", Pins("G17 F18")),
        Subsignal("b", Pins("F15 E14")),
        IOStandard("LVCMOS33")
    ),

    ("user_sw", 0, Pins("H14"), IOStandard("LVCMOS33")),
    ("user_sw", 1, Pins("H18"), IOStandard("LVCMOS33")),
    ("user_sw", 2, Pins("G18"), IOStandard("LVCMOS33")),
    ("user_sw", 3, Pins("M5"), IOStandard("LVCMOS33")),

    ("user_btn", 0, Pins("G15"), IOStandard("LVCMOS33")),
    ("user_btn", 1, Pins("K16"), IOStandard("LVCMOS33")),
    ("user_btn", 2, Pins("J16"), IOStandard("LVCMOS33")),
    ("user_btn", 3, Pins("H13"), IOStandard("LVCMOS33")),

    # ("clk100", 0, Pins("R2"), IOStandard("LVCMOS33")),
    ("clk100", 0, Pins("R2"), IOStandard("SSTL135")),    

    ("cpu_reset", 0, Pins("C18"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("R12")),
        Subsignal("rx", Pins("V12")),
        IOStandard("LVCMOS33")),

    ("spi", 0,
        Subsignal("clk", Pins("G16")),
        Subsignal("cs_n", Pins("H16")),
        Subsignal("mosi", Pins("H17")),
        Subsignal("miso", Pins("K14")),
        IOStandard("LVCMOS33")
    ),

    ("spiflash_4x", 0,  # clock needs to be accessed through STARTUPE2
        Subsignal("cs_n", Pins("M13")),
        Subsignal("dq", Pins("K17", "K18", "L14", "M15")),
        IOStandard("LVCMOS33")
    ),
    ("spiflash_1x", 0,  # clock needs to be accessed through STARTUPE2
        Subsignal("cs_n", Pins("M13")),
        Subsignal("mosi", Pins("K17")),
        Subsignal("miso", Pins("K18")),
        Subsignal("wp", Pins("L14")),
        Subsignal("hold", Pins("M15")),
        IOStandard("LVCMOS33")
    ),

    ("ddram", 0,
        Subsignal("a", Pins(
            "U2 R4 V2 V4 T3 R7 V6 T6",
            "U7 V7 P6 T5 R6 U6"),
            IOStandard("SSTL135")),
        Subsignal("ba", Pins("V5 T1 U3"), IOStandard("SSTL135")),
        Subsignal("ras_n", Pins("U1"), IOStandard("SSTL135")),
        Subsignal("cas_n", Pins("V3"), IOStandard("SSTL135")),
        Subsignal("we_n", Pins("P7"), IOStandard("SSTL135")),
        Subsignal("cs_n", Pins("R3"), IOStandard("SSTL135")),
        Subsignal("dm", Pins("K4 M3"), IOStandard("SSTL135")),
        Subsignal("dq", Pins(
            "K2 K3 L4 M6 K6 M4 L5 L6",
            "N4 R1 N1 N5 M2 P1 M1 P2"),
            IOStandard("SSTL135"),
            Misc("IN_TERM=UNTUNED_SPLIT_40")),
        Subsignal("dqs_p", Pins("K1 N3"), IOStandard("DIFF_SSTL135")),
        Subsignal("dqs_n", Pins("L1 N2"), IOStandard("DIFF_SSTL135")),
        Subsignal("clk_p", Pins("R5"), IOStandard("DIFF_SSTL135")),
        Subsignal("clk_n", Pins("T4"), IOStandard("DIFF_SSTL135")),
        Subsignal("cke", Pins("T2"), IOStandard("SSTL135")),
        Subsignal("odt", Pins("P5"), IOStandard("SSTL135")),
        Subsignal("reset_n", Pins("J6"), IOStandard("SSTL135")),
        Misc("SLEW=FAST"),
    ),

    ("pmoda", 0, Pins("L17 L18 M14 N14 M16 M17 M18 N18"), IOStandard("LVCMOS33")),
    ("pmodb", 0, Pins("P17 P18 R18 T18 P14 P15 N15 P16"), IOStandard("LVCMOS33")),
    ("pmodc", 0, Pins("U15 V16 U17 U18 U16 P13 R13 V14"), IOStandard("LVCMOS33")),
    ("pmodd", 0, Pins("V15 U12 V13 T12 T13 R11 T11 U11"), IOStandard("LVCMOS33")),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk100"
    default_clk_period = 10.0

    # From https://www.xilinx.com/support/documentation/user_guides/ug470_7Series_Config.pdf
    # 17536096 bits == 2192012 == 0x21728c -- Therefore 0x220000
    # 7S50 same Configuration Bitstream Length as 7A35T
    gateware_size = 0x220000

    # Cypress 'sp s25fl128' (ID 0x00182001)
    # FIXME: Create a "spi flash module" object in the same way we have SDRAM
    # module objects.
    spiflash_model = "S25FL128S"
    spiflash_read_dummy_bits = 10
    spiflash_clock_div = 4
    spiflash_total_size = int((128/8)*1024*1024) # 128Mbit
    spiflash_page_size = 256
    spiflash_sector_size = 0x10000

    def __init__(self, toolchain="vivado", programmer="vivado"):
        XilinxPlatform.__init__(self, "xc7s50csga324-1", _io,
                                toolchain=toolchain)
        self.toolchain.bitstream_commands = \
            ["set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]"]
        self.toolchain.additional_commands = \
            ["write_cfgmem -force -format bin -interface spix4 -size 16 "
             "-loadbit \"up 0x0 {build_name}.bit\" -file {build_name}.bin"]
        self.programmer = programmer
        self.add_platform_command("set_property INTERNAL_VREF 0.675 [get_iobanks 34]")

    def create_programmer(self):
        if self.programmer == "xc3sprog":
            return XC3SProg("nexys4")
        elif self.programmer == "vivado":
            return VivadoProgrammer(flash_part="n25q128-3.3v-spi-x1_x2_x4")
        else:
            raise ValueError("{} programmer is not supported"
                             .format(self.programmer))


# # This file is Copyright (c) 2015 Yann Sionneau <yann@sionneau.net>
# # This file is Copyright (c) 2015 Florent Kermarrec <florent@enjoy-digital.fr>
# # License: BSD

# from litex.build.generic_platform import *
# from litex.build.openocd import OpenOCD
# from litex.build.xilinx import XilinxPlatform, XC3SProg, VivadoProgrammer

# _io = [
#     ("user_led", 0, Pins("H5"), IOStandard("LVCMOS33")),
#     ("user_led", 1, Pins("J5"), IOStandard("LVCMOS33")),
#     ("user_led", 2, Pins("T9"), IOStandard("LVCMOS33")),
#     ("user_led", 3, Pins("T10"), IOStandard("LVCMOS33")),

#     ("rgb_leds", 0,
#         Subsignal("r", Pins("G6 G3 J3 K1")),
#         Subsignal("g", Pins("F6 J4 J2 H6")),
#         Subsignal("b", Pins("E1 G4 H4 K2")),
#         IOStandard("LVCMOS33")
#     ),

#     ("user_sw", 0, Pins("A8"), IOStandard("LVCMOS33")),
#     ("user_sw", 1, Pins("C11"), IOStandard("LVCMOS33")),
#     ("user_sw", 2, Pins("C10"), IOStandard("LVCMOS33")),
#     ("user_sw", 3, Pins("A10"), IOStandard("LVCMOS33")),

#     ("user_btn", 0, Pins("D9"), IOStandard("LVCMOS33")),
#     ("user_btn", 1, Pins("C9"), IOStandard("LVCMOS33")),
#     ("user_btn", 2, Pins("B9"), IOStandard("LVCMOS33")),
#     ("user_btn", 3, Pins("B8"), IOStandard("LVCMOS33")),

#     ("clk100", 0, Pins("E3"), IOStandard("LVCMOS33")),

#     ("cpu_reset", 0, Pins("C2"), IOStandard("LVCMOS33")),

#     ("serial", 0,
#         Subsignal("tx", Pins("D10")),
#         Subsignal("rx", Pins("A9")),
#         IOStandard("LVCMOS33")),

#     ("spiflash_4x", 0,  # clock needs to be accessed through STARTUPE2
#         Subsignal("cs_n", Pins("L13")),
#         Subsignal("dq", Pins("K17", "K18", "L14", "M14")),
#         IOStandard("LVCMOS33")
#     ),
#     ("spiflash_1x", 0,  # clock needs to be accessed through STARTUPE2
#         Subsignal("cs_n", Pins("L13")),
#         Subsignal("mosi", Pins("K17")),
#         Subsignal("miso", Pins("K18")),
#         Subsignal("wp", Pins("L14")),
#         Subsignal("hold", Pins("M14")),
#         IOStandard("LVCMOS33")
#     ),

#     ("eth_ref_clk", 0, Pins("G18"), IOStandard("LVCMOS33")),

#     ("ddram", 0,
#         Subsignal("a", Pins(
#             "R2 M6 N4 T1 N6 R7 V6 U7",
#             "R8 V7 R6 U6 T6 T8"),
#             IOStandard("SSTL15")),
#         Subsignal("ba", Pins("R1 P4 P2"), IOStandard("SSTL15")),
#         Subsignal("ras_n", Pins("P3"), IOStandard("SSTL15")),
#         Subsignal("cas_n", Pins("M4"), IOStandard("SSTL15")),
#         Subsignal("we_n", Pins("P5"), IOStandard("SSTL15")),
#         Subsignal("cs_n", Pins("U8"), IOStandard("SSTL15")),
#         Subsignal("dm", Pins("L1 U1"), IOStandard("SSTL15")),
#         Subsignal("dq", Pins(
#             "K5 L3 K3 L6 M3 M1 L4 M2",
#             "V4 T5 U4 V5 V1 T3 U3 R3"),
#             IOStandard("SSTL15"),
#             Misc("IN_TERM=UNTUNED_SPLIT_40")),
#         Subsignal("dqs_p", Pins("N2 U2"), IOStandard("DIFF_SSTL15")),
#         Subsignal("dqs_n", Pins("N1 V2"), IOStandard("DIFF_SSTL15")),
#         Subsignal("clk_p", Pins("U9"), IOStandard("DIFF_SSTL15")),
#         Subsignal("clk_n", Pins("V9"), IOStandard("DIFF_SSTL15")),
#         Subsignal("cke", Pins("N5"), IOStandard("SSTL15")),
#         Subsignal("odt", Pins("R5"), IOStandard("SSTL15")),
#         Subsignal("reset_n", Pins("K6"), IOStandard("SSTL15")),
#         Misc("SLEW=FAST"),
#     ),

#     ("eth_clocks", 0,
#         Subsignal("tx", Pins("H16")),
#         Subsignal("rx", Pins("F15")),
#         IOStandard("LVCMOS33")
#     ),
#     ("eth", 0,
#         Subsignal("rst_n", Pins("C16")),
#         Subsignal("mdio", Pins("K13")),
#         Subsignal("mdc", Pins("F16")),
#         Subsignal("dv", Pins("G16")),
#         Subsignal("rx_er", Pins("C17")),
#         Subsignal("rx_data", Pins("D18 E17 E18 G17")),
#         Subsignal("tx_en", Pins("H15")),
#         Subsignal("tx_data", Pins("H14 J14 J13 H17")),
#         Subsignal("col", Pins("D17")),
#         Subsignal("crs", Pins("G14")),
#         IOStandard("LVCMOS33")
#     ),
# ]


# class Platform(XilinxPlatform):
#     name = "arty"
#     default_clk_name = "clk100"
#     default_clk_period = 10.0

#     # From https://www.xilinx.com/support/documentation/user_guides/ug470_7Series_Config.pdf
#     # 17536096 bits == 2192012 == 0x21728c -- Therefore 0x220000
#     gateware_size = 0x220000

#     # Micron N25Q128A13ESF40 (ID 0x0018ba20)
#     # FIXME: Create a "spi flash module" object in the same way we have SDRAM
#     # module objects.
#     spiflash_model = "n25q128a13"
#     spiflash_read_dummy_bits = 10
#     spiflash_clock_div = 4
#     spiflash_total_size = int((128/8)*1024*1024) # 128Mbit
#     spiflash_page_size = 256
#     spiflash_sector_size = 0x10000

#     def __init__(self, toolchain="vivado", programmer="openocd"):
#         XilinxPlatform.__init__(self, "xc7a35t-csg324-1", _io,
#                                 toolchain=toolchain)
#         self.toolchain.bitstream_commands = \
#             ["set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]"]
#         self.toolchain.additional_commands = \
#             ["write_cfgmem -force -format bin -interface spix4 -size 16 "
#              "-loadbit \"up 0x0 {build_name}.bit\" -file {build_name}.bin"]
#         self.programmer = programmer
#         self.add_platform_command("set_property INTERNAL_VREF 0.750 [get_iobanks 34]")

#     def create_programmer(self):
#         if self.programmer == "openocd":
#             proxy="bscan_spi_{}.bit".format(self.device.split('-')[0])
#             return OpenOCD(config="board/digilent_arty.cfg", flash_proxy_basename=proxy)
#         elif self.programmer == "xc3sprog":
#             return XC3SProg("nexys4")
#         elif self.programmer == "vivado":
#             return VivadoProgrammer(flash_part="n25q128-3.3v-spi-x1_x2_x4")
#         else:
#             raise ValueError("{} programmer is not supported"
#                              .format(self.programmer))
