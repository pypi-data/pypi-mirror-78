import numpy
from bllipparser import RerankingParser
from nltk import Tree
from nltk.data import find
from gensim.utils import tokenize
from nltk.corpus import stopwords
import os
import sys
import shutil
import warnings
import re
import string


class ConjunctionParser(object):
    """Represents a single parse (sub)tree in Penn Treebank format. This
    wraps the InputTree structure in the Charniak parser."""
    def __init__(self):
        self._parser = parser = RerankingParser.fetch_and_load('WSJ-with-AUX', verbose=False)
    def parse(self, sentence):
        from bllipparser import tokenize
        if ' and' not in sentence:
            return [sentence]
        orig = sentence
    
        parser = self._parser

        best = parser.parse(sentence) 
        
        parse_str = str(best.get_parser_best().ptb_parse)
        t = Tree.fromstring(parse_str)
        t1 = t
        verbs = []
        for subtree in t.subtrees():
            next_level_trees_labels = [item for item in subtree.subtrees()]
            if subtree.label() == "VB" and ("VP" not in str(next_level_trees_labels[1:])): 
                leaves_and_tags = subtree.pos()
                try:
                    verb = [item[0] for item in leaves_and_tags if item[1] == 'VB']
                    verbs.extend(verb)
                except:
                    verb = [item[0] for item in leaves_and_tags][0]
                    verbs.append(verb)
        oxford_flag = False
        and_flag = False
        if len(verbs) > 1:
            # If verbs are joined with "and" and no other text inbetween, consider them one verb.
            # Should this even be the case though? Can't we just apply the verbs to each noun phrase?
            leaves = ' '.join([leaf[0] for leaf in t.pos()])
            new_verbs = []
            for i in range(0, len(verbs) - 1):
                # For every verb and following verb in our list of verbs...
                verb_and_verb = verbs[i] + ' and ' + verbs[i + 1]
                verb_comma_verb = verbs[i] + ' , ' + verbs[i + 1]
                verb_comma_and_verb = verbs[i] + ' , and ' + verbs[i + 1]
                if verb_and_verb in leaves:
                    new_verb = [verb_and_verb]
                    and_flag = True
                elif verb_comma_verb in leaves:
                    verb_comma_verb = verbs[i] + ', ' + verbs[i + 1]
                    new_verb = [verb_comma_verb]
                elif verb_comma_and_verb in leaves:
                    verb_comma_and_verb = verbs[i] + ', and ' + verbs[i + 1]
                    new_verb = [verbs[i - 1] + ', ' + verb_comma_and_verb]
                    oxford_flag = True
                    flag_verb = new_verb[0]
                else:
                    new_verb = [verbs[i], verbs[i + 1]]
                new_verbs.extend(new_verb)
            if oxford_flag:
                new_verbs = new_verbs[new_verbs.index(flag_verb):]
        else:
            new_verbs = verbs
        if len(new_verbs) > 1:
            # If there's still more than one verb, they reference different nouns and can be separated into sentences 
            # starting with the verb
            verb_inds = []
            for verb in new_verbs:
                if len(list(set(new_verbs))) == len(new_verbs):
                    verb_inds.append([leaf[0] for leaf in t.pos()].index(verb))
                else:
                    #Account for duplicates of the same verb to make robust to run-on sentences
                    inds = [i for i, x in enumerate([leaf[0] for leaf in t.pos()]) if x == verb]
                    verb_inds.extend(inds)
                    verb_inds = list(set(verb_inds))
                    verb_inds.sort()
            new_sentences = [' '.join([leaf[0] for leaf in t.pos()][i:j]) for i,j in zip(verb_inds, verb_inds[1:]+[None])]
            new_sentences = [sentence[:-4] if sentence[-4:] == ' and' else sentence for sentence in new_sentences]
        else:
            new_sentences = [sentence]
        processed_sentences = []
        prep_flag = False
        for sentence in new_sentences:
            # Check again for and now that some sentences have split into two
            if 'and' not in sentence:
                from gensim.utils import tokenize
                if len(list(tokenize(sentence))) > 1:
                    processed_sentences.append(sentence)
                continue
            # At this point, we have a verb (or verbs) which is somewhere in new_verbs and somewhere in our sentence, and 'and' joining
            # together two or more noun/adjective phrases (either like: 'flashing metal system and gutters' or like 
            # 'gutters and wall and rake trim', or like 'gypsum walls, banister, and new gutters')
            # Goal here is to apply the verb (or verbs) that is in this sentence to each of the noun phrases.
            sentence_verbs = [verb for verb in verbs if verb in sentence]
            # Remove new_verbs from sentence first
            for new_verb in new_verbs:
                if new_verb in sentence:
                    sentence = sentence[sentence.index(new_verb):]
                    sentence = sentence.replace(new_verb, '').strip()
            noun_phrases = []
            # Check for prepositional phrases
            best = parser.parse(sentence)
            parse_str = str(best.get_parser_best().ptb_parse)
            t = Tree.fromstring(parse_str)
            pp_subtree = [subtree for subtree in t.subtrees() if subtree.label() == 'PP' and 'and' in [leaf[0] for leaf in subtree.pos()]]
            if len(pp_subtree) > 0:
                prep_flag = True
                pp_subtree = pp_subtree[0]
                pp = [leaf[0] for leaf in pp_subtree.pos()][0]
                before_pp = sentence.split(' ' + pp + ' ')[0] + ' ' + pp
                after_pp = sentence.split(' ' + pp + ' ')[1].strip()
                sentence = after_pp
        #     Split on a comma, comma and, or and?
            noun_list = sentence.split(', and ')
            # Now we have a list, with length 1 if that wasn't found
            noun_list = [sent.split(', ') for sent in noun_list]
            noun_list = [item for sublist in noun_list for item in sublist]
            noun_list = [sent.split(' and ') for sent in noun_list]
            noun_list = [item for sublist in noun_list for item in sublist]
            # Now that we have the noun phrases, apply the verbs in verbs to each noun phrase
            for verb in sentence_verbs:
                for noun in noun_list:
                    if prep_flag:
                        noun = before_pp + ' ' + noun
                    processed_sentences.append(verb + ' ' + noun)
        if processed_sentences == []:
            processed_sentences = [orig]
        processed_sentences = list(set(processed_sentences))
        return processed_sentences