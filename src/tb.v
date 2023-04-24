`default_nettype none
`timescale 1ns/1ps

/*
this testbench just instantiates the module and makes some convenient wires
that can be driven / tested by the cocotb test.py
*/

// copy parameters to tb.v, ttfir.v, test.py
// as files may be used individually
module tb #(parameter N_TAPS = 4,
                      BW_in = 6,
                      BW_out = 8
    )
    (
    input clk,
    input rst,
    input signed [BW_in - 1:0] x_in,
    output signed [BW_out - 1:0] y_out
   );

    // this part dumps the trace to a vcd file that can be viewed with GTKWave
    initial begin
        $dumpfile ("tb.vcd");
        $dumpvars (0, tb);
        #1;
    end

    // wire up the inputs and outputs
    wire [7:0] inputs;
    assign inputs[BW_in - 1 + 2:0] = {x_in, rst, clk};
    if (BW_in < 6)
        assign inputs[7:BW_in + 2] = 0;
    wire [7:0] outputs;
    assign y_out = outputs[BW_out - 1:0];

    // instantiate the DUT
    gbsha_tt03_mac_top gbsha_tt03_mac_top(
        `ifdef GL_TEST
            .vccd1( 1'b1),
            .vssd1( 1'b0),
        `endif
        .io_in  (inputs),
        .io_out (outputs)
        );

endmodule
