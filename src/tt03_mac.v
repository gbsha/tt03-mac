`default_nettype none

// copy parameters to tb.v, test.py
// as files may be used individually
module gbsha_tt03_mac_top #(parameter N_TAPS = 4,
                             BW_in = 6,
                             BW_product = 11,
                             BW_sum = 13,
                             BW_out = 8
                             )
(
  input [7:0] io_in,
  output [7:0] io_out
);
    // control signals
    wire clk = io_in[0];
    wire reset = io_in[1];
    reg [2:0] coefficient_loaded;
    reg provide_lsb;
    reg read;

    // inputs and output
    wire signed [BW_in - 1:0] x_in = io_in[BW_in - 1 + 2:2];
    wire [BW_out - 1:0] y_out;
    assign io_out[BW_out - 1:0] = y_out;
    if (BW_out < 8)
        assign io_out[7:BW_out] = 0;

    // storage for input, multiplier
    reg signed [BW_in - 1:0] coefficient [N_TAPS -1:0];
    reg signed [BW_in - 1:0] x [N_TAPS - 2:0];

    // intermediate values
    wire signed [BW_product - 1:0] product [N_TAPS -1: 0];
    // output register
    reg signed [BW_sum - 1:0] sum;

    always @(posedge clk) begin
        // initialize shift register with zeros
        if (reset) begin // Reset registers
            x[0] <= 0;
            x[1] <= 0;
            x[2] <= 0;
            coefficient[0] <= 0;
            coefficient[1] <= 0;
            coefficient[2] <= 0;
            coefficient[3] <= 0;
            sum <= 0;
            coefficient_loaded <= 0;
            provide_lsb <= 0;
            read <= 1;
        end else if (coefficient_loaded == 0) begin // Read LSB option
            provide_lsb <= x_in;
            coefficient_loaded <= 1;
        end else if (coefficient_loaded < N_TAPS + 1) begin // Load weights
            coefficient[3] <= coefficient[2];
            coefficient[2] <= coefficient[1];
            coefficient[1] <= coefficient[0];
            coefficient[0] <= x_in;
            coefficient_loaded <= coefficient_loaded + 1;
        end else if (read) begin // Load inputs
            sum <= product[0] + product[1] + product[2] + product[3];
            x[2] <= x[1];
            x[1] <= x[0];
            x[0] <= x_in;
            read <= read + provide_lsb;
        end else begin // Provide LSB
            sum[2 * (BW_sum - BW_out) - 1:BW_sum - BW_out] <= sum[BW_sum - BW_out -1:0];
            read <= read + provide_lsb;
        end
    end

    assign product[0] = x_in * coefficient[0];
    assign product[1] = x[0] * coefficient[1];
    assign product[2] = x[1] * coefficient[2];
    assign product[3] = x[2] * coefficient[3];

    // shift by 5 bits. Corresponds to division by 32
    assign y_out = sum[BW_sum - 1:BW_sum - BW_out];
endmodule
