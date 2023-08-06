#!/usr/bin/env python

'''
A script for testing various plotting function object
Simon Mudd
24/07/2020
'''

import lsdviztools.lsdbasemaptools as bmt
from lsdviztools.lsdplottingtools import lsdmap_gdalio as gio
import lsdviztools.lsdplottingtools as lsdplt
import rasterio as rio
import numpy as np
import lsdviztools.lsdmapwrappers as lsdmw

def test_01():
    this_DEM = bmt.ot_scraper()

    this_DEM.print_parameters()
    this_DEM.download_pythonic()

    this_DEM.to_UTM_pythonic()


def test_02():

    fname_prefix = "shillong_SRTM30_UTM"
    DataDirectory = "./"
    ChannelFileName = "shillong_SRTM30_UTM_chi_data_map.csv"

    img_name0 = lsdmw.SimpleHillshade(DataDirectory,fname_prefix, cmap = "terrain", cbar_loc = "right", size_format = "ESURF", fig_format = "png", dpi = 250, out_fname_prefix = "",save_fig = False)

    #img_name = lsdmw.PrintChannels(DataDirectory,fname_prefix, ChannelFileName, cmap = "jet", size_format = "ESURF", fig_format = "png", dpi = 250, out_fname_prefix = "", plotting_column = "basin_key")

    #img_name2 = lsdmw.PrintChannelsAndBasins(DataDirectory,fname_prefix, add_basin_labels = True, cmap = "jet", size_format = "ESURF", fig_format = "png", dpi = 250, out_fname_prefix = "")

    #img_name3 = lsdmw.PrintBasins(DataDirectory,fname_prefix, add_basin_labels = True, cmap = "jet", cbar_loc = "right", size_format = "ESURF", fig_format = "png", dpi = 250, out_fname_prefix = "")

    #img_name4 = lsdmw.PrintBasins_Complex(DataDirectory,fname_prefix,use_keys_not_junctions = True, show_colourbar = False,Remove_Basins = [], Rename_Basins = {0:"yo",1:"bo"}, Value_dict= {},cmap = "jet", colorbarlabel = "colourbar", size_format = "geomorphology",fig_format = "png", dpi = 250, out_fname_prefix = "", include_channels = True, label_basins = True, save_fig = False)

    #print(img_name4)

    #img_name5 = lsdmw.PrintChiChannels(DataDirectory,fname_prefix, ChannelFileName, add_basin_labels = True, cmap = "jet", cbar_loc = "right", size_format = "geomorphology", fig_format = "png", dpi = 250,plotting_column = "source_key",discrete_colours = False, NColours = 10, out_fname_prefix = "")

    #img_name6 = lsdmw.PrintChiChannelsAndBasins(DataDirectory,fname_prefix, ChannelFileName, add_basin_labels = True, cmap = "jet", cbar_loc = "right", size_format = "ESURF", fig_format = "png", dpi = 250,plotting_column = "source_key",discrete_colours = False, NColours = 10, colour_log = True, colorbarlabel = "Colourbar", Basin_remove_list = [], Basin_rename_dict = {} , value_dict = {}, out_fname_prefix = "", show_basins = True, min_channel_point_size = 0.5, max_channel_point_size = 2)

    #img_name7 = lsdmw.PrintChiCoordChannelsAndBasins(DataDirectory,fname_prefix, ChannelFileName, add_basin_labels = True, cmap = "cubehelix", cbar_loc = "right", size_format = "ESURF", fig_format = "png", dpi = 250,plotting_column = "source_key",discrete_colours = False, NColours = 10, colour_log = True, colorbarlabel = "Colourbar", Basin_remove_list = [], Basin_rename_dict = {} , value_dict = {}, plot_chi_raster = False, out_fname_prefix = "", show_basins = True, min_channel_point_size = 0.5, max_channel_point_size = 2)

    #img_name8 = lsdmw.PrintChiStacked(DataDirectory,fname_prefix, ChannelFileName, cmap = "jet", cbar_loc = "bottom", size_format = "ESURF", fig_format = "png", dpi = 250,plotting_column = "source_key",discrete_colours = False, NColours = 10,colorbarlabel = "Colourbar", axis_data_name = "chi", plot_data_name = "m_chi", plotting_data_format = 'log', Basin_select_list = [], Basin_rename_dict = {}, out_fname_prefix = "", first_basin = 0, last_basin = 0, figure_aspect_ratio = 2, X_offset = 5, rotate_labels=False)


def test_03():

    fname_prefix = "shillong_SRTM30_UTM"
    Drape_prefix = "shillong_SRTM30_UTM"
    DataDirectory = "./"
    img_name = lsdmw.PrintCategorised(DataDirectory,fname_prefix, Drape_prefix,
                     show_colourbar = False,
                     cmap = "jet", cbar_loc = "right", cbar_label = "drape colourbar", size_format = "geomorphology",
                     fig_format = "png", dpi = 250, out_fname_prefix = "")


if __name__ == "__main__":
    test_02()
    #test_03()
    #run_tests_2()
