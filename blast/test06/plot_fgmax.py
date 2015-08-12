"""
Plot fgmax output from GeoClaw run.

"""

import matplotlib.pyplot as plt
import numpy
from clawpack.geoclaw import fgmax_tools, geoplot

def plot_fgmax_grid():

    fg = fgmax_tools.FGmaxGrid()
    fg.read_input_data('fgmax_grid1.txt')
    fg.read_output()

    #clines_zeta = [0.01] + list(numpy.linspace(0.05,0.3,6)) + [0.5,1.0,10.0]
    clines_zeta = [0.001] + list(numpy.linspace(0.05,0.25,10))
    colors = geoplot.discrete_cmap_1(clines_zeta)
    plt.figure(1)
    plt.clf()
    zeta = numpy.where(fg.B>0, fg.h, fg.h+fg.B)   # surface elevation in ocean
    plt.contourf(fg.X,fg.Y,zeta,clines_zeta,colors=colors)
    plt.colorbar()
    plt.contour(fg.X,fg.Y,fg.B,[0.],colors='k')  # coastline


    # draw better land
    import clawpack.geoclaw.topotools as tt
    topo = tt.Topography(path='../bathy/atlantic_2min.tt3')
    shore = topo.make_shoreline_xy()
    plt.plot(shore[:,0], shore[:,1], 'k', linewidth=10)

    # plot arrival time contours and label:
    arrival_t = fg.arrival_time/3600.  # arrival time in hours
    #clines_t = numpy.linspace(0,8,17)  # hours
    clines_t = numpy.linspace(0,2,5)  # hours
    #clines_t_label = clines_t[::2]  # which ones to label 
    clines_t_label = clines_t[::1]  # which ones to label 
    clines_t_colors = ([.5,.5,.5],)
    con_t = plt.contour(fg.X,fg.Y,arrival_t, clines_t,colors=clines_t_colors) 
    plt.clabel(con_t, clines_t_label)

    # fix axes:
    plt.ticklabel_format(format='plain',useOffset=False)
    plt.xticks(rotation=20)
    plt.gca().set_aspect(1./numpy.cos(fg.Y.mean()*numpy.pi/180.))
    plt.title("Maximum amplitude / arrival times (hrs)")


if __name__=="__main__":
    import os
    plot_fgmax_grid()
    plotdir = '_plots'
    if not os.path.isdir(plotdir): 
        os.mkdir(plotdir)
    fname = os.path.join(plotdir, "amplitude_times.png")
    plt.savefig(fname)
    print "Created ",fname