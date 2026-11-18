"""Meridian IP-1 main controller board (HYPOTHETICAL device): parts, placement and netlist as plain data.
100 x 80 mm, 4 layers. Functions: 24 V input protection, 5 V buck, 3.3 V LDO, STM32F103 MCU, TMC2226 stepper driver for the
peristaltic pump motor, low-side drivers for the solenoid pinch valve and fan, ADS1220 24-bit ADC for two bridge pressure
transducers, optical bubble-sensor interface, motor NTC, RS-485 link to the display board, EEPROM for calibration.
Each part: ref -> (footprint, value, x_mm, y_mm, rot_deg).  Each net: name -> ["REF.pad", ...]
"""
R, C6, C12, C1210, L6 = "Resistor_SMD:R_0603_1608Metric", "Capacitor_SMD:C_0603_1608Metric", "Capacitor_SMD:C_1206_3216Metric", "Capacitor_SMD:C_1210_3225Metric", "Inductor_SMD:L_0603_1608Metric"
VH2, VH4 = "Connector_JST:JST_VH_B2P-VH_1x02_P3.96mm_Vertical", "Connector_JST:JST_VH_B4P-VH_1x04_P3.96mm_Vertical"
PH2, PH4 = "Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical", "Connector_JST:JST_PH_B4B-PH-K_1x04_P2.00mm_Vertical"
SOIC8, SOT23, SMA, SMB, LED = "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm", "Package_TO_SOT_SMD:SOT-23", "Diode_SMD:D_SMA", "Diode_SMD:D_SMB", "LED_SMD:LED_0603_1608Metric"
CPR = "Capacitor_THT:CP_Radial_D8.0mm_P3.50mm"
MH = "MountingHole:MountingHole_3.2mm_M3_Pad"

