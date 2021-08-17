import pickle

def simpleFileToDict(filename):
    to_be_dumped = {}
    with open(filename) as file:
        for line in file:
            key, value = line.split()
            to_be_dumped[key] = int(value)
    return to_be_dumped

def complexFileToDict(filename):
    to_be_dumped = {}
    with open(filename) as file:
        for line in file:
            key, _ , _ = line.split()
            to_be_dumped[key] = {}
        file.seek(0) # return the cursor to the first line of the file
        for line in file:
            key, value, number = line.split()
            to_be_dumped[key][value] = int(number)
    return to_be_dumped


#%% dumping to file
    
inserts_file = "common_inserts_ptbr.txt"
deletes_file = "common_deletes_ptbr.txt"
replaces_file = "common_replaces_ptbr.txt"

inserts_to_be_dumped = simpleFileToDict(inserts_file)
deletes_to_be_dumped = simpleFileToDict(deletes_file)
replaces_to_be_dumped = complexFileToDict(replaces_file)
pickle.dump(inserts_to_be_dumped, open("common_inserts_ptbr.p","wb"))
pickle.dump(deletes_to_be_dumped, open("common_deletes_ptbr.p","wb"))
pickle.dump(replaces_to_be_dumped, open("common_replaces_ptbr.p","wb"))


print(replaces_to_be_dumped)

