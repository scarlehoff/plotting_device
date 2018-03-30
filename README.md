# Plotting device

A library for (beautiful?)-(gnuplotlike?) plots using matplotlib, so I can use jupyter notebooks with it

------

The plan was to have something I can use in a quick&dirty way together with jupyter notebooks to show plots during presentations or lectures.
For that I needed some plotting styles that were only available (as far as I know) in gnuplot, namely boxxyerrorbars so I have added them to matplotlib in the most general way I could think of.

Also, taking ratios of two plots in gnuplot is a pain so I added a plot_1/plot_2 division method to the Plot class.

I imagine this code will evolve over time as I need to add new features. It is geared towards its applications in High Energy Physics because that's what I do (you can see the example plot looks fairly similar to the ones in https://arxiv.org/abs/1802.02445) but it should be completely general.

Please, ask me any questions you have.

Happy plotting!
