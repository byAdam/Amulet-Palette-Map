from amulet.api.block import Block
import numpy as np
import re
import amulet_nbt
import copy
import ast

operation_options = { "Map File": ["file_open"] }

class BlockMap:
	def __init__(self, old_name, old_props, new_name, new_props):
		self.old_name = old_name
		self.old_props = old_props

		self.new_name = new_name
		self.new_props = new_props

	def get_new(self, old):
		args = copy.deepcopy(self.new_props)
		if args == "*":
			args = old.properties

		for a in args:
			if args[a] == "*":
				args[a] = old.properties[a]
			
			if args[a][0] == "$":
				x = args[a][1:]

				if x in old.properties:
					args[a] = old.properties[x]
				else:
					args[a] = ""

			if type(args[a]) is str:
				args[a] = amulet_nbt.from_snbt(args[a])
			
		return Block(*self.new_name.split(":"), args)

def property_match(a, b):
	return a == b or b == "*"

def find_blocks_in_palette(p, bm):
	blocks = []

	name = bm.old_name + "$"
	props = bm.old_props

	for b in p._block_to_index_map:
		## If the name regex matches block name
		if re.match(name, b.namespaced_name):
			## If all properties match
			if props == "*" or all(prop in b.properties and property_match(b.properties[prop], props[prop]) for prop in props):
				blocks.append(b)
	
	return blocks

def change_block_in_palette(p, o, bm):
	# Get block index and remove from block_to_index map`
	if o in p._block_to_index_map:
		i = p._block_to_index_map[o]
		new = bm.get_new(o)

		i = p._block_to_index_map[o]
		del p._block_to_index_map[o]

		# Add new block to block_to_index map
		p._block_to_index_map[new] = i
		# Add new block to _index_to_block
		p._index_to_block[i] = new

		return i
	return -1

def parse_map_file(mf):
	def part_split(x):
		if "<" in x:
			a, b = x.split("<")
			a = a.strip()
			b = b.strip()
			return a, b if b == "*" else ast.literal_eval(b)
		else:
			return x.strip(), "_"

	maps = []

	line_no = 0
	for line in mf:
		line_no += 1
		line = line.strip()
		## Commnets
		if line[0] == "#":
			continue
		
		try:
			old, new = line.split(">")
			
			old_name, old_props = part_split(old)
			new_name, new_props = part_split(new)

			## If blank properties, it should be any property
			if old_props == "_":
				old_props = "*"
			
			if new_props == "_":
				new_props = {}

			maps.append(BlockMap(old_name, old_props, new_name, new_props))
		except:
			raise("Invalid map file at line {}".format(line_no))

	return maps

def operation(world, dimension, selection, options):
	map_file = open(options["Map File"])
	maps = parse_map_file(map_file)

	changed_ids = []

	## Loop through blockmaps
	for bm in maps:
		blocks = find_blocks_in_palette(world.palette, bm)
		print(blocks)

		# Loop through found blocks
		for b in blocks:
			i = change_block_in_palette(world.palette, b, bm)

			if i >= 0:
				changed_ids.append(i)
	

	## Loop through all chunks, and set changed=true if any block has been changed in chunk 
	for chunk_c in world.world_wrapper.all_chunk_coords(dimension):
		chunk = world.get_chunk(chunk_c[0], chunk_c[1], dimension)

		flat_chunk = chunk.blocks.__array__()
		if any([b in flat_chunk for b in changed_ids]):
			chunk.changed = True

export = {
    "name": "Palette Map",
    "operation": operation,
    "options": operation_options
}