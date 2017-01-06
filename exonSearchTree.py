'''
Making an exon search tree which will hopefully speed up the whole get_variants section.
Then again, it might slow it down. Maybe I'll test it both ways.
Or maybe I won't. Who knows what I'll do? I'm a WILD CARD

It's a several-layer tree. There's a chromosome node, which has daughter "chunk" nodes (one chunk for each million
BP in a chromosome), which have leaf nodes for each exon. (An exon that spans multiple chunk nodes will appear
in all, since we'll be searching for single positions...I think.)
'''

class ExonSearchTree:
	def __init__(self, chunk_size = 1000000):
		self.chr_nodes = {}
		self.chunk_size = chunk_size
	
	def print_tree(self):
		for node in self.chr_nodes:
			self.chr_nodes[node].print_node()
	
	def add_exon(self, chr, start, end, name = "."):
		chr = str(chr)
		try:
			self.chr_nodes[chr].add_node(start, end, name)
		except KeyError:
			self.chr_nodes[chr] = ESTChrNode(chr, self.chunk_size)
			self.chr_nodes[chr].add_node(start, end, name)
			
	def find_exon(self, chr, pos):
		chr = str(chr)
		return self.chr_nodes[chr].find_exon(pos)

class ESTChrNode:
	# A layer of chromosome nodes
	def __init__(self, chr_num, chunk_size):
		self.chr_num = chr_num
		self.chunk_nodes = {}
		self.chunk_size = chunk_size
	
	def add_node(self, start, end, name):
		start_chunk = start/self.chunk_size
		end_chunk = end/self.chunk_size
		for chunk in range(start_chunk, end_chunk+1):
			try:
				self.chunk_nodes[chunk].add_node(start, end, name)
			except KeyError:
				self.chunk_nodes[chunk] = ESTChunkNode(self.chr_num, chunk)
				self.chunk_nodes[chunk].add_node(start, end, name)
	
	def find_exon(self, pos):
		chunk = pos/self.chunk_size
		return self.chunk_nodes[chunk].find_exon(pos)

	def print_node(self):
		for node in self.chunk_nodes:
			self.chunk_nodes[node].print_node()

class ESTChunkNode:
	# A layer of chunk nodes (for now, every million BP gets its own chunk node)
	def __init__(self, chr, number):
		self.chr = chr
		self.chunk_num = number
		self.exons = {}
	
	def add_node(self, start, end, name):
		self.exons[start] = ESTExonLeaf(self.chr, start, end, name)
	
	def find_exon(self, pos):
		names = []
		for ex in self.exons:
			if pos >= ex:
				exon = self.exons[ex]
				if pos <= exon.end:
					 names.append(exon.name)
		return names

	def print_node(self):
		for node in self.exons:
			self.exons[node].print_exon()

class ESTExonLeaf:
	# The leaf node that contains the exon.
	def __init__(self, chr, start, end, name):
		self.chr = chr
		self.start = start
		self.end = end
		self.name = name
	
	def print_exon(self):
		print self.chr, self.start, self.end, self.name
		
if __name__=="__main__":
	est = ExonSearchTree(1000)
	est.add_exon(1, 100000000, 100002000, "NP_5")
	est.add_exon('M', 999990, 1000500, "NP_6")
	est.add_exon('Q', 3939, 8858)
	est.print_tree()
	print est.find_exon('M', 999995)
	print est.find_exon('1', 100000001)