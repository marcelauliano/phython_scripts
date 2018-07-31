#Marcela Uliano-Silva, July 2018
#Simple script to write patterns with a numeric range and output them to individual files.

names = ("[\n\"raw_reads.")
names2 = (".las.rr_hctg_track.partial.msgpack\"\n]")
for i in range(1,465):
	with open('partial%i.json' %i, 'w') as output:
		output.write(str(names) + str(i) + str(names2))
	
