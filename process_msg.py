import re


def main(text):
    print(text.split('COMP'))
    entries = text.split('COMP')[:-1] #discard last split, it's just a tail
    parsed_entries = []
    for entry in entries:
        lines = entry.split('\n')
        line_dict = {}
        for line in lines:
            print(line)
            if 'HSH' in line:
                a = re.search("[\d]+\.[\d]", line)
                if a == None:
                    print ("Erro! Nenhum HSH encontrado na seguinte mensagem:")
                    print (text)
                    exit()
                else:
                    a = a.group()
                    line_dict['HSH'] = a
            elif 'PREF' in line:
                a = re.search("[\d]+", line).group()
                line_dict['PREF'] = a
            elif 'PATR' in line:
                a = re.search("[\d]+", line).group()
                line_dict['PATR'] = a
            elif 'CMT' in line:
                a = re.search("[\d]+.*[\d]", line).group()
                a = a.replace('-', '')
                line_dict['CMT'] = a
            elif 'MOT' in line:
                a = re.search("[\d]+.*[\d]", line).group()
                a = a.replace('-', '')
                line_dict['MOT'] = a
        parsed_entries.append(line_dict)
    return parsed_entries




if __name__ == "__main__":
    msg = '\
    HSH 10.1 GAIBU\
    PREF: GT 18131\
    PATR: 730316\
    CMT: 126369-2 SD CLEDIVALDO\
    MOT: 126373-0 SD RAMON\
    FONE: 9.7319-8347\
    COMP: 02PM\
    \n\
    HSH 10.1 GAIBU\
    PREF: GT 18131\
    PATR: 730316\
    CMT: 126369-2 SD CLEDIVALDO\
    MOT: 126373-0 SD RAMON\
    FONE: 9.7319-8347\
    COMP: 02PM\
    '

    main(msg)