This page provide  examples of input files with increasing flexibility.
It also provides some information on the 'format' of the files, which is supplemented by the information in the files
themselves.
To make 'ember' diagrams from your own data, start from the Basic format below, which contains a standard IPCC-style data table
(but note that no files are 'from the IPCC' or under its responsibility: see [more information](/more)).

# Basic format

We expect the Basic format to fill most needs. It is simple and may receive more development efforts to accommodate
future needs. This format is based on tables provided in the supplementary material of IPCC Special reports published
in 2019. The files indicates the level of global warming which corresponds to "risk transitions", i.e. changes
from one risk level to the next, according to a standard scale of risk used by the IPCC in several of its reports.

## SRCCL figure SPM.2 B

[SRCCL example](/examples/Basic-fmt-SRCCL.xlsx)

This example contains the data from table SM7.6 of the Special Report on Climate change and Land. 
The resulting 'burning ember diagram' appears in the Summary for Policymakers as 
[figure 2, panel B (IPCC website)](https://www.ipcc.ch/site/assets/uploads/2019/08/SPM2-approval-FINAL-1.pdf).

## Template for new embers

[Standard template](/examples/Basic-template.xlsx)

This spreadsheet does not contain real data, but rather generic names intended to help identifying how it can be 
modified. It also contains lines to indicate the hazard level corresponding to the 'midpoints' (or median) within
each transition. Those midpoints are optional (the lines can be left blank or deleted, as in the SRCCL example above)

## Parameters in the "data" spreadsheet

A few parameters, mainly related to the data itself, can be set in the same spreadsheet as the data:

- `haz_top_value = 3` => the vertical scale is limited to +3°C (the `=` sign is used here for clarity, in the sheet
   the name of the parameter and its value are simply in adjacent cells)

- `haz_name` and `haz_unit` => the vertical scale ('hazard level') may relate to 
indicators of change other than mean temperature, for example the rate of change or ocean pH.

- `leg_title` specifies a title to be written on top of the legend (colour bar); it is copied here from SRCCL SPM.2; it this title is not appropriate for your graphic,
just delete or replace it.

While it is not used in this example, you may move the legend to the right instead of the bottom, by adding

- `leg_pos = right`

None of these parameters is mandatory: there are default values.

# Basic format + layout parameters sheet

The "Basic format" (above) is limited to a few parameters which are sufficient to reproduce most types
or 'burning ember' figures published so far, but with limitations regarding layout details.
To avoid cluttering the sheet that contains the assessment data, we add a sheet containing layout parameters.

[SRCCL example + layout](/examples/Basic-layout-SRCCL.xlsx)

The "Basic+layout" example includes the additional 'layout' sheet with all its parameters.
This particular example illustrates the following:

- **caption position** (in this example `leg_pos = right`). This is one of the few parameters which can be either in the main
data sheet (as mentioned above) or in the layout data sheet (here); when the layout sheet is present, we advise 
in favour of including theses parameters in the layout sheet.<br> 
There are 5 permitted values for `leg_pos`: *under*, *right*, *in-grid-horizontal*, *in-grid-vertical* 
(for complex figures in which there are at least two lines of "ember" groups), 
ane *none* (which results in the absence of legend); <br>
*in-grid-*... is specific to more complex figures in which there are at least two lines of "ember" groups, which form a "grid".

- **horizontal grid lines** (in this example 0, 1, 2, 3 °C). The selection of these levels may (simultaneously) use two
definitions, provided in the parameter `haz_grid_lines`. Its first value (here: 3) is a target number of levels which
the software may adapt slightly in order to provide 'nice' levels (here : the 4 values 0, 1, 2, 3). The next columns on
the right additionally provide absolute values of levels that have to be plotted (here: a line is added at 1.5°C)
which is set to 3 (and adapted by the software to have 4 'nice' levels). There can be more than one of these
'prescribed' levels.

- **confidence levels presentation**. These can be show in different ways: a number of dots was used in the most recent 
IPCC practice (see SROCC SPM.3), while letters (L for Low confidence, H for Medium, ...) where used in the SRCCL.  
The names of confidence levels (Low, Medium...) used in the data sheet are translated to symbols for the diagram 
according to a table which is at the bottom of the 'layout' sheet. You could fill anything as input (`conf_levels_file`)
and anything as output (`conf_levels_graph`), so even translations could potentially be done in this way.

The resulting figure is significantly closer to the layout of the published figure 
([figure 2, panel B (IPCC website)](https://www.ipcc.ch/site/assets/uploads/2019/08/SPM2-approval-FINAL-1.pdf));
this shows the flexibility generated by using the 'layout' sheet.

There are other options illustrated in this Excel file, such as the possibility to 
<a name="sort">**sort the embers**</a>.
It is thus possible to generate different diagrams without changing the 'data' sheet (i.e. instead
of manually moving data lines to re-order embers, which could possibly result in errors, you may list the ember names 
in the desired order in the 'layout' sheet). It also possible to sort *groups* of embers;
groups are tables in the data sheet, separated by blank lines.
The position of many elements can be adjusted by changing parameters according to their
names from the diagram included in the Excel file.

# Fullflex format

[Fullflex format example](/examples/Flex-fmt-RFC.xlsx)

The "full flexibility" format provides more flexibilty regarding the input data.
The first sheet from this Excel workbook is completely different from the first sheet of the 'basic format' above.
It provides more control on the risk levels, e.g. a transition 
that has a faster increase in risk at some temperature level. 
The second sheet is the 'layout' sheet described above, 
and the last sheet defines the colors and associated risk levels.
The data provided here is only an example for the format, and should not be used.

## <a name="Z2020">Zommers et al. 2020</a>

The data used in figure 3 of an upcoming publication by Zommers et al. [1] will be added here when the paper is published.
The approach for obtaining this data is decribed in [Marbaix (2020)](https://doi.org/10.5281/zenodo.3992856).

The main file, corresponidng to figure 3 of the paper, is RFCs-data-2020_01_26-Z2020_rev1.xlsx. Additionally, 
RFCs-data-2020_01_26-Z2020_rev1_byPubli.xlsx shows the embers sorted by publication (instead of by Reason for concern).
Both files contain the same data, while the different sorting is triggered by parameters in the 'layout' spreadsheet, 
as explained above ([sort the embers](#sort)).

[1] Zommers, Z., Marbaix P, Fischlin A., Ibrahim Z. Z., Grant Z, Magnan A. K., Pörtner H-O, Howden M., Calvin K., Warner K., 
Thiery W., Sebesvari Z., Davin E. L., Evans J.P., Rosenzweig, C., O’Neill B. C., Anand Patwardhan, Warren R., 
van Aalst M. K. and Hulbert M. (2020).
*Burning Embers: Towards more transparent and robust climate change risk assessments*. 
Accepted for publication in Nature Reviews Earth & Environment.

# Further improvements & documentation

Comments are welcome. We will make our best to respond to requests regarding improvement,
documentation, or specific features, adapting the application if needed.
(see contact below).