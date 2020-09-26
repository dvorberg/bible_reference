#!/usr/bin/env python
# -*- coding: utf-8; -*-

##  Copyright 2018–20 by Diedrich Vorberg <diedrich@tux4web.de>
##
##  All Rights Reserved
##
##  For more Information on orm see the README file.
##
##  This program is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 2 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program; if not, write to the Free Software
##  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##
##  I have added a copy of the GPL in the file COPYING

"""
Convenience module.
"""

from .bible_reference import Canon, default_canon

default = default_canon

king_hames = Canon("KingJames")
"""
This is the canon used by King James Version (my 1973 Holman Edition)
"""

BHS = Canon("BHS")
"""
The masorete canon as used in the Biblia Hebraica Stuttgartensia,
5. Auflage 1997, Stuttgart 1969/77; cf. `./BHS.canon`.
"""

LXX = Canon("LXX")
"""
Septuaginta. Edidit Alfred Rahlfs. Editio Quinta. Stuttgart, 1935;
cf. `./LXX.canon`.
"""

