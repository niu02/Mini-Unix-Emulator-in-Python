class File: #everything is a file and every file has an owner   
    def chown(self, new_owner): #owner attribute has not been set here as subclasses have different initiliased attributes so cannot inherit 'owner'
        self.owner = new_owner #sets a specified string as the new owner of the file
        
    def chmod(self, numb): #implementing chmod using octal permission representation
        new_perm = "" 
        permission = [0,0,0] 
        if numb in [1,3,5,7]: #each list includes the numbers that each permission is active in
            permission[2] = 'x' #execute permission
        if numb in [2,3,6,7]:
            permission[1] = 'w' #write permission
        if numb in [4,5,6,7]:
            permission[0] = 'r' #read permission
        if numb > 7: #7 is the highest permission number
            return
        for i in permission:
            if i == 0:
                new_perm += "-"
            else:
                new_perm += f"{i}"
        self.perm = new_perm
        

class PlainFile(File):
    def __init__(self, name, owner="default", perm="rw-"):
        self.name = name
        self.owner = owner
        self.perm = perm
    
    def __repr__(self): #to return 'PlainFile' + its name when called
        return f'PlainFile({self.name})'

class Directory(File):
    def __init__(self, name, file_list, owner="default", perm="rwx"):
        self.name = name
        self.file_list = file_list
        self.owner = owner
        self.perm = perm
    
    def __repr__(self): #to return 'Directory' + its name + the files it contains when called
        return f'Directory({self.name},{self.file_list})'
    
    def ls(self, level=0): #level keeps track of levels of directories/files, and is set at 0 to begin with
        print('\t' * level + self.name) #number of indents are determined (multiplied) by level depending on how deep down the directories have gone
        for file in self.file_list: #explores each file in the directory's file list
            if type(file) == Directory:
                file.ls(level+1) #level increases by 1 when entering a new directory
            else:
                print('\t' * (level+1) + file.name) #adds an indent & level increases by 1 when printing the files of a new directory

                     
class FileSystem(Directory):
    def __init__(self, directory):
        self.directory = directory
        self.owner = self.directory.owner
          
    def pwd(self): #prints name of current directory
        return self.directory.name
    
    def ls(self, flag=""): 
        for file in self.directory.file_list:
            if flag == "-l": #prints full listing of file permissions and owner
                print(file.perm + "\t\t" + file.owner + "\t" + file.name)
            else:
                print(file.name) #prints only the name of files within the current directory      
    
    def cd(self, next_directory): #changes directory
        for file in self.directory.file_list:
            if next_directory == file.name and type(file) == Directory: #to ensure the next_directory name is an existing directory and not a PlainFile
                self.parent_directory = self.directory
                self.directory = file
                return
        if next_directory == "..":
            self.directory = self.parent_directory
            return
        print("That directory does not exist!") #if next_directory doesn't already exist or isn't a directory

    def create_file(self, name, perm="rw-"):
        for file in self.directory.file_list:
            if name == file.name and type(file) == PlainFile: #if a file already exists with the same name, the method will print an error and not execute
                print("That file already exists.")
                return
        new_file = PlainFile(name, self.directory.owner, perm) #creates a new PlainFile with the specified name if it's available
        self.directory.file_list += [new_file] #adds the new file to the directory
        
    def mkdir(self, name, owner="default"): #making a new directory         
        for file in self.directory.file_list:
            if name == file.name and type(file) == Directory: #if a directory already exists with the same name, the method will print an error and not execute
                print("That directory already exists.")
                return
        new_directory = Directory(name, [], owner) #creates a new empty directory if the name is available
        self.directory.file_list += [new_directory] #adds the directory to the current directory
        
    def rm(self, name, flag=""): #to remove a file or directory
        new_list = [] #a new directory list to contain all previous files minus the file being removed
        execute = True
        for file in self.directory.file_list:
            if name == file.name and type(file) == Directory and file.file_list != []: #ensures the file being removed is not a populated directory
                print("Sorry, that directory is not empty.")
            elif name == file.name: #ensures the file being removed is not added to the new list
                continue
            new_list += [file]
        if flag == "-i": #initiates a prompt before deleting
            prompt = input("Are you sure you want to remove this?\nEnter Y (yes) or N (no): ")
            if prompt == "Y" or prompt == "y":
                pass
            elif prompt == "N" or prompt == "n":
                execute = False
            else:
                print("Invalid answer, remove unsuccessful.") 
                execute = False
        while execute:
            self.directory.file_list = new_list #replaces the old directory file list with the new one, with the specified file removed
            break
    
    def find(self, name, parent=None):
        if parent == None: #parent keeps track of the original directory
            parent = self.directory
        path = False 
        for file in parent.file_list:
            if type(file) == Directory and file.name != name:
                path = self.find(name, file)
                if path: #breaks the loop if a match for name is found
                    break
            elif file.name == name:
                path = file.name #if there is a match, path will record the parent directory of name + file.name
                break
        if path: #if path has a value and thus returns True, this returns the path leading to name
            return parent.name + "/" + path
        return False #returns False when there is no match for name
    
    def wc(self, flag):
        if flag == "-L": #to print the character length of the longest file name in the current directory
            highest_len = ""
            for file in self.directory.file_list:
                if len(file.name) > len(highest_len):
                    highest_len = file.name
                else:
                    continue
            print(f"{len(highest_len)}\t{highest_len}")
        if flag == "-l": #to print the number of files in the current directory
            file_count = 0
            for file in self.directory.file_list:
                file_count += 1
            print(file_count)
    
    
                 


