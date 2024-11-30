# Output settings
set terminal pdfcairo size 5in,5in
set output 'RT_distribution.pdf'

# Plot formatting
set size 0.8,1
set xrange [30:101]
set yrange [0:2000]

# Data settings
set datafile separator ","

# Labels and formatting
set ylabel "Response Time [ms]" font "Bold-Times_Roman,22"
set xlabel "X-ile [%]" font "Bold-Times_Roman,22"
set xtics 5

# Plot the data
plot 'RT_client_dist.csv' using 1:2 with linespoints \
     pt 1 lt 1 lw 1 lc rgb "red" \
     title "Client" axis x1y1