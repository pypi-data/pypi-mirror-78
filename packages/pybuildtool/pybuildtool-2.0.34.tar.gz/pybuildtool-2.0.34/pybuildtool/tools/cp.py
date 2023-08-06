""" Copy files.
"""
from shutil import copyfile, Error
from pybuildtool import BaseTask

tool_name = __name__

class Task(BaseTask):

    name = tool_name

    def perform(self):
        if len(self.file_in) != 1:
            self.bld.fatal('%s only need one input, got %s' % (
                    tool_name.capitalize(), repr(self.file_in)))

        if len(self.file_out) != 1:
            self.bld.fatal('%s can only have one output, got %s' % (
                    tool_name.capitalize(), repr(self.file_out)))

        try:
            copyfile(self.file_in[0], self.file_out[0])
            return 0
        except Error:
            self.bld.fatal('tried to copy file to itself')
        except IOError:
            self.bld.fatal('destination location cannot be written')
        return 1
