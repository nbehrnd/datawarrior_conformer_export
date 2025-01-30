#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# name:     datawarrior_conformer_export.py
# author:   nbehrnd@yahoo.com
# license:  GPL v2
# date:     [2023-01-25 Wed]
# edit:     <2023-05-31 Wed>

"""Access the 3D conformation from DW's 3D-Structure window.

Background:
The present version of DataWarrior displays conformations, alignments, etc in
an interactive 3D-structure window.  From there, a double click on the molecule
of interest allows to copy-paste the conformation into a new instance of DW /
an empty structure cell though apparently not always as a 3D structure.

The 'copy Molecule (3D)' of the window '3D structure' allows to copy-paste the
conformer information as a string into a text editor.  The information in this
string actually includes the 3D coordinates and additional data (e.g. how DW
can display the structure in the array) though the sequence of entries needs
some adjustment this script provides when writing a new 'container.dwar' (only)
for an export to 3D .sdf from DW.

Use:
The script was written for and is tested with Python 3.10.9 as provided e.g.,
by Linux Debian 12/bookworm (branch testing).  Only modules of the standard
Python library are used.  There are no additional dependencies.

For ethanol, the 3D molecule string from the 3D structure window is e.g.,

eMHAIh@ #qxnjsbG[f@@CV?bpATlYqSQ^brHTcidvtKPTLXdhCNwimWYdBEohCvWAKGohzuBAvythT@H`@h@@

Such a string may contain characters with a special meaning to the shell, and
can launch an unwanted action.  It consists of two data (sketcher structure and
encoded coordinates) separated by a space.  These are the reasons why it is
necessary to enclose the string by single quotes to explicitly indicate the
start and the end of the input.  For the above, run the following command (on
one line):

python3 ./datawarrior_conformer_export.py 'eMHAIh@ #qxnjsbG[f@@CV?bpATlYqSQ^brHTcidvtKPTLXdhCNwimWYdBEohCvWAKGohzuBAvythT@H`@h@@'

which will write file 'container.dwar'.  Read this new file with DataWarrior,
and export the structure as usually (File -> Save Special -> SD File) with the
option "Atom coordinates" on level "3D Structure"."""

import argparse
import sys
import time


def get_args():
    """collect the input, provide initial help"""

    parser = argparse.ArgumentParser(
        description="""Based on DW's Molecule 3D string, this script writes
file `container.dwar` to provide an eventual structure export as a (3D) .sdf
file. The script processes only one string at a time.  Note, earlier versions
of file `container.dwar` in the currently used working directory are going to
be overwritten.""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "input_string",
        help="""Copy-paste the DW string Molecule 3D from the window displaying
the 3D structure.  In the present implementation of this script, the string
must be enclosed in single quotes to explicitly indicate to the shell the start
and end of the string to process.  The script will not work if the input string
is enclosed in double quotes instead of single quotes.""",
    )

    return parser.parse_args()


def rearrange_string(input_string):
    """adjust the sequence of the entries the input provides"""
    input_structure = input_string.split()[0]
    input_3d = input_string.split()[1]

    # "placeholder" uses column FragFp irrelevant for the export to .sdf
    # "1" is the compound counter used in DataWarrior's spreadsheet
    report = "\t".join([input_3d, "placeholder", input_structure, "1"])
    return report


def write_new_dwar(structure_line=""):
    """provide 'container.dwar' for the export to .sdf

    The new file two write consists of three parts

    + a leading block, provided with an automatically adjusted time stamp
      Following DW's pattern, the insert is the UNIX epoch time in line of
      time of creating the .dwar file.
    + the by now rearranged line including DW's idcode about the conformer
    + a trailing block, which is invariant to local time and structure

    The two blocks are defined, followed by the concatenated output which
    is returned."""

    leading_block = str(
        f"""<datawarrior-fileinfo>
<version="3.3">
<created="{int( time.time() )}">
<rowcount="1">
</datawarrior-fileinfo>
<column properties>
<columnName="Structure">
<columnProperty="specialType	idcode">
<columnName="idcoordinates3D">
<columnProperty="parent	Structure">
<columnProperty="specialType	idcoordinates3D">
<columnName="FragFp">
<columnProperty="parent	Structure">
<columnProperty="specialType	FragFp">
<columnProperty="version	1.2.1">
</column properties>
idcoordinates3D	FragFp	Structure	Structure No"""
    )

    trailing_block = """<datawarrior properties>
<axisColumn_2D View_0="<unassigned>">
<axisColumn_2D View_1="<unassigned>">
<axisColumn_3D View_0="<unassigned>">
<axisColumn_3D View_1="<unassigned>">
<axisColumn_3D View_2="<unassigned>">
<chartType_2D View="scatter">
<chartType_3D View="scatter">
<columnFilter_Table="">
<columnWidth_Table_Structure="100">
<columnWidth_Table_Structure No="80">
<crosshairList_2D View="">
<detailView="height[Data]=0.33333;height[Structure]=0.33333;height[3D-Structure]=0.33333">
<faceColor3D_3D View="-1250054">
<fastRendering_2D View="false">
<fastRendering_3D View="false">
<filter0="#structure#	Structure">
<headerLines_Table="2">
<mainSplitting="0.70688">
<mainView="Structures">
<mainViewCount="4">
<mainViewDockInfo0="root">
<mainViewDockInfo1="Table	bottom	0.5">
<mainViewDockInfo2="Table	right	0.5">
<mainViewDockInfo3="2D View	right	0.5">
<mainViewName0="Table">
<mainViewName1="2D View">
<mainViewName2="Structures">
<mainViewName3="3D View">
<mainViewType0="tableView">
<mainViewType1="2Dview">
<mainViewType2="structureView">
<mainViewType3="3Dview">
<rightSplitting="0.64035">
<rotationMatrix_3D View00="1">
<rotationMatrix_3D View01="0">
<rotationMatrix_3D View02="0">
<rotationMatrix_3D View10="0">
<rotationMatrix_3D View11="1">
<rotationMatrix_3D View12="0">
<rotationMatrix_3D View20="0">
<rotationMatrix_3D View21="0">
<rotationMatrix_3D View22="1">
<rowHeight_Table="80">
<scaleStyle_2D View="frame">
<scaleStyle_3D View="arrows">
<scatterplotMargin_2D View="0.025">
<scatterplotMargin_3D View="0.025">
<showNaNValues_2D View="true">
<showNaNValues_3D View="true">
<structureGridColumn_Structures="Structure">
<structureGridColumns_Structures="6">
</datawarrior properties>"""

    export_string = ""
    export_string += leading_block
    export_string += "\n"
    export_string += structure_line
    export_string += "\n"
    export_string += trailing_block

    try:
        with open("container.dwar", mode="wt", encoding="UTF-8") as newfile:
            newfile.write(export_string)
    except IOError:
        print("It was impossible to write file 'container.dwar'.  Exit.")
        sys.exit()


def main():
    """joining functions"""
    args = get_args()

    insert = rearrange_string(args.input_string)
    write_new_dwar(structure_line=insert)


if __name__ == "__main__":
    main()
