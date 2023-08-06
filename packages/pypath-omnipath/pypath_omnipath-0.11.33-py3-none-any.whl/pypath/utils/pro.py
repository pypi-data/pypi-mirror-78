#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  This file is part of the `pypath` python module
#  Provides many functions to interact with Gene Ontology data.
#
#  Copyright
#  2014-2020
#  EMBL, EMBL-EBI, Uniklinik RWTH Aachen, Heidelberg University
#
#  File author(s): Dénes Türei (turei.denes@gmail.com)
#                  Nicolàs Palacio
#                  Olga Ivanova
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  Website: http://pypath.omnipathdb.org/
#

import pypath.utils.ontology as ontology


class ProteinOntology(ontology.Ontology):
    
    all_relations = {
        'is_a',
        'derives_from',
    }
    
    
    def __init__(
            self,
            terms = None,
            ancestors = None,
            descendants = None,
            term = None,
            name = None,
        ):
        """
        Loads data about Protein Ontology terms and their relations.
        """
        
        session_mod.Logger.__init__(self, name = 'pro')