PARTS = {
 # --- 24 V input and protection (bottom-left) ---
 "J1": (VH2, "24V IN", 6.5, 62.0, 90), "F1": ("Fuse:Fuse_1812_4532Metric", "PTC 3A", 15.5, 70.5, 0), "D1": (SMB, "SMBJ28A", 15.5, 75.5, 180),
 "D2": (SMB, "B340", 24.5, 70.5, 0), "C1": (CPR, "220u 35V", 33.5, 73.0, 0), "C2": (C1210, "10u 50V", 41.5, 72.0, 90), "C3": (C6, "100n", 45.0, 72.0, 90),
 # --- 5 V buck and 3.3 V LDO (bottom-middle) ---
 "U1": ("Package_TO_SOT_SMD:SOT-23-6", "TPS54202", 44.0, 63.5, 0), "C7": (C1210, "10u 50V", 38.5, 63.5, 90), "C4": (C6, "100n", 48.6, 63.0, 90),
 "R1": (R, "100k", 40.0, 59.0, 0), "R2": (R, "22k", 44.0, 59.0, 0), "L1": ("Inductor_SMD:L_Bourns_SRR1260", "10u 5A", 56.5, 66.0, 0),
 "R3": (R, "100k", 48.0, 68.0, 0), "R4": (R, "13.3k", 48.0, 70.0, 0), "C5": (C12, "22u", 66.5, 62.5, 90), "C6": (C12, "22u", 69.5, 62.5, 90),
 "U2": ("Package_TO_SOT_SMD:SOT-223-3_TabPin2", "AMS1117-3.3", 68.0, 71.0, 0), "C8": (C12, "10u", 62.5, 76.0, 0), "C9": (C12, "22u", 75.5, 71.0, 90),
 # --- stepper driver for the pump motor (left) ---
 "U4": ("Package_SO:HTSSOP-28-1EP_4.4x9.7mm_P0.65mm_EP2.75x6.2mm_ThermalVias", "TMC2226", 27.0, 30.0, 90), "J3": (VH4, "PUMP MOTOR", 6.5, 25.0, 90),
 "C19": (CPR, "100u 35V", 11.5, 43.5, 0), "C20": (C6, "100n", 24.6, 36.5, 0), "C21": (C6, "100n", 24.6, 23.5, 0), "R7": ("Resistor_SMD:R_1206_3216Metric", "0R11", 20.5, 23.5, 180),
 "R8": ("Resistor_SMD:R_1206_3216Metric", "0R11", 20.5, 36.5, 180), "C22": (C6, "22n", 27.8, 36.5, 0), "C23": (C6, "100n", 31.0, 36.5, 180), "C24": (C12, "2u2", 35.2, 36.5, 0),
 "C25": (C6, "100n", 31.8, 23.5, 0), "R9": (R, "10k", 38.6, 33.0, 90), "R10": (R, "1k", 35.4, 23.5, 0), "R11": (R, "10k", 28.2, 23.5, 0), "R12": (R, "20k", 28.2, 21.3, 0),
 # --- valve and fan drivers (top-left) ---
 "J4": (VH2, "PINCH VALVE", 20.0, 6.5, 0), "Q1": (SOT23, "AO3400A", 31.0, 13.0, 0), "D3": (SMA, "SS34", 31.5, 7.0, 0), "R13": (R, "100R", 35.5, 12.0, 90), "R14": (R, "100k", 35.5, 16.0, 90),
 "J9": (PH2, "FAN", 40.0, 5.0, 0), "Q2": (SOT23, "AO3400A", 43.0, 13.0, 0), "D4": (SMA, "SS34", 47.0, 8.5, 90), "R15": (R, "100R", 47.0, 14.0, 90), "R16": (R, "100k", 49.5, 14.0, 90),
 # --- MCU (centre) ---
 "U3": ("Package_QFP:LQFP-48_7x7mm_P0.5mm", "STM32F103C8T6", 58.0, 36.0, 0), "Y1": ("Crystal:Crystal_SMD_5032-2Pin_5.0x3.2mm", "8MHz", 47.5, 30.0, 90),
 "C17": (C6, "18p", 44.0, 27.5, 90), "C18": (C6, "18p", 44.0, 32.5, 90), "C10": (C6, "100n", 51.0, 42.5, 0), "C11": (C6, "100n", 65.0, 42.5, 0), "C12": (C6, "100n", 65.0, 29.5, 0),
 "C13": (C6, "100n", 51.0, 37.0, 90), "C14": (C6, "1u", 51.0, 24.5, 0), "C15": (C12, "4u7", 58.0, 45.5, 0), "FB1": (L6, "600R", 55.0, 24.5, 0),
 "R5": (R, "10k", 47.0, 37.0, 90), "C16": (C6, "100n", 47.0, 41.0, 90), "SW1": ("Button_Switch_SMD:SW_SPST_TL3342", "RESET", 42.0, 46.5, 0), "R6": (R, "10k", 62.0, 27.0, 0),
 "R32": (R, "10k", 55.0, 47.5, 0), "J10": ("Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical", "SWD", 94.5, 27.0, 0),
 # --- pressure ADC and sensor connectors (top-right) ---
 "U5": ("Package_SO:TSSOP-16_4.4x5mm_P0.65mm", "ADS1220", 77.0, 17.0, 0), "J5": (PH4, "PRESSURE IN", 64.0, 5.0, 0), "J6": (PH4, "PRESSURE OUT", 78.0, 5.0, 0),
 "R17": (R, "1k", 68.0, 11.0, 90), "R18": (R, "1k", 70.5, 11.0, 90), "C28": (C6, "100n", 70.5, 15.0, 0), "R19": (R, "1k", 81.5, 10.5, 90), "R20": (R, "1k", 84.0, 10.5, 90),
 "C29": (C6, "100n", 83.5, 14.5, 0), "C26": (C6, "100n", 83.5, 17.5, 0), "C27": (C6, "100n", 83.5, 20.0, 0),
 # --- bubble sensor, NTC, 24 V monitor ---
 "J7": (PH4, "BUBBLE", 52.0, 5.0, 0), "R21": (R, "150R", 56.0, 12.0, 90), "R22": (R, "10k", 58.5, 12.0, 90), "C30": (C6, "10n", 61.0, 12.0, 90),
 "J8": (PH2, "MOTOR NTC", 92.0, 5.0, 0), "R23": (R, "10k", 90.5, 12.0, 90), "C31": (C6, "100n", 93.0, 12.0, 90),
 "R24": (R, "100k", 40.5, 52.5, 0), "R25": (R, "10k", 44.5, 52.5, 0), "C32": (C6, "100n", 48.5, 52.5, 0),
 # --- RS-485 to the display board, EEPROM, LEDs (right) ---
 "U6": (SOIC8, "MAX3485", 84.0, 60.0, 0), "C33": (C6, "100n", 84.0, 54.5, 0), "R26": (R, "120R", 90.5, 60.0, 90), "J11": (PH4, "UI RS485", 86.0, 75.0, 180),
 "U7": (SOIC8, "24LC256", 84.0, 44.0, 0), "C34": (C6, "100n", 84.0, 38.5, 0), "R27": (R, "4k7", 76.0, 42.0, 90), "R28": (R, "4k7", 73.5, 42.0, 90),
 "D5": (LED, "GRN PWR", 72.0, 51.0, 0), "R29": (R, "1k", 68.0, 51.0, 0), "D6": (LED, "GRN RUN", 72.0, 54.0, 0), "R30": (R, "1k", 68.0, 54.0, 0), "D7": (LED, "RED FAULT", 72.0, 57.0, 0), "R31": (R, "1k", 68.0, 57.0, 0),
 "H1": (MH, "M3", 4.0, 4.0, 0), "H2": (MH, "M3", 96.0, 20.0, 0), "H3": (MH, "M3", 4.0, 76.0, 0), "H4": (MH, "M3", 96.0, 76.0, 0),
}

