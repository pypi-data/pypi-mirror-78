# -*- coding: utf-8 -*-
"""
makember procuces a full burning ember plot from colour levels read from a table (.xlsx).

The objectives are to
- facilitate reproducibility of the figures,
- facilitate the production of new figures in a way that is both quick and reliable.
This code is written in http://en.wikipedia.org/wiki/Python_(programming_language)
using the open-source library ReportLab from http://www.reportlab.com

Copyright (C) 2020  philippe.marbaix@uclouvain.be
"""
import numpy as np
import os
from reportlab.lib.units import mm, cm
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT
from embermaker import helpers as hlp
from embermaker import ember as emb
from embermaker.__init__ import __version__


# For an upcoming release (none of this appears urgent):
# Todo: Test the support for reading confidence levels in the "extended" format
#      (implemented but not fully tested with 'extended' format data sheets, but well tested with the basic format)

# Input file
# ----------
# This code can process 3 file formats:
# - The basic file format only contains data about the risk and confidence levels,
#   in the format from the IPCC SRCCL chap 7 supplementary material; the workbook only contains one sheet.
# - The extended file format contains the same first sheet, but 2 additional sheets provide:
#   . graphic parameters
#   . color definitions
# - The full-flex format uses a different sheet to provide the data about the risk levels;
#   this sheet provides the possibility to define more risk levels: it may define the start, middle point and end
#   of a colour transition, or contain more colours. It can contain data with a reference other than the pre-ind level.
#   This format provides support for hazard indicators other then global-mean temperature.
#   The two following sheets should be identical to the "extended" file format above.

