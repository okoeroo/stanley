#!/usr/bin/python


# statement
# question
# excalamtion, equal to statement with emotion
# command


class Input(object):
    def __init__(self):
        return

    def introspect(self):
        return {'io_in':'stdin', 'io_out':'raw_String'}

    def addStorage(self, storage):
        self.storage = storage

    def process(self, parent):
        parent.io_in_buffer = raw_input('||>>|| # ')
        return

class Process(object):
    def __init__(self):
        return

    def introspect(self):
        return {'io_in':'raw_String', 'io_out':'String'}

    def addStorage(self, storage):
        self.storage = storage

    def process(self, parent):
        parent.io_out_buffer = parent.io_in_buffer
        return


class Output(object):
    def __init__(self):
        return

    def introspect(self):
        return {'io_in':'String', 'io_out':'stdout'}

    def addStorage(self, storage):
        self.storage = storage

    def process(self, parent):
        print parent.io_out_buffer
        return

class MainBrainStorage(object):
    def __init__(self):
        return

    def store(self, obj):
        return obj_id

    def retrieve(self, obj_id):
        return obj



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
    mb.addModule(Input())

    mb.start()