N = {}
def net(name, *pads): N.setdefault(name, []).extend(pads)
# power entry
net("+24V_IN", "J1.1", "F1.1"); net("VFUSE", "F1.2", "D1.1", "D2.2")
net("+24V", "D2.1", "C1.1", "C2.1", "C3.1", "U1.3", "C7.1", "R1.1", "U4.3", "U4.26", "C19.1", "C20.1", "C21.1", "C23.1", "J4.1", "D3.1", "J9.1", "D4.1", "R24.1")
# buck 24 V -> 5 V
net("BUCK_EN", "R1.2", "R2.1", "U1.5"); net("BUCK_SW", "U1.2", "C4.2", "L1.1"); net("BUCK_BOOT", "U1.6", "C4.1"); net("BUCK_FB", "U1.4", "R3.2", "R4.1")
net("+5V", "L1.2", "R3.1", "C5.1", "C6.1", "U2.3", "C8.1", "J11.1")
net("+3V3", "U2.2", "C9.1", "U3.24", "U3.36", "U3.48", "U3.1", "C10.1", "C11.1", "C12.1", "C13.1", "C15.1", "FB1.1", "R5.1", "R9.1", "U4.19", "C25.1", "U5.13", "C27.1",
    "J7.1", "R22.1", "U6.8", "C33.1", "U7.8", "C34.1", "R27.1", "R28.1", "R29.1", "R30.1", "J10.1")
