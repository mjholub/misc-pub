set datafile separator ","
set xdata time
set timefmt "%Y-%m-%d"
set format x "%Y-%m-%d"
set xlabel "Date"
set ylabel "Lines"
set title "Code additions/deletions over time"
plot "stats.csv" using 1:2 with lines title "Additions", "stats.csv" using 1:3 with lines title "Deletions"
