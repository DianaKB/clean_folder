import argparse
import os
import shutil



files_expansion = {
    'imag':('.jpeg', '.png', '.jpg', '.svg'),
    'video':('.avi', '.mp4', '.mov', '.mkv'),
    'document':('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
    'music':('.mp3', '.ogg', '.wav', '.amr'),
    'achive':('.zip', '.gz', '.tar')}

files_expansion_exist = set()
noname_expansion = set()

parser = argparse.ArgumentParser(description='Сортировка папки')
parser.add_argument('path', type=str, help='Путь к папке,можно без кавычек' )
args = parser.parse_args()


def sort_file(parent_dir, current_path,
                                       current_file,name_dir):
    if not os.path.exists(os.path.join(parent_dir, name_dir)):
        os.mkdir(os.path.join(parent_dir, name_dir))
    path_replace = os.path.join(parent_dir, name_dir,
                                          normalize(current_file))
    #создание множества расширений существующих в parent_dir
    expanssion = os.path.splitext(current_file)[-1].strip()
    files_expansion_exist.add(expanssion)
    os.replace(current_path, path_replace)
    if name_dir =='archives':
        shutil.unpack_archive(path_replace,path_replace
                              .replace(expanssion,''))
      
    
def list_category(parent_dir,*name_dir):
    list_category = {}
    files  = os.listdir(os.path.join(parent_dir))
    for i in files:
        if os.path.isdir(os.path.join(parent_dir,i)) and i in name_dir:
            files = os.listdir(os.path.join(parent_dir,i))
            for j in files:
                list_category.setdefault(i,[]).append(j)
        else:
            continue
    return list_category
        
def normalize(name_dir):
    TRANS = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g',
         1043: 'G', 1076: 'd', 1044: 'D', 1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E',
         1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I', 1081: 'j',
         1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M',
         1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r',
         1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 1091: 'u', 1059: 'U',
         1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS',
         1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH',
         1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '', 1101: 'e',
         1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'u', 1071: 'U',
         1108: 'ja', 1028: 'JA', 1110: 'je', 1030: 'JE', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'}
    
    expansion = '.'+os.path.splitext(name_dir)[1][1:].strip()
    verif_name = name_dir.translate(TRANS).replace(expansion,'')
    
    for i in verif_name:
        if not i.isdigit() and not i.isalpha():
            verif_name = verif_name.replace(i,'_')
            
    return(verif_name+expansion)

    

def check_expansion(parent_dir,files_expansion,path_dir_rec):
    files = os.listdir(path_dir_rec)
    
    for i in files:

        if (os.path.isdir(os.path.join(path_dir_rec,i)) and i!='images'
            and i!='video' and i!='documents'
            and i!='music' and i!='archives'):
            if not os.listdir(os.path.join(path_dir_rec,i)):
                os.rmdir(os.path.join(path_dir_rec,i))
            else:
                check_expansion(parent_dir, files_expansion,
                                os.path.join(path_dir_rec,i))
        
        elif i.endswith(files_expansion['imag']):       #картинки
            sort_file(parent_dir,os.path.join(path_dir_rec,i), i,'images')
                
        elif i.endswith(files_expansion['video']):     #відео
            sort_file(parent_dir,os.path.join(path_dir_rec,i), i,'video')
                
        elif i.endswith(files_expansion['document']) :  #доки
            sort_file(parent_dir,os.path.join(path_dir_rec,i), i,'documents')
                
        elif i.endswith(files_expansion['music']):     #музыка
            sort_file(parent_dir,os.path.join(path_dir_rec,i), i,'music')
                
        elif i.endswith(files_expansion['achive']):    #архивы
            sort_file(parent_dir,os.path.join(path_dir_rec,i), i,'archives')

        elif os.path.isfile(os.path.join(path_dir_rec,i)):
            noname_expansion.add(os.path.splitext(i)[1][1:].strip())
        
    
def print_result():
    check_expansion(args.path,files_expansion,args.path)
    print('\n*************************************************************\n\n')
    print('*** Список файлов в каждой категории (музыка, видео, фото и пр.):\n')
    print(list_category(args.path,'documents','images','music','video','archives'))
    if len(files_expansion_exist)==0:
        print("\n*** В целевой папке НЕТ известных расширений\n")
    else:
        print('''\n*** Перечень всех известных скрипту расширений, которые
          встречаются в целевой папке:\n''')
        print(files_expansion_exist)

    if len(noname_expansion)==0:
        print("\n*** В целевой папке НЕТ неизвестных расширений\n")
    else:
        print('''\n*** Перечень всех расширений, которые скрипту неизвестны:\n''')
        print(noname_expansion)
                  
