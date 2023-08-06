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

import importlib as imp

import pypath.inputs as inputs
import pypath.share.session as session


class Ontology(session.Logger):
    
    all_relations = {
        'is_a',
        'part_of',
        'occurs_in',
        'regulates',
        'positively_regulates',
        'negatively_regulates',
    }
    
    
    def __init__(
            self,
            terms = None,
            ancestors = None,
            descendants = None,
            term = None,
            name = None,
            input_method = None,
        ):
        """
        Loads data about the terms and their relations in an ontology.
        """
        
        if not hasattr(self, '_log_name'):
            
            session_mod.Logger.__init__(self, name = 'ontology')
        
        self._terms_provided = terms
        self._ancestors_provided = ancestors
        self._descendants_provided = descendants
        self._term_provided = term
        self._name_provided = name
        self._input_mehod = input_mehod
        
        self._load()
    
    
    def reload(self):
        """Reloads the object from the module level."""
        
        modname = self.__class__.__module__
        mod = __import__(modname, fromlist = [modname.split('.')[0]])
        imp.reload(mod)
        new = getattr(mod, self.__class__.__name__)
        setattr(self, '__class__', new)
    
    
    def _load(self):
        
        self._log('Populating ontology.')
        
        self._set_input_method()
        self._load_terms()
        self._load_tree()
        self._set_aspect()
        self._set_name()
        self._set_term()
        
        self._log('Ontology populated.')
    
    
    def _set_input_method(self):
        
        self._input_mehod = inputs.get_method(self._input_mehod)
    
    
    def _load_terms(self):
        
        self._terms = self._terms_provided or self.input_mehod()
    
    
    def _load_tree(self):
        
        self._log('Building the ontology tree.')
        
        self.ancestors = (
            self._ancestors_provided or
            self._merge_aspects(
                dataio.go_ancestors_quickgo()
            )
        )
        self.descendants = (
            self._descendants_provided or
            self._merge_aspects(
                dataio.go_descendants_quickgo()
            )
        )
    
    
    def _set_aspect(self):
        
        self.aspect = (
            self._aspect_provided or
            dict(
                (term, asp)
                for asp, terms in iteritems(self._terms)
                for term in terms.keys()
            )
        )
    
    
    def _set_name(self):
        
        self._log('Collecting short names of ontology terms.')
        
        self.name = (
            self._name_provided or
            dict(
                i
                for ii in self._terms.values()
                for i in iteritems(ii)
            )
        )
    
    
    def _set_term(self):
        
        self.term = (
            self._term_provided or
            dict(
                reversed(i)
                for i in iteritems(self.name)
            )
        )
    
    
    def is_term(self, term):
        """
        Tells if ``term`` is a GO accession number.
        """
        
        return term in self.name
    
    
    def is_name(self, name):
        """
        Tells if ``name`` is a GO term name.
        """
        
        return name in self.term
    
    
    def get_name(self, term):
        """
        For a GO accession number returns the name of the term.
        If ``term`` is already a GO term name returns it unchanged.
        """
        
        return (
            term
                if self.is_name(term) else
            None
                if term not in self.name else
            self.name[term]
        )
    
    
    def get_term(self, name):
        """
        For a GO term name returns its GO accession number.
        If ``name`` is a GO accession returns it unchanged.
        """
        
        result = (
            name
                if self.is_term(name) else
            None
                if name not in self.term else
            self.term[name]
        )
        
        if result is None:
            
            self._log('Could not find GO term name: `%s`.' % name)
        
        return result
    
    
    def terms_to_names(self, terms):
        """
        For a list of GO names returns a list of tuples with the terms
        and their names.
        """
        
        return [(term, self.get_name(term)) for term in terms]
    
    
    def terms_to_names_aspects(self, terms):
        """
        For a list of GO terms returns a list of tuples with the terms,
        their names and the ontology aspect.
        """
        
        return [
            (term, self.get_name(term), self.get_aspect(term))
            for term in terms
        ]
    
    
    def names_to_terms(self, names):
        """
        For a list of GO terms returns a list of tuples with the terms
        and their names.
        """
        
        return [(self.get_term(name), name) for name in names]
    
    
    def names_to_terms_aspects(self, names):
        """
        For a list of GO namess returns a list of tuples with the terms,
        their names and ontology aspects.
        """
        
        return [
            (self.get_term(name), name, self.aspect_from_name(name))
            for name in names
        ]
    
    
    def aspect_from_name(self, name):
        """
        Tells about a Gene Ontology term name which aspect does it belong to.
        """
        
        term = self.get_term(name)
        
        if term:
            
            return self.get_aspect(term)
    
    
    @staticmethod
    def _merge_aspects(dct):
        
        dct['P'].update(dct['C'])
        dct['P'].update(dct['F'])
        return dct['P']
    
    
    def subgraph_nodes(
            self,
            direction,
            terms,
            relations = None,
            include_seed = True,
        ):
        """
        Returns a set of all nodes either in the subgraph of ancestors 
        or descendants of a single term or a set of terms.
        
        :param str direction:
            Possible values: `ancestors` or `descendants`.
        :param bool include_seed:
            Include ``terms`` in the subgraph or only the related nodes.
        """
        
        relations = relations or self.all_relations
        
        if isinstance(terms, common.basestring):
            
            terms = {terms}
        
        graph = getattr(self, direction)
        subgraph = set(terms) if include_seed else set()
        
        for term in terms:
            
            for related, relation in graph[term]:
                
                if relation not in relations:
                    
                    continue
                
                if related not in subgraph:
                    
                    subgraph.update(
                        self.subgraph_nodes(direction, related, relations)
                    )
                    subgraph.add(related)
        
        return subgraph
    
    
    def get_all_ancestors(self, terms, relations = None, include_seed = True):
        """
        Returns a set of all ancestors of a single term or a set of terms.
        """
        
        terms = self.set_of_terms(terms)
        
        return self.subgraph_nodes(
            direction = 'ancestors',
            terms = terms,
            relations = relations,
            include_seed = include_seed,
        )
    
    
    def get_all_descendants(
            self,
            terms,
            relations = None,
            include_seed = True,
        ):
        """
        Returns a set of all descendants of a single term or a set of terms.
        """
        
        terms = self.set_of_terms(terms)
        
        return self.subgraph_nodes(
            direction = 'descendants',
            terms = terms,
            relations = relations,
            include_seed = include_seed,
        )
    
    
    def get_aspect(self, term):
        """
        For a GO term tells which aspect does it belong to.
        Returns `None` if the term is not in the ontology.
        """
        
        if term in self.aspect:
            
            return self.aspect[term]
    
    
    def all_from_aspect(self, aspect):
        """
        Returns the set of all GO terms of one aspect.
        """
        
        return set(
            term
            for term, asp in iteritems(self.aspect)
            if asp == aspect
        )
    
    
    def is_root(self, term):
        """
        Tells if a term is the root of the graph i.e. it has no ancestors.
        """
        
        return term in self.ancestors and bool(self.ancestors[term])
    
    
    def is_leaf(self, term):
        """
        Tells if a term is a leaf of the graph i.e. it has no descendants.
        """
        
        return (
            (
                term in self.ancestors and
                term not in self.descendants
            ) or
            not bool(self.descendants[term])
        )
    
    
    def lowest(self, terms, *args):
        """
        From a set of terms returns the lowest level ones, removing all which
        are parents of some others in the set.
        """
        
        return self.flatten(terms, *args)
    
    
    def highest(self, terms, *args):
        """
        From a set of terms returns the highest level ones, removing all
        which are descendants of some others in the set.
        """
        
        return self.flatten(terms, *args, lowest = False)
    
    
    def flatten(self, terms, *args, lowest = True):
        """
        Returns a set of terms by removing either all redundant ancestors or
        descendants from the provided set terms. By removing the ancestors
        you get the lowest level set of terms, by removing the descendants
        the result will be the highest level non-redundant terms.
        
        :param str direction:
            Either `lowest` or `highest`.
        """
        
        terms = self.set_of_terms(terms, *args)
        
        method = getattr(
            self,
            'get_all_%s' % (
                'ancestors' if lowest else 'descendants'
            )
        )
        
        return (
            terms -
            set.union(
                *(
                    method(term, include_seed = False)
                    for term in terms
                )
            )
        )
    
    
    def set_of_terms(self, terms_names, *args):
        """
        Converts anything to a set of terms. ``terms_names`` can be either a
        single term or name or an iterable of terms and names.
        """
        
        return self.set_of(terms_names, *args)
    
    
    def set_of_names(self, terms_names, *args):
        """
        Converts anything to a set of names. ``terms_names`` can be either a
        single term or name or an iterable of terms and names.
        """
        
        return self.set_of(terms_names, *args, to_terms = False)
    
    
    def set_of(self, terms_names, *args, to_terms = True):
        """
        Converts anything to a set of terms or names.
        ``terms_names`` can be either a single term or name or an iterable
        of terms and names.
        
        :param bool to_terms:
            The target identifier type is `term`; if ``False`` the target
            will be `name`.
        """
        
        if isinstance(terms_names, common.basestring):
            
            terms_names = {terms_names}
            
        elif not isinstance(terms_names, set):
            
            terms_names = set(terms_names)
        
        if args:
            
            terms_names.update(set(args))
        
        method = getattr(
            self,
            'get_term' if to_terms else 'get_name'
        )
        
        return {
            method(term) for term in terms_names
        }
