# coding=utf-8


dic = {}


def read_count():
    with open("c:\\log.log") as file_obj:
        for line in file_obj:
            line = line.strip()
            if '{"articleid":' in line:
                id = line.split('articleid')[1].replace('":"','').replace('}', '').replace('"', '')
                if id.isdigit() :
                    id = int (id)
                    dic.setdefault(id, 0)
                    dic[id] += 1
    darr = sorted(dic.items(), key=lambda d: d[0])
    for d in darr:
        print d

if __name__ == '__main__':
    read_count()
