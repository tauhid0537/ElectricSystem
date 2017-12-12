# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ElectricSystems
                                 A QGIS plugin to develop, process, validate
 and Analyze Electricity Network data
                             -------------------
        begin                : 2017-01-01
        copyright            : (C) 2017 by Tauhidul Islam
        email                : tislam@nreca-intl.org
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

def name():
  return "NRECA Electric Systems"

def version():
  return "Version 1.0"

def description():
  return "A QGIS plugin to develop, process, validate and Analyze Electricity Network data"

def qgisMinimumVersion():
  return "1.8"

def experimental():
  return True

def author():
  return "MD TAUHIDUL ISLAM"

def authorName():
  return author()

def email():
  return "tislam@nreca-intl.org, tauhid0537@gmail.com"

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    from .mainclass import ElectricSystems
    return ElectricSystems(iface)
