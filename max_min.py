#Marcela Uliano-Silva
import glob

#this function outputs the smallest and the largest value in a list
def max_min(inte):
    kmer_profs=[]
    int_list=[int(a) for a in inte]
    for i in int_list:
        kmer_profs.append(i)
    maxi =  max(kmer_profs)
    mini =  min(kmer_profs)
    minMax = str(mini) + "\t" + str(maxi)
    return minMax

#here I'm openning a list to append all names of files I'm listing with glob.iglob (files in the current folder that end i .mitohifiReads)
fils=[]
for filepath in glob.iglob('*.mitohifiReads'):
    fils.append(filepath)
#then I loop over the files appended to fils to run the function max_min 
for i in fils:
   with open(i)as file:
        print(max_min(file) + "\t" +i)
