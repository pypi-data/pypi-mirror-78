import json
import sys
import yaml
from getopt import GetoptError, getopt

class YJ:
    def __init__(self, arr):
        self.flatten_arr = {}
        self.flatten(arr)

    def flatten(self, arr, pre=""):
        for i in arr:
            if type(arr[i]) is dict:
                pf = i
                if pre != "":
                    pf = pre + "." + i
                self.flatten(arr[i], pf)
            else:
                if pre != "":
                    self.flatten_arr[pre + "." + i] = arr[i]
                else:
                    self.flatten_arr[i] = arr[i]
    
    def get_flatten_array(self):
        return self.flatten_arr

def usage():
    usage = """
        -h, --help                 help for yj
        -I, --indent int           sets indent level for output (default 2)
        -P, --prettyPrint          pretty print
        -f, --filename             filename that's outputted as json. By default it prints 
        a json document in one line, use the prettyPrint flag to print a formatted doc.
    """
    print(usage)


def main():
    argv = sys.argv[1:]

    indent = 2
    prettyPrint = False
    name = ""
    try:
        opts, _ = getopt(
            argv, "hI:Pf:", ["help", "indent=", "prettyPrint", "filename="])
    except GetoptError as err:
        usage()
        print(err)
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-I", "--indent"):
            indent = int(arg)
        elif opt in ("-P", "--prettyPrint"):
            prettyPrint = True
        elif opt in ("-f", "--filename"):
            name = arg
        else:
            usage()
            sys.exit(2)
    
    if name == "":
        print('Error: Please enter the filename to be converted')
        usage()
        sys.exit(2)

    with open(name) as file:
        yaml_list = yaml.load(file, Loader=yaml.FullLoader)
    
    YJObj = YJ(yaml_list)
    final_list = YJObj.get_flatten_array()
    if prettyPrint:
        print(json.dumps(final_list, indent=indent, sort_keys=False))
    else:
        print(final_list)

if __name__ == '__main__':
    main()