net("+3V3A", "FB1.2", "C14.1", "U3.9", "U5.12", "C26.1", "U5.9", "J5.1", "J6.1", "R23.1")
# MCU support
net("NRST", "U3.7", "R5.2", "C16.1", "SW1.1", "J10.4"); net("BOOT0", "U3.44", "R6.1"); net("BOOT1", "U3.20", "R32.1")
net("OSC_IN", "U3.5", "Y1.1", "C17.1"); net("OSC_OUT", "U3.6", "Y1.2", "C18.1"); net("SWDIO", "U3.34", "J10.2"); net("SWCLK", "U3.37", "J10.3")
# stepper driver
net("MOT_A1", "U4.28", "J3.1"); net("MOT_A2", "U4.25", "J3.2"); net("MOT_B1", "U4.1", "J3.3"); net("MOT_B2", "U4.4", "J3.4")
net("SENSE_A", "U4.27", "R7.1"); net("SENSE_B", "U4.2", "R8.1"); net("CP_O", "U4.7", "C22.1"); net("CP_I", "U4.8", "C22.2"); net("VCP", "U4.9", "C23.2")
net("DRV_5V", "U4.11", "C24.1", "R11.1"); net("DRV_VREF", "U4.21", "R11.2", "R12.1")
net("DRV_EN_N", "U4.5", "R9.2", "U3.25"); net("DRV_STEP", "U4.20", "U3.29"); net("DRV_DIR", "U4.23", "U3.26")
net("DRV_UART", "U4.18", "R10.1", "U3.22"); net("DRV_UART_TX", "R10.2", "U3.21"); net("DRV_DIAG", "U4.15", "U3.27"); net("DRV_INDEX", "U4.16", "U3.28")
# valve and fan
net("VALVE_G", "Q1.1", "R13.2", "R14.1"); net("VALVE_CTL", "R13.1", "U3.11"); net("VALVE_N", "Q1.3", "D3.2", "J4.2")
net("FAN_G", "Q2.1", "R15.2", "R16.1"); net("FAN_CTL", "R15.1", "U3.12"); net("FAN_N", "Q2.3", "D4.2", "J9.2")
# pressure ADC (SPI1) and transducer inputs
net("ADC_SCK", "U5.1", "U3.15"); net("ADC_MISO", "U5.15", "U3.16"); net("ADC_MOSI", "U5.16", "U3.17"); net("ADC_CS_N", "U5.2", "U3.14"); net("ADC_DRDY_N", "U5.14", "U3.18")
net("P1P_IN", "J5.2", "R17.1"); net("P1N_IN", "J5.3", "R18.1"); net("P1P", "R17.2", "C28.1", "U5.11"); net("P1N", "R18.2", "C28.2", "U5.10")
net("P2P_IN", "J6.2", "R19.1"); net("P2N_IN", "J6.3", "R20.1"); net("P2P", "R19.2", "C29.1", "U5.7"); net("P2N", "R20.2", "C29.2", "U5.6")
# bubble sensor, NTC, 24 V monitor
net("BUB_LED_K", "J7.2", "R21.1"); net("BUB_LED_DRV", "R21.2", "U3.41"); net("BUB_SIG", "J7.3", "R22.2", "C30.1", "U3.13")
net("NTC", "J8.1", "R23.2", "C31.1", "U3.10"); net("VMON", "R24.2", "R25.1", "C32.1", "U3.19")
# RS-485, EEPROM, LEDs
net("RS485_RO", "U6.1", "U3.31"); net("RS485_DI", "U6.4", "U3.30"); net("RS485_DE", "U6.2", "U6.3", "U3.32"); net("RS485_A", "U6.6", "R26.1", "J11.2"); net("RS485_B", "U6.7", "R26.2", "J11.3")
net("I2C_SDA", "U7.5", "R27.2", "U3.43"); net("I2C_SCL", "U7.6", "R28.2", "U3.42")
net("LED_PWR", "R29.2", "D5.2"); net("LED_RUN_A", "R30.2", "D6.2"); net("LED_RUN", "D6.1", "U3.2"); net("LED_FLT", "U3.46", "R31.1"); net("LED_FLT_A", "R31.2", "D7.2")
net("GND", "J1.2", "D1.2", "C1.2", "C2.2", "C3.2", "U1.1", "C7.2", "R2.2", "R4.2", "C5.2", "C6.2", "U2.1", "C8.2", "C9.2",
    "U3.23", "U3.35", "U3.47", "U3.8", "C10.2", "C11.2", "C12.2", "C13.2", "C14.2", "C15.2", "C16.2", "SW1.2", "R6.2", "R32.2", "C17.2", "C18.2", "J10.5",
    "U4.6", "U4.22", "U4.29", "U4.12", "U4.14", "U4.10", "U4.24", "U4.17", "C19.2", "C20.2", "C21.2", "R7.2", "R8.2", "C24.2", "C25.2", "R12.2",
    "Q1.2", "R14.2", "Q2.2", "R16.2", "U5.4", "U5.5", "U5.3", "U5.8", "C26.2", "C27.2", "J5.4", "J6.4", "J7.4", "C30.2", "J8.2", "C31.2", "R25.2", "C32.2",
    "U6.5", "C33.2", "J11.4", "U7.1", "U7.2", "U7.3", "U7.4", "U7.7", "C34.2", "D5.1", "D7.1", "H1.1", "H2.1", "H3.1", "H4.1")
NETS = N
NC = {"U3": ["3", "4", "33", "38", "39", "40", "45"], "U4": ["13"]}   # deliberately unconnected: spare GPIO, driver NC pin
POWER_NETS = ["+24V_IN", "VFUSE", "+24V", "BUCK_SW", "+5V", "MOT_A1", "MOT_A2", "MOT_B1", "MOT_B2", "SENSE_A", "SENSE_B", "VALVE_N", "FAN_N"]
BOARD_W, BOARD_H = 100.0, 80.0
