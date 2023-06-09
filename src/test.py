import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

def binstr2signed_int(x):
    # Converte binary str x to integer, assuming that x is in 2's complement format.
    bw = len(x)
    if bw == 1:
        return -int(x, 2)
    return int(x[1:], 2) - int(x[0], 2) * 2**(bw - 1)

N_TAPS = 4
INPUT_REG = 0

@cocotb.test()
async def test_delay(dut):
    input =           [0] * (N_TAPS - 1 + 1) + [8, 4, 0, 0]
    output_expected = [0] * (N_TAPS + 2 + INPUT_REG) + [1]
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0
    dut._log.info("checking...")
    for clock_cycle, (x, y_expected) in enumerate(zip(input, output_expected)):
        dut.x_in.value = x
        await ClockCycles(dut.clk, 1)
        y_actual = binstr2signed_int(dut.y_out.value.binstr)
        assert y_actual == y_expected, f"{clock_cycle = }: {y_actual = }, {y_expected = }"


@cocotb.test()
async def test_identity_function(dut):
    input =           [0] * (N_TAPS - 1 + 1) + [16] + [x * 2 for x in range(-8, 8)] + [0, 0]
    output_expected = [0] * (N_TAPS + 2 + INPUT_REG) + [x for x in range(-8, 8)]
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0
    dut._log.info("checking...")
    for clock_cycle, (x, y_expected) in enumerate(zip(input, output_expected)):
        dut.x_in.value = x
        await ClockCycles(dut.clk, 1)
        y_actual = binstr2signed_int(dut.y_out.value.binstr)
        assert y_actual == y_expected, f"{clock_cycle = }: {y_actual = }, {y_expected = }"


@cocotb.test()
async def test_minus_function(dut):
    input =           [0] * (N_TAPS - 1 + 1) + [-31] + [x * 2 for x in range(-15, 16)] + [0, 0]
    output_expected = [0] * (N_TAPS + 2 + INPUT_REG) + [-(x * 2 * 31)//32 for x in range(-15, 16)]
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0
    dut._log.info("checking...")
    for clock_cycle, (x, y_expected) in enumerate(zip(input, output_expected)):
        dut.x_in.value = x
        await ClockCycles(dut.clk, 1)
        y_actual = binstr2signed_int(dut.y_out.value.binstr)
        assert y_actual == y_expected, f"{clock_cycle = }: {y_actual = }, {y_expected = }"


@cocotb.test()
async def test_maximum_value(dut):
    input =           [0] + [-31 for _ in range(2 * N_TAPS)] + 2 * [0]
    output_expected = [0] * (N_TAPS + 2 + INPUT_REG) + [i * 31 * 31 // 32 for i in range(1, N_TAPS + 1)]
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0
    dut._log.info("checking...")
    for clock_cycle, (x, y_expected) in enumerate(zip(input, output_expected)):
        dut.x_in.value = x
        await ClockCycles(dut.clk, 1)
        y_actual = binstr2signed_int(dut.y_out.value.binstr)
        assert y_actual == y_expected, f"{clock_cycle = }: {y_actual = }, {y_expected = }"


@cocotb.test()
async def test_minimum_value(dut):
    input =           [0] + [-32] * N_TAPS + [31] * N_TAPS
    output_expected = [0] * (N_TAPS + 2 + INPUT_REG) + [-32 * 31 * i // 32  for i in range(1, N_TAPS + 1)]
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0
    dut._log.info("checking...")
    for clock_cycle, (x, y_expected) in enumerate(zip(input, output_expected)):
        dut.x_in.value = x
        await ClockCycles(dut.clk, 1)
        y_actual = binstr2signed_int(dut.y_out.value.binstr)
        assert y_actual == y_expected, f"{clock_cycle = }: {y_actual = }, {y_expected = }"


@cocotb.test()
async def test_maximum_product_lsb(dut):
    input =           [1] + [0] * (N_TAPS - 1) + [-32, -31] + [0] * 20
    output_expected = [0] * (N_TAPS + 2 + INPUT_REG) + [31, 0] + [0] * 20
    output_bw = [1] * (N_TAPS + 2 + INPUT_REG) + [8, 5] + [0] * 20
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0
    dut._log.info("checking...")
    for clock_cycle, (x, y_expected, y_bw) in enumerate(zip(input, output_expected, output_bw)):
        dut.x_in.value = x
        await ClockCycles(dut.clk, 1)
        y_actual = binstr2signed_int(dut.y_out.value.binstr[-y_bw:])
        assert y_actual == y_expected, f"{clock_cycle = }: {y_actual = }, {y_expected = }"


@cocotb.test()
async def test_maximum_value_lsb(dut):
    input =           [1] + [31] * N_TAPS + [-32, 0] * 10 + [0] * 10
    output_expected = [0] * (N_TAPS + 2) + [a for b in [[-992 * i, 0] for i in range(4)] for a in b]
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0
    dut._log.info("checking...")
    y_msb_lsb = ["", ""]
    for clock_cycle, (x, y_expected) in enumerate(zip(input, output_expected)):
        dut.x_in.value = x
        y_msb_lsb[(clock_cycle + 1) % 2] = dut.y_out.value.binstr
        if (clock_cycle % 2) == 0:
           y_actual = binstr2signed_int(y_msb_lsb[0] + y_msb_lsb[1][-5:])
           print(f"{y_actual = }, {y_expected = }")
           assert y_actual == y_expected, f"{clock_cycle = }: {y_actual = }, {y_expected = }"
        await ClockCycles(dut.clk, 1)