def makember(infile=None, outfile=None, prefcsys='CMYK'):
    """
    Reads ember data from .xlsx files, reads default values if needed, and generates an ember plot;
    in principle, this part of the plotting relates to the most 'high level' aspects that decides for the design,
    while lower level aspects are delegated to the ember module.
    :param infile: The name of the data file (.xlsx). Mandatory.
    :param outfile: An optional name for the output file; default = path and name of infile, extension replaced to .pdf
    :param prefcsys: The prefered color system (also called mode): RGB or CMYK.
    :return: a list of two strings: [output file path, error message if any]
    """

    # Input file:
    if infile is None:
        return [None, hlp.addlogfail("No input file.")]

    # File containing default values; used if user-provided file does not include parameters:
    # (assumed to be a subdirectory within the embermaker package, with apologizes if this is unsafe or not elegant)
    infdef = os.path.join(os.path.dirname(__file__), "defaults/BE-defaults.xlsx")

    # Open input file (workbook):
    wbmain = hlp.secure_open_workbook(infile)

    # The file containing default values for parameters or colors will only be open if needed:
    def getwbdef():
        return hlp.secure_open_workbook(infdef)

    if "Graph parameters" not in wbmain.sheet_names():
        hlp.addlogmes("Graph parameters: will use default values.")
        wbpar = getwbdef()
    else:
        wbpar = wbmain

    if "Color definitions" not in wbmain.sheet_names():
        hlp.addlogmes("Colours: will use default palettes.")
        wbcol = getwbdef()
    else:
        wbcol = wbmain

    # Get the color palette
    # ---------------------
    # The palette will be defined by:
    # - its color system (RGB, CMYK...): csys
    # - names of risk levels associated to colors : cnames (see excel sheet)
    # - a risk level index: cdefs[0] (1D numpy array of risk indexes)
    # - the color densities for each color corresponding to a risk index :
    #       cdefs[i] (1D numpy array of color densities for each risk index, given i=#color within the color system)
    read = False
    cnames, ctmp = [], []
    csys = ''  # csys will be the colour system, read from file
    cref = 1.0  # Reference (max) value of the color range (optional parameter)
    sht = wbcol.sheet_by_name("Color definitions")
    rows = sht.get_rows()
    # Default palette (if no palette defined in the color sheet)
    if prefcsys == 'RGB':
        cpal = 'RGB-SRCCL-C7'
    else:
        cpal = 'CMYK-IPCC'

    for row in rows:
        key = str(row[0].value).strip()
        name = str(row[1].value).strip()
        inda = [acell.value for acell in row[2:]]  # input data
        if key == 'ACTIVE-P':
            cpal = name
            hlp.addlogmes('Will use color palette: ' + cpal)
        elif key == 'PALETTE' and cpal == name:
            read = True
        elif key == '':
            read = False
        elif key == 'HEADERS' and read:
            if inda[1:4] == ['Red', 'Green', 'Blue']:
                csys = 'RGB'
            elif inda[1:5] == ['Cyan', 'Magenta', 'Yellow', 'Black']:
                csys = 'CMYK'
            else:
                raise Exception("Unknown color system (see colors in sheet 'Color definitions').")
        elif key == 'DATA' and read:
            cnames.append(name)
            ctmp.append(inda[:1 + len(csys)])
        elif key == 'REFERENCE' and read:
            # The "reference" is an arbitrary number that is the maximum of colour values, typically 1, 100, or 255.
            # (default value is 1, see above)
            try:
                cref = float(inda[0])
            except ValueError:
                return [None, hlp.addlogfail(
                    "REFERENCE value for the colors is wrong or misplaced (must be 3rd col in 'Color definitions').")]
    cdiv = [1.0] + ([cref] * (len(ctmp[0]) - 1))  # We need to divide each line by the ref, but not element 0
    cdefs = (np.array(ctmp) / cdiv).transpose()  # color definitions array
    del ctmp
    hlp.addlogmes("Read colour palette: " + csys)
    hlp.addlogmes("Palette risk levels and colors: " + str(cdefs))

    # Get graph parameters
    # --------------------
    gp = {}
    sht = wbpar.sheet_by_name("Graph parameters")
    rows = sht.get_rows()
    for row in rows:
        key = row[0].value.strip()
        if key != '':
            # Find the position of the last non-empty cell + 1, or 1 if there is none:
            # (next just gets the first value of the iterator, which is what we want; the list is scanned from its end)
            rowlen = next(i for i in range(len(row), 0, -1) if row[i - 1].value or i == 1)
            if rowlen <= 2:  # 2 values = key + one value (possibly empty)
                gp.update({row[0].value: row[1].value})  # Case key, value : store the value (not 1-element list)
            else:  # More than 2 values = the user provided a list of values
                gp.update({row[0].value: [c.value for c in row[1:rowlen]]})  # Case key, list : store the list
    hlp.addlogmes("Read graphic parameters: " + str(gp))

    # Get the ember data from the file
    # --------------------------------
    sht = wbmain.sheet_by_index(0)
    # Check file format; By default, the format is "Basic" = SRCCL-like (look for the File format in the first 6 rows)
    ffind = [sht.cell_value(i, 1) for i in range(max(6, sht.nrows)) if sht.cell_value(i, 0) == "File format"]
    if len(ffind) == 1:
        ffmt = ffind[0].strip()
    else:
        ffmt = "Basic"
    hlp.addlogmes("Format of the main input file: " + str(ffmt))
    rows = sht.get_rows()

    # BE data storage
    lbes = []  # list of ember instances (to be filled by reading the data part of the Excel sheet, below)

    be = None  # The ember currently being processed
    be_risk = None
    be_group = ''

    # Fullflex file format = from Zommers et al 2020
    # - - - - - - - - - - - - - - - - - - - - - - - -
    ndata = 0  # Will be set to the number of risk levels in the file
    if ffmt == "Fullflex":
        dstate = 'paused'  # Cannot read data until 1) allowed to by the 'Start' keyword and 2) the risk levels are set
        for row in rows:
            key = row[0].value.strip()
            name = row[1].value.strip()
            inda = [acell.value for acell in row[2:]]  # input data
            if key == 'RISK-INDEX':
                # Get the risk levels for which the file will provide data ('hazard' levels related to the risk levels)
                be_risk = inda
                try:
                    ndata = be_risk.index('ref_to_preind')  # number of risk T(risk) levels for which there is data
                    # There are two additional values in header : ref-to-pre-ind and top_value (see .xlsx file)
                    dstate = 'ready'
                except ValueError:
                    raise Exception("Could not find column 'ref_to_preind' in the header line.")
                del be_risk[ndata:]
                for rlev in be_risk:
                    if isinstance(rlev, str):
                        raise Exception("There seems to be a missing value in the RISK-INDEX. This is not allowed")
                hlp.addlogmes('Read risk-index values:' + str(be_risk))
            elif key == 'START':
                dstate = 'waiting header'
                hlp.addlogmes('Waiting for risk levels / header')
            elif key == 'STOP':
                dstate = 'paused'
                hlp.addlogmes('Paused')
            elif key == 'GROUP' and dstate != 'paused':
                be_group = row[1].value
                hlp.addlogmes('Reading ember group: ' + str(be_group), mestype='title')
            elif key == 'HAZARD-INDICATOR' and dstate == 'waiting header':
                raise Exception("DATA was found before any risk levels / header line - cannot handle this.")
            elif key == 'HAZARD-INDICATOR' and dstate == 'ready':
                hlp.addlogmes('Reading data for: ' + str(name), mestype='subtitle')
                # Create an ember and add it to the list of embers:
                be = emb.Ember()
                lbes.append(be)
                be.name = str(name)
                be.group = be_group
                rhaz = float(inda[ndata])  # Reference hazard level (e.g. temperature) / pre-ind
                be.toph = float(inda[ndata + 1]) + rhaz  # Upper end of BE validity (do not show colours beyond that)
                be_hazl = []  # temporary storage for hazard-level data within a single ember
                be_risl = []  # temporary storage for risk-level data within a single ember
                if ndata != len(be_risk):
                    return [None, hlp.addlogfail(
                        "# risk levels does not match # hazard levels:" + str((len(be_risk), len(be_hazl))))]

                for i, x in enumerate(inda[0:ndata]):
                    if not (isinstance(x, str)):
                        be_hazl.append(x + rhaz)
                        be_risl.append(be_risk[i])  # so we skip risk levels with missing data for hazard level
                be.hazl = np.array(be_hazl)
                be.risk = np.array(be_risl)
            elif key == 'CONFIDENCE' and dstate == 'ready':
                be.conf = inda[0:ndata]
            elif key == 'HAZARD-INDICATOR-DEF':
                gp.update(
                    {'haz_' + name: inda[0]})  # Those parameters are on the first sheet because they relate to data

    # Basic file format = from IPCC SRCCL sup. mat.
    # - - - - - - - - - - - - - - - - - - - - - - -
    elif ffmt == "Basic":
        # The Basic format provide 'hazard' data for 3 transitions defined below.
        # The correspondance to our risk-index values is :
        # Undetectable to moderate = 0 -> 1, Moderate to high 1 -> 2, High to very high 2 -> 3.
        # *.5 = Median risk levels.
        # Hence the risk levels are:
        be_risk_levs = [[0.0, 0.5, 1.0],  # First transition (undetectable to moderate)
                        [1.0, 1.5, 2.0],  # Second transition
                        [2.0, 2.5, 3.0]]
        be_trans_names = ['undetectable to moderate', 'moderate to high', 'high to very high']
        be_trans_names_syn = {'white to yellow': 'undetectable to moderate',
                              'yellow to red': 'moderate to high',
                              'red to purple': 'high to very high'}
        be_trans_phases = ['min', 'median', 'max']
        be_trans_phases_syn = {'begin': 'min',
                               'end': 'max'}

        # Default values for some of the main parameters in the basic format
        gp.update({'haz_name': u'Global mean temperature change'})
        gp.update({'haz_unit': u'°C'})
        gp.update({'software_version_min': u'1.2.0'})  # Assumed minimum version if the file does not indicate it

        # List of parameters that can be used on the first sheet (= together with the data):
        bfparams = ['project_name', 'project_source', 'project_version',
                    'haz_name', 'haz_unit', 'haz_bottom_value', 'haz_top_value', 'haz_top_valid',
                    'haz_map_factor', 'haz_map_shift',
                    'leg_title', 'leg_pos', 'software_version_min']

        dstate = 'read-parameters'  # File reading status
        trans_name = ''
        be_group = u''  # Default ember group name
        for irow, row in enumerate(rows):
            cola = row[0].value.strip()  # Column A: may optionally contain the name of a group of embers
            colb = hlp.stripped(row[1].value)  # Column B: contains ember name, in the first line of a new ember.

            # if already reading and column D is blank or an ember name is found, an ember ended: prepare for next ember
            if dstate == 'reading' and (hlp.isempty(row[3].value) or not hlp.isempty(colb)):
                dstate = 'wait-ember'

            if cola == 'START':
                dstate = 'wait-ember'
                hlp.addlogmes('Waiting for risk levels / header')
                # Check file compatibility (we should have it now because the main parameters were read)
                fver = str(gp['software_version_min'])
                if fver > __version__:
                    hlp.addlogwarn("The input file requires a version ({}) newer than this app ({})"
                                   .format(fver, __version__), critical=True)
            elif cola == 'STOP':
                dstate = 'paused'
                hlp.addlogmes('Paused')
            elif cola in bfparams:
                # Read parameter
                gp.update({cola: colb})
            elif not hlp.isempty(cola) and hlp.isempty(colb) and dstate == 'wait-ember':
                # Read group name (data in first column, second column empty)
                be_group = cola
                hlp.addlogmes('Reading ember group: ' + str(be_group), mestype='title')
            elif colb == 'Name' or colb == 'Component':
                pass  # Ignore line(s) starting with "Name" or "Component", they are a table header.
            elif hlp.isempty(cola) and not hlp.isempty(colb) and dstate == 'wait-ember':  # Start new ember
                hlp.addlogmes('Reading data for: ' + str(colb), mestype='subtitle')
                # Create an ember and add it to the list of embers:
                be = emb.Ember()
                lbes.append(be)
                be.name = str(colb)
                be.group = be_group
                be.toph = float(gp['haz_top_value'])  # Upper end of BE validity (do not show colours beyond that)
                trans_name = ''  # A Transition name must be provided at first read, may fail if wrong file format
                dstate = 'reading'

            if dstate == 'reading':  # Try to read data if available, but always read transition name etc.
                trans_phase = hlp.normstr(row[3].value)
                if trans_phase in be_trans_phases_syn:  # Old name for the phase => 'translate' to new
                    trans_phase = be_trans_phases_syn[trans_phase]
                if trans_phase == be_trans_phases[0]:  # Start of a transition
                    trans_name = hlp.normstr(row[2].value)
                    if trans_name in be_trans_names_syn:  # Old name for the transition => 'translate' to new
                        trans_name = be_trans_names_syn[trans_name]
                    conf = row[5].value  # The confidence level, if any, is given at the start of the transition.
                    # (the validity of the confidence level name is checked below, when it is used)
                else:
                    conf = '<cont>'
                if trans_name not in be_trans_names or trans_phase not in be_trans_phases:
                    return [None, hlp.addlogfail('Input file format error: unknown transition in line {}'
                                                 .format(irow + 1))]
                itrans = be_trans_names.index(trans_name)
                iphase = be_trans_phases.index(trans_phase)

                hazl = row[4].value
                hlp.addlogmes('- ' + trans_name + "/" + trans_phase
                              + ' -> ' + str(hazl) + '; conf: ' + str(conf))
                if type(hazl) in [float, int]:  # existing (not missing) value
                    be.hazl.append(float(hazl))
                    be.risk.append(
                        be_risk_levs[itrans][iphase])  # we skip risk levels with missing data for hazard level
                    be.conf.append(conf)

        # Although most following operations work on array-like, at least one needs numpy arrays, so convert:
        for be in lbes:
            be.hazl = np.array(be.hazl)
            be.risk = np.array(be.risk)

    else:
        return [None, hlp.addlogfail("Unknown input file format:" + str(ffmt))]

    if len(lbes) == 0:
        return [None,
                hlp.addlogfail("No embers were found in the input file. Suspect a formatting error or incompatiblity. " 
                               "Please note that data is only read below a START mark in the first column;"
                               "if it is missing, nothing will be read.")]

    # Create the ouput file, drawing canevas, and ember-diagram object
    # ----------------------------------------------------------------
    if outfile is None:
        outfile = (os.path.splitext(infile)[0] + '.pdf').replace('/in/', '/out/')
    # Create output file and space for drawing:
    egr = emb.EmberGraph(outfile, csys, cnames, cdefs, gp)  # ember-diagram
    c = egr.c  # Drawing canvas

    # Optional mapping to a different hazard unit or hazard reference level
    # ---------------------------------------------------------------------
    if egr.isdefined('haz_map_factor'):
        hlp.addlogwarn("A scaling of the vertical (hazard) axis is requested in the input file (change in unit);"
                       " haz_map_factor= " + str(egr.getgp('haz_map_factor')))
        for be in lbes:
            be.hazl *= egr.getgp('haz_map_factor', vtype='float')

    if egr.isdefined('haz_map_shift'):
        hlp.addlogwarn("A change in the reference level for the vertical axis (hazard) was requested in the input file;"
                       " haz_map_shift= " + str(egr.getgp('haz_map_shift')))
        for be in lbes:
            be.hazl += egr.getgp('haz_map_shift', vtype='float')

    # Sort the embers, if requested (option)
    # --------------------------------------
    # There are two sorting levels. The sorting needs to be done on the second criteria first.
    # Second sorting level
    if egr.getgp('sort_2nd_by', vtype='lower') == 'name':
        emb.sortlist = egr.getgp('sort_2nd_by', data=True, vtype='lower')
        lbes = emb.selecsort(lbes,
                             emb.skeyname)  # Standard python sorting by f=skeyname + delete embers not in sortlist
        hlp.addlogmes("Secondary sorting by: name; values: " + str(emb.sortlist))
    if egr.getgp('sort_2nd_by', vtype='lower') == 'group':
        emb.sortlist = egr.getgp('sort_2nd_by', data=True, vtype='lower')
        lbes = emb.selecsort(lbes, emb.skeygroup)
        hlp.addlogmes("Secondary sorting by: group; values: " + str(emb.sortlist))

    # The first level may swap the role of ember group and name: this allows grouping by names (becoming 'groups')
    if egr.getgp('sort_first_by', vtype='lower') in ['name', 'group']:
        # Allow sorting according to an order set by a list in the Excel sheet:
        emb.sortlist = egr.getgp('sort_first_by', data=True, vtype='lower')
        hlp.addlogmes(
            "Primary sorting by: " + egr.getgp('sort_first_by', vtype='lower') + "; values: " + str(emb.sortlist))
        # Allow grouping by name instead of group, by swapping groups and names:
        if egr.getgp('sort_first_by', vtype='lower') == 'name':
            for be in lbes:
                be.name, be.group = be.group, be.name
        # Sort
        lbes = emb.selecsort(lbes, emb.skeygroup)

    # Generate group of embers (sublists) to prepare for drawing
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # index of embers which are not in the same group as the previous one
    ids = [i for i in range(1, len(lbes)) if lbes[i - 1].group != lbes[i].group]
    ids.insert(0, 0)  # add id=0 for first ember to build a list of index ranges defining groups
    ids.append(len(lbes))  # add  id+1 for the last ember (end of last range of embers)
    # List of groups of burning embers (nested list):
    glbes = [lbes[i:j] for i, j in zip(ids[0:len(ids) - 1], ids[1:])]

    # Draw the ember diagram
    # ----------------------
    # Note about notation:
    # x and y are coordinates on the canvas;
    # xbas, ybas define the bottom-left corner of a current plotting area.
    # be_ define lengths on the canvas read from the "gp" (graphic-) parameters found in a file.
    xbas = 1 * cm
    mxpos = xbas  # The role of mxpos is to track the maximum width of the canvas on which something was drawn.
    # The following values are used to calculate the upper most vertical position then draw towards the bottom
    gry = egr.getgp('be_bot_y') + egr.getgp('be_y') + egr.getgp('be_top_y')  # total height of the ember part
    if egr.getgp('leg_pos') == 'under':
        legy = egr.getgp('leg_bot_y') + egr.getgp('leg_y') + egr.getgp('leg_top_y')  # total height of the legend part
    else:
        legy = 0 * cm  # Legend is on the right: no need for vertical space
    # Embers are drawn in one or mutiple lines
    # The full figure does not have a fixed size: it is simply of the size needed to draw all the provided embers.
    # First define the number of graphic lines needed for the diagram:
    # (max_gr_line is the max number of embers per line, by default it is all the embers in one line)
    glines = np.ceil(len(glbes) / egr.getgp('max_gr_line', default=100))
    be_y = egr.getgp('be_y')
    be_x = egr.getgp('be_x')
    be_stp = be_x + egr.getgp('be_int_x')

    igrl = 0  # Number of groups in the current line
    il = 0  # Number of the current line

    # Draw the name of the vertical axis
    # - - - - - - - - - - - - - - - - - -
    # Todo (potentially, not urgent): possibly integrate in ember.vaxis ?

    ybas = ((glines - 1) * gry + legy + egr.getgp('be_bot_y') + egr.getgp('be_y') / 2.0)
    xnam = egr.getgp('haz_name_x', default=1 * cm)
    xbas = xnam * 0.7
    c.saveState()
    c.rotate(90)
    c.drawCentredString(ybas, -xbas, egr.getgp('haz_name', default='Hazard'))
    c.restoreState()

    # iterate over groups for drawing
    # - - - - - - - - - - - - - - - -
    for gbes in glbes:

        # Start a line of ember groups
        # - - - - - - - - - - - - - - -
        igrl += 1  # Move to next ember group in the current graphic line
        # If new graphic line, initialize relevant parameters:
        if igrl > egr.getgp('max_gr_line', default=100) or il == 0:
            xbas = xnam
            igrl = 1
            il += 1
            # Position of the bottom of the current BE draw area:
            ybas = (glines - il) * gry + legy + egr.getgp('be_bot_y')

        hlp.addlogmes('Drawing group: ' + str(gbes[0].group), mestype='title')

        # Y-coordinate (hazard levels) and axis
        # - - - - - - - - - - - - - - - - - - -
        # Pin the y coordinates to the drawing canvas for this group of embers (who will share the same y axis)
        # After this definition of the y-coordinates, egr will be used for any scaling to the canvas.
        # it is not possible to change the scaling (= how an hasard level is converted to canvas coordinate)
        # other than by calling 'pincoord'.
        # pincoord is called for each group of embers, never inside a group as it shares the same axis.
        egr.pincoord(ybas, be_y)

        # Draw the vertical axis and grid lines (using the y coordinates set by pincoord, but locating the axis at xpos)
        xgr = egr.getgp('scale_x') + len(gbes) * be_stp
        xpos = [xbas, xgr]
        egr.vaxis(xpos)

        # Update the position of the left of the current BE draw area (move to ember position, after axis):
        xbas += egr.getgp('scale_x') + egr.getgp('be_int_x') * 0.5

        # Group title
        egr.style.alignment = TA_LEFT
        egr.style.fontSize = gp['gr_fnt_size']
        egr.style.leading = egr.style.fontSize
        par = Paragraph(gbes[0].group, egr.style)
        xavlenght = len(gbes) * be_stp
        par.wrap(xavlenght, 60 * mm)
        par.drawOn(c, xbas, ybas + be_y + egr.getgp('be_top_y') * 0.33)

        bexs = []
        ahlevs = []
        # iterate over the embers in a group
        # - - - - - - - - - - - - - - - - - -
        for be in gbes:
            hlp.addlogmes('Drawing ember: ' + be.name, mestype='subtitle')
            xpos = [xbas, be_x]

            # Check user data consistency
            # - - - - - - - - - - - - - -
            if len(be.hazl) < 2:
                hlp.addlogwarn("No data or insufficient data for an ember: " + be.name, critical=True)
                continue  # There is nothing to do with this ember, but we continue to the next one (iterate)

            for ilev in np.arange(len(be.hazl) - 1):
                rdir = 1 if (be.risk[-1] >= be.risk[0]) else -1
                if ((be.hazl[ilev + 1] - be.hazl[ilev]) * rdir) < 0:
                    # While it might be that some risk decreases with hazard, this is unusual => issue warning
                    hlp.addlogwarn("Risk does not increase with hazard or a transition ends above the start of the next"
                                   " one [" + str(be.hazl[ilev]) + " then " + str(be.hazl[ilev + 1]) + "] for ember: "
                                   + be.name)
            for irisk in cdefs[0]:  # For all risk levels that are associated to a colour...
                # Catch any risk level that is below the highest one for this ember and not defined in this ember:
                if irisk <= be.risk[-1] and irisk not in be.risk:
                    hlp.addlogwarn(
                        "An intermediate risk level appears undefined; this will likely result in an abnormal "
                        "colour transition for ember: '" + be.name + "'", critical=True)

            # Draw ember:
            # - - - - - -
            bex = be.draw(egr, xpos)

            # Prepare data for the line showing the changes between embers :
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            if egr.getgp('show_changes') == 'True':
                rlevs = egr.getgp('show_changes', data=True)
                hlevs = np.interp(rlevs, be.risk, be.hazl)
                bexs.append(bex)
                ahlevs.append(
                    hlevs)  # [a]ll [h]azard-[lev]els = for all requested risk levels and all embers in the group

            # Add lines and marks indicating the confidence levels :
            # - - - - - - - - - - - - - - - - - - - - - - - - - - -
            # This section would benefit from being integrated in embers.py
            if egr.getgp('show_confidence') == 'True':
                # Set the font type and size for the symbols;
                # a scaling factor may be provided as attribute of conf_levels_graph
                fsize = egr.getgp('fnt_size') * egr.getgp('conf_levels_graph', vtype='float', default=2)
                fname = egr.getgp('conf_fnt_name', default=gp['fnt_name'])  # use specific font if defined
                c.setFont(fname, fsize)
                c.setLineWidth(0.2 * mm)
                # Get confidence level names and symbols:
                cffile = egr.getgp('conf_levels_file', data=True, vtype='lower')  # gets the data as lower case str
                cfgraph = egr.getgp('conf_levels_graph', data=True)

                # Get a list of ember data indexes corresponding to (potential) ends of confidence marks:
                # a confidence mark applies from the level where the confidence is stated and for as long as the
                # next levels indicate be.conf = '<cont>' (for the basic format, this range = a transition)
                nlevs = len(be.conf)
                conf_ends = [i for i in range(nlevs)
                             if be.conf[i] == '<cont>' and (i + 1 == nlevs or be.conf[i + 1] != '<cont>')]
                # Define the 'gap' between confidence lines which make sures that they are not contiguous:
                ygap = egr.get_y() * 0.005

                # Plot the confidence markings
                for ilev in range(int(len(be.hazl))):
                    if not (hlp.isempty(be.conf[ilev]) or be.conf[ilev] == '<cont>'):
                        xconf = xbas + be_x + 0.1 * egr.getgp('gr_int_x')
                        # Calculate limits of the color transitions along the hazard axis
                        # Lower limit:
                        yclo = ybas + egr.scale(be.hazl[ilev]) + ygap
                        # Higher limit: first find its index according to the above rule (end of the current mark)
                        try:
                            ihi = [i for i in conf_ends if i > ilev][0]
                        except IndexError:
                            hlp.addlogmes('End of a transition could not be found.')
                            continue
                        # The "min" below avoids extension of the shown line above the upper end of the graph (axis).
                        ychi = ybas + min(egr.scale(be.hazl[ihi]) - ygap, egr.get_y())
                        # hlp.addlogmes(str([be.hazl[ilev],be.hazl[ilev+1]]))
                        yconf = (yclo + ychi) / 2.0 - fsize / 3.0
                        lconf = str(be.conf[ilev]).lower()
                        try:
                            # Convert the confidence level name to the symbol from the graph parameters
                            conf = cfgraph[cffile.index(lconf)]
                        except ValueError:
                            hlp.addlogwarn(
                                'Confidence level from file could not be converted to graph symbol: ' + lconf)
                            conf = ""
                        c.drawString(xconf + gp['fnt_size'] / 3, yconf, conf)
                        c.line(xconf, yclo, xconf, ychi)
                c.setFont(gp['fnt_name'], gp['fnt_size'])

            # Move 'cursor' to the next ember
            xbas += be_stp

        # Draw the lines showing the changes between embers :
        # - - - - - - - - - - - - - - - - - - - - - - - - - -
        if egr.getgp('show_changes') == 'True':
            c.setStrokeColor(egr.colors['tgrey'])
            c.setDash([3, 3], 1)  # 3 unit on, 2 unit off; the last parameter defines a start point with dashes.
            ahlevs = np.transpose(ahlevs)
            for shlevs in ahlevs:  # for one curve = for a [s]ingle of the requested risk-levels
                beys = [egr.scale(shlev) for shlev in shlevs]  # scale to Canvas coordinates
                for ibe in range(len(beys) - 1):  # Draw, by line segment
                    c.line(bexs[ibe], ybas + beys[ibe], bexs[ibe + 1], ybas + beys[ibe + 1])
                hlp.addlogmes("Mean hazard / requested risk level: {:.3}".format(np.mean(shlevs)))
            c.setDash([], 0)  # Stop dashes = back to solid, unbroken line (this is from Adobe PDF reference !)

        # Add interval between groups
        # - - - - - - - - - - - - - -
        xbas += egr.getgp('gr_int_x')
        mxpos = max(mxpos, xbas)

    # Draw the legend
    # ----------------
    # The ember groups form a "grid". The legend can be
    # - centered at the right of the entire grid (leg_pos = right), and vertical
    # - centered under the entire grid (leg_pos = under), and horizontal
    # - inside the grid, as an additional ember group (leg_pos = in-grid-horizontal or in-grid-vertical)
    # The last case is only permitted as it makes sense, ie. there are several lines in the grid and the last
    # line is incomplete:
    if egr.getgp('leg_pos', vtype="lower") != "none":
        if ("in-grid" in egr.getgp('leg_pos')) and xbas < mxpos and glines > 1:
            emberbox = [xbas, legy, mxpos - xbas, gry]  # Box inside the grid : x0, y0, xsize, ysize
            isinside = True
        else:
            emberbox = [0, legy, mxpos, glines * gry]  # Box surrounding all embers : x0, y0, xsize, ysize
            isinside = False
        mxpos += egr.drawlegend(emberbox, isinside)
        # drawlegend returns any additional horizontal space used by the legend.

    # Add warning if a critical issue happened
    # ----------------------------------------
    # This will appear on top of the normal page, so first calculate the page height:
    mypos = gry * glines + legy
    # If there is more than one critical issue message, only one is 'stamped' on the graph for now.
    if hlp.getlog("critical"):
        egr.style.alignment = TA_LEFT
        egr.style.fontSize = 9
        egr.style.textColor = egr.colors['red']
        msg = "A critical issue happened: this diagram is not reliable. Please investigate. \n" \
              + hlp.getlog("critical")[0] + "(...)"
        par = Paragraph(msg, egr.style)
        par.wrap(7 * cm, 3 * cm)
        par.drawOn(c, 0.5 * cm, mypos + 0.2*cm)
        mypos += 2.5*cm  # Add space to the canvas for this warning

    if len(hlp.getlog("warning")) == 0 and len(hlp.getlog("critical")) == 0:
        c.setKeywords(["No warning messages: perfect"])
    else:
        c.setKeywords(["Warnings: "] + hlp.getlog("warning") + hlp.getlog("critical"))

    # Set page size and finalize
    # --------------------------
    # The min function below is a quick fix to enable case where only a few embers are drawn;
    # it should account for the real size of the colorbar
    c.setPageSize((mxpos, mypos))
    c.setCreator("MakeEmbers " + __version__)
    c.setTitle(str(os.path.splitext(os.path.basename(infile))[0]))
    c.setSubject("Embers with palette " + cpal)

    c.showPage()
    c.save()

    return [outfile, ""]
