#!/usr/bin/python

MODULE = '/Users/okoeroo/dvl/scripts/python/stanley/pattern-2.6'
import sys
if MODULE not in sys.path: sys.path.append(MODULE)
from pattern.en import parse, parsetree, pluralize, singularize

# statement
# question
# excalamtion, equal to statement with emotion
# command


class InputSentence(object):
    def __init__(self):
        return

    def introspect(self):
        return {'io_in':'stdin', 'io_out':'raw_String'}

    def addStorage(self, storage):
        self.storage = storage

    def process(self, parent):
        buf = raw_input('||>>|| # ')
        self.storage.store(buf, index='sentence', type='input', id='1')
        return

class Process(object):
    def __init__(self):
        return

    def introspect(self):
        return {'io_in':'raw_String', 'io_out':'String'}

    def addStorage(self, storage):
        self.storage = storage

    def process(self, parent):
        buf = self.storage.retrieve(index='sentence', type='input', id='1')
        if buf.lower().split()[0] in {"who", "where", "when", "why", "what", "which", "how"}:
            self.storage.store('question', index='sentence', type='sentence_type', id='1')

        # command, begin (first word here) with a nounce
        elif buf.lower().split()[0] in {"give", "show", "do", "fix", "stop", "start", ""}:
            self.storage.store('command', index='sentence', type='sentence_type', id='1')

        s = buf
        s = parse(s,
                tokenize = True,  # Tokenize the input, i.e. split punctuation from words.
                tags = True,  # Find part-of-speech tags.
                chunks = True,  # Find chunk tags, e.g. "the black cat" = NP = noun phrase.
                relations = True,  # Find relations between chunks.
                lemmata = True,  # Find word lemmata.
                light = False)

#        print s
        for sentence in s.split():
            for w in sentence:
                print w

        return


class Output(object):
    def __init__(self):
        return

    def introspect(self):
        return {'io_in':'String', 'io_out':'stdout'}

    def addStorage(self, storage):
        self.storage = storage

    def process(self, parent):
        buf = self.storage.retrieve(index='sentence', type='input', id='1')
        print buf

        try:
            buf = self.storage.retrieve(index='sentence', type='sentence_type', id='1')
            print buf
        except:
            pass
        return


import uuid, base64
from collections import defaultdict
class MainBrainStorage(object):
    data = defaultdict(lambda : defaultdict(dict))

    def __init__(self):
        return

    def store(self, obj, **kwargs):
        val_index = kwargs.pop('index', None)
        val_type  = kwargs.pop('type', None)
        val_id    = kwargs.pop('id', uuid.uuid4())

        if val_index is None: raise
        if val_type  is None: raise
        if val_id    is None: raise

        # Store at coordinate, similar to ElasticSearch
        self.data[val_index][val_type][val_id] = obj
        return val_id

    def retrieve(self, **kwargs):
        val_index = kwargs.pop('index', None)
        val_type  = kwargs.pop('type', None)
        val_id    = kwargs.pop('id', None)

        if val_index is None: raise
        if val_type  is None: raise
        if val_id    is None: raise

        # Retrieve at coordinate, similar to ElasticSearch
        return self.data[val_index][val_type][val_id]

class MainBrain(object):
    modules = []

    def __init__(self):
        self.storage = MainBrainStorage()

    def addModule(self, module):
        module.addStorage(self.storage)
        self.modules.append(module)

    def selectModuleByCriteria(self, **kwargs):
        io_in  = kwargs.pop('io_in',  None)
        io_out = kwargs.pop('io_out', None)

        if io_in is not None:
            for m in self.modules:
                if m.introspect()['io_in'] == io_in:
                    return m

        if io_out is not None:
            for m in self.modules:
                if m.introspect()['io_out'] == io_out:
                    return m

        return None

    def start(self):
        # Start here
        m = self.selectModuleByCriteria(io_in='stdin')

        while m:
            m.process(self)

            # Finished
            if m.introspect()['io_out'] == 'stdout':
                # Yes
                break
            else:
                # Select next
                m = self.selectModuleByCriteria(io_in=m.introspect()['io_out'])



### Main ###
if __name__ == "__main__":
    mb = MainBrain()

    mb.addModule(Output())
    mb.addModule(Process())
    mb.addModule(InputSentence())

    mb.start()
