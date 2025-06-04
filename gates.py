# file: gates.py
# content: implementation of standard gates
# created: 2025 June 4 Wednesday
# author: Roch Schanen

from rom import rom

######################################################################
###                                                               NAND
######################################################################

class gate(logic_device):

	def add_input(self, port, subset = None):
		
