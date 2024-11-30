
# Output settings
set terminal pdfcairo size 10in,8in
set output 'RT_queue_components.pdf'

# Plot styling
set style data lines
set grid

# Multiple plot layout
set multiplot layout 3,1 title "Queue Analysis and Response Time Components"

# Plot 1: Response Time Components
set title "Response Time Components"
set xlabel "Time (s)"
set ylabel "Response Time (ms)"
set key right top
plot 'client_req.csv' using (($1-1731874533.545)/1000):4 title 'Total RT',      'queue_length.csv' using ($1-1731874533.545):2 title 'Queue Time'

# Plot 2: Queue Length
set title "Queue Length Over Time"
set xlabel "Time (s)"
set ylabel "Queue Length"
set key right top
plot 'queue_length.csv' using ($1-1731874533.545):3 title 'Total Queue Length',      'queue_length_client.csv' using ($1-1731874533.545):2 title 'Client Queue',      'queue_length_server.csv' using ($1-1731874533.545):2 title 'Server Queue'

# Plot 3: Bottleneck Periods
set title "Bottleneck Detection"
set xlabel "Time (s)"
set ylabel "Is Bottleneck"
set key right top
plot 'queue_length.csv' using ($1-1731874533.545):4 title 'Bottleneck Periods' with steps

unset multiplot
