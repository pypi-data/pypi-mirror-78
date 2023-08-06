#####################################################################
#Programm author: Carmelo Sammarco
#####################################################################

#< Tool4ASN - Software to compute cross correlations with different stacking methodologies. >
#Copyright (C) <2020>  <Carmelo Sammarco - sammarcocarmelo@gmail.com>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################################################################

import pkg_resources
import shutil
import os

forfolder1 =  pkg_resources.resource_filename('Tool4ASN', 'Script/')
forfolder2 =  pkg_resources.resource_filename('Tool4ASN', 'Script/')


#def script():
    #outpath = str(os.getcwd())
    #shutil.copy(forfolder1, outpath)
    #shutil.copy(forfolder2, outpath)