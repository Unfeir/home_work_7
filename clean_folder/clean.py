
import pathlib
import re
from shutil import move, unpack_archive
import sys

# directory = r"D:\study\GoIT\cours\python_core\module_6\DZ\for_tests"
# PATH = pathlib.Path(directory)
if len(sys.argv) <2:
    print("Please, enter dir")
    exit()
else:
    PATH = pathlib.Path(sys.argv[1])  
    print(PATH)  

########### create dict for cyrillic ###############
def translator():
    ''' Function created dict for normilize file name'''
    cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    translation = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    trans = {}  
    for c, t in zip(cyrillic_symbols,translation):
        trans[ord(c)] = t
        trans[ord(c.upper())] = t.upper()
    
    return trans
    
############# Normilize file name ##################
def normalize(f_name):
    '''take file name as argument and return normilize name'''
    trans = translator()
    name = re.sub(r"\W+", "_" , f_name)
    return name.translate(trans)
   

# test = ["My-doc%k", "my_pdf", "MY-рисунок", "Ёпе1с?ня"]
# for i in test:
#     print(normalize(i))


####### find all files in dir and call sort() ######################
def recursive_iterdir(path):
    ''' ітеруємось по заданій папці і відправляємо кожен файл на обробку до функції sort'''     
    
    for element in path.iterdir():
        if element.is_dir():
            recursive_iterdir(element)
        else:    
            sort(element)  # send D:\study\GoIT\cours\python_core\module_6\DZ\for_tests\folder2\folder2_2\folder2_2_1\dfdfd.docx
                
        

###### sort all files in dict ########################
def sort(element):
    ''' Приймає файл як Path і відповідно до словника створює папку 
    і переміщає до неї файл, 
    у випадку архіва - розпаковує у папку з тією самою назвою'''
 
    type_dict = {
    "images": ['JPEG', 'PNG', 'JPG', 'SVG'],
    "video": ['AVI', 'MP4', 'MOV', 'MKV'],
    "documents": ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    "audio": ['MP3', 'OGG', 'WAV', 'AMR'],
    "archives": ['ZIP', 'GZ', 'TAR'],
    "other": []
}
    
    new_stem = normalize(element.stem)
    extension = element.suffix.replace(".", "").upper()
    new_name = new_stem + "." + extension
    
    # parent_folder = path.parent
    for key, value in type_dict.items():
        if extension in value:
            new_folder = PATH.joinpath(key)
            new_folder.mkdir(exist_ok=True)
            if key == "archives":
                unpack_archive(element, new_folder.joinpath(new_stem))
                element.unlink()
                return
            else:
                element.rename(new_folder / new_name)
                #move(path, new_folder.joinpath(new_name[0])) # same but with shutil
                return
        
    new_folder = PATH.joinpath("other")
    new_folder.mkdir(exist_ok=True)
    element.rename(new_folder / new_name)
        
def cleaner(path):
    ''' delet all empty dir'''
    for item in path.iterdir():
        if item.is_dir():
            cleaner(item)
            if not any(item.iterdir()):
                item.rmdir()



    
    
def main_fun():
    global PATH
    if PATH.is_dir():
        recursive_iterdir(PATH)
        cleaner(PATH)
    else:
        print(f"There is no such dir: {PATH}")

if __name__ == '__main__':
    main_fun()
    print("Finish")

