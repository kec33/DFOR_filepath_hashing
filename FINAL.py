import os
import psutil
import hashlib

#------------------------------------------------------------

def discover_disks():                                       #Discovers every disk that is on the system
    disks = []
    partitions = psutil.disk_partitions(all=True)
    for partition in partitions:
        if partition.mountpoint not in disks:
            disks.append(partition.mountpoint)
    return disks

def find_file_in_disks(filename, disks):                    #Finds all the files with the same name on the system
    f_names = []                                            
    file_found = False
    for disk in disks:
        for root, directories, files in os.walk(disk):
            for file in files:
                if file == filename:
                    ff = os.path.join(root, file)
                    f_names.append(ff)
                    file_found = True
    if not file_found:
        print(f"\nFile '{filename}' not found in any disk.")
    return f_names

def hash_file(file_path, algorithm):                         #Calculates the hash value of a file.
    hash_value = hashlib.new(algorithm)
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_value.update(chunk)
    return hash_value.hexdigest()

#------------------------------------------------------------

def main():
    filename = input('Enter the file name (with extension): ')
    algorithm = input("Choose a hashing algorithm (e.g., md5, sha1, sha256): ")

    disks = discover_disks()
    file_list = find_file_in_disks(filename, disks)
    
    if bool(file_list):
        print("\n\nThese are the full paths of all the files with that name: \n")
        for file in file_list:
            print(file, "\n")
        print("\n")
    else:
        print("\nThere are no files to display.")

    for file_path in file_list:
        try:
            hash_value = hash_file(file_path, algorithm)
            print(f"The hash value {algorithm} of the file: `{file_path}` is ---> {hash_value} \n")
        except:
            print("Not found")

if __name__ == '__main__':
    main()
