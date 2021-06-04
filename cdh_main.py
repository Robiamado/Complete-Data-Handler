import math
import traceback

# returns error message and exit with corresponding code (Error codes.txt)
def error(code, cdh_name, *argv):
    error_starter = "Error :"
    report_site = "..."
    if code == 0:
        print(error_starter, "CDH internal code error - please report at", report_site)
    elif code == 1:
        print(error_starter, "Index out of range in", cdh_name)
    elif code == 2:
        print(error_starter, "Attempting to modify read only values in name", cdh_name)
    elif code == 3:
        print(error_starter, "Invalid argument in", argv[0], "operator at", cdh_name, argv[0], argv[1])
    elif code == 4:
        print(error_starter, "Range steps exceed range length in", cdh_name)
    elif code == 5:
        print(error_starter, "Invalid arguments in get method at", cdh_name)
    elif code == 6:
        print(error_starter, "Attempting to set invalid values in", cdh_name)
    elif code == 7:
        print(error_starter, "Attempting to update invalid values at", cdh_name)
    elif code == 8:
        print(error_starter, "No common", argv[0], "found in", cdh_name, "and", argv[1])
    elif code == 9:
        print(error_starter, "Invalid index in common operator. Only 'key' and 'val' are accepted inputs.")
    else:
        error(0, cdh_name)
    exit(0)
    
# converts strings to numbers, returns false if not possible
def str_to_num(str_to_conv, num_type = None):
    if num_type == None:
        try:
            str_to_conv = int(str_to_conv)
        except:
            try:
                str_to_conv = float(str_to_conv)
            except:
                try:
                    str_to_conv = complex(str_to_conv)
                except:
                    return False
    return str_to_conv
    
# multiply 2 strings as coloumn/row vector multiplication
def str_mul(first_str, second_str):
    return_str = ''
    j = 0
    while j < min(len(first_str), len(second_str)):
        return_str = return_str + first_str[j] + second_str[j]
        j = j + 1
    if j-1 == len(first_str):
        return_str = return_str + second_str[j:]
    elif j-1 == len(second_str):
        return_str = return_str + first_str[j:]
    return return_str
    
# dictionary with id as numerical index as lists and standard operators 
class cdh(dict):
    def __init__(self, data = None,  *argv, name = None, ro = False,):
        globals()["eq"] = infix(lambda l,m: l.set(m))
        if name == None:
            (filename,line_number,function_name,text) = traceback.extract_stack()[-2]
            self.name = text[:text.find("=")].strip()
        if data is None:
            data = {}
        else:
            keys_to_change = []
            if type(data) in [dict, cdh]:
                for key,value in data.items():
                        data.update({key : value})
                        if type(key) is not str:
                            keys_to_change.append(key)
                for key_to_change in keys_to_change:
                    data[str(key_to_change)] = data.pop(key_to_change)
            elif type(data) in [int, float, complex, str, list]:
                data = {'0' : data}
        if argv != ():
            keys_to_change = []
            i = 1
            for arg in argv:
                if type(arg) in [dict, cdh]:
                    for key,value in arg.items():
                        data.update({key : value})
                        if type(key) is not str:
                            keys_to_change.append(key)
                    for key_to_change in keys_to_change:
                        data[str(key_to_change)] = data.pop(key_to_change)
                elif type(arg) in [int, float, complex, str, list]:
                    data.update({str(i) : arg})
                i = i + 1
        super().__init__(data)
        self.read_only = ro
        self.id = []
        for i in range(len(self)):
            self.id.append(i)

    def __str__(self):
        return_str = "{"
        i = 0
        for key,value in self.items():
            return_str = return_str + "(" + str(self.id[i]) + ") " + str(key) + ": " + str(value) + ", "
            i = i + 1
        return_str = return_str.strip(", ") + "}"
        return return_str

    def __getitem__(self, index):
        return_val = None
        if type(index) is int:
            if index >= 0 and index < len(self.id):
                i = 0
                for key,value in self.items():
                    if i == index:
                        return_val = {key: value}
                    i += 1
            elif index < 0 and index >= -len(self.id):
                i = -len(self.id)
                for key,value in self.items():
                    if i == index:
                        return_val = {key: value}
                    i += 1
            else:
                error(1, self.name)
        elif type(index) is slice:
            return_val = dict()
            index_start = index.start
            index_stop = index.stop
            if index_start == None:
                index_start = 0
            if index_stop == None:
                index_stop = len(self)
            if index_start < 0:
                index_start = index_start + len(self) + 1
            if index_stop < 0:
                index_stop = index_stop + len(self) + 1
            if index_start <= len(self) and index_stop <= len(self):
                if index_stop > index_start:
                    slice_range = range(index_start, index_stop - 1)
                    i = index_start
                    max_slice_range = index_stop - 1
                elif index_start == index_stop:
                    slice_range = range(index_start, index_start)
                    i = index_start
                    max_slice_range = index_start
                elif index_start > index_stop:
                    slice_range = range(index_stop, index_start - 1)
                    i = index_stop
                    max_slice_range = index_start - 1
            else:
                error(1, self.name)
            j = 0
            if index.step != None:
                if index.step <= index.stop - index.start:
                    step_counter = index.step + i
                    for key,value in self.items():
                        if i <= max_slice_range and i == self.id[j]:
                            if i == step_counter:
                                return_val.update({key: value})
                                step_counter = step_counter + index.step
                            elif i == slice_range[0]:
                                return_val.update({key: value})
                            i += 1
                        j += 1
                else:
                    error(4, self.name)
            else:
                for key,value in self.items():
                    if i <= max_slice_range and i == self.id[j]:
                        return_val.update({key: value})
                        i += 1
                    j += 1
            if return_val == {}:
                return_val = None
        else:
            if type(index) is not str:
                index = str(index)

            return_val = None
            for key,value in self.items():
                if key == index:
                    return_val = value
                    break
        return return_val

    def __setitem__(self, index, set_value):
        if type(index) is int:
            def int_setter(set_key, set_value):
                if type(set_value) is dict:
                    set_value = cdh(set_value)
                if type(set_value) is cdh:
                    if len(set_value) == 1:
                        temp_cdh = cdh()
                        j = len(self.id) - 1
                        if index < 0:
                            set_index = index+len(self.id)
                        else:
                            set_index = index
                        while j >= set_index:
                            if j != set_index:
                                temp_cdh.update(self[j])
                            self.pop(j)
                            j -= 1
                        self.update({set_value.get('key', 0): set_value.get('val', 0)})
                        self.update(temp_cdh)
                    else:
                        self.update({set_key : set_value})
                else:
                    self.update({set_key : set_value})

            if index >= 0 and index < len(self.id):
                i = 0
                for key in self.keys():
                    if i == index:
                        int_setter(key, set_value)
                        break
                    i += 1
            elif index < 0 and index >= -len(self.id):
                i = -len(self.id)
                for key in self.keys():
                    if i == index:
                        int_setter(key, set_value)
                        break
                    i += 1
            else:
                error(1, self.name)
        else:
            if type(index) is not str:
                index = str(index)

            for key in self.keys():
                if key == index:
                    if set_value in [dict, cdh]:
                        print('debug')
                        self.update(set_value)
                    else:
                        self.update({key : set_value})
                    break

    def __add__(self, other):
        if type(other) in [int, float, complex, str, list, dict, cdh]:
            i = 0
            return_val = cdh()
            other_name = ''
            if type(other) in [int, float, complex, str]:
                other_name = [k for k,v in locals().items() if v == other][0]
                other = [other]
            elif type(other) is list:
                other_name = [k for k,v in locals().items() if v == other][0]
            elif type(other) is dict:
                other = cdh(other)
                other_name = other.name
            elif type(other) is cdh:
                other_name = other.name             
            while i < max(len(self), len(other)):
                if i < min(len(self), len(other)):
                    if type(other) is list:
                        other_i = other[i]
                    elif type(other) is cdh:
                        other_i = other.get("val", i)
                    if type(other_i) in [int, float, complex]:
                        if type(self.get("val", i)) in [int, float, complex]:
                            return_val.update({self.get("key", i) : self.get("val", i) + other_i})
                        elif type(self.get("val", i)) is str:
                            if str_to_num(self.get("val", i)):
                                return_val.update({self.get("key", i) : str_to_num(self.get("val", i)) + other})
                            else:
                                return_val.update({self.get("key", i) : self.get("val", i) + str(other_i)})
                        else:
                            error(3, self.name, "+", other_name)
                    elif type(other_i) is str:
                        if type(self.get("val", i)) in [int, float, complex]:
                            if str_to_num(other_i):
                                return_val.update({self.get("key", i) : self.get("val", i) + str_to_num(other_i)})
                            else:
                                return_val.update({self.get("key", i) : str(self.get("val", i)) + other_i})
                        elif type(self.get("val", i)) is str:
                            if str_to_num(self.get("val", i)) and str_to_num(other_i):
                                return_val.update({self.get("key", i) : str_to_num(self.get("val", i)) + str_to_num(other_i)})
                            else:
                                return_val.update({self.get("key", i) : self.get("val", i) + other_i})
                        else:
                            error(3, self.name, "+", other_name)
                else:
                    if len(self) > len(other):
                        return_val.update({self.get("key", i) : self.get("val", i)})
                    elif len(other) > len(self):
                        if type(other) is list:
                            other_i = other[i]
                        elif type(other) is cdh:
                            other_i = other.get("val", i)
                        return_val.update({i : other_i})
                i += 1
            return return_val
        else:
            error(3, self.name, "+", other_name)

    def __sub__(self, other):
        if type(other) in [int, float, complex, str, list, dict, cdh]:
            i = 0
            return_val = cdh()
            other_name = ''
            if type(other) in [int, float, complex, str]:
                other_name = [k for k,v in locals().items() if v == other][0]
                other = [other]
            elif type(other) is list:
                other_name = [k for k,v in locals().items() if v == other][0]
            elif type(other) is dict:
                other = cdh(other)
                other_name = other.name
            elif type(other) is cdh:
                other_name = other.name             
            while i < max(len(self), len(other)):
                if i < min(len(self), len(other)):
                    if type(other) is list:
                        other_i = other[i]
                    elif type(other) is cdh:
                        other_i = other.get("val", i)
                    if type(other_i) in [int, float, complex]:
                        if type(self.get("val", i)) in [int, float, complex]:
                            return_val.update({self.get("key", i) : self.get("val", i) - other_i})
                        elif type(self.get("val", i)) is str:
                            if str_to_num(self.get("val", i)):
                                return_val.update({self.get("key", i) : str_to_num(self.get("val", i)) - other})
                            else:
                                return_val.update({self.get("key", i) : self.get("val", i).strip(str(other_i))})
                        else:
                            error(3, self.name, "-", other_name)
                    elif type(other_i) is str:
                        if type(self.get("val", i)) in [int, float, complex]:
                            if str_to_num(other_i):
                                return_val.update({self.get("key", i) : self.get("val", i) - str_to_num(other_i)})
                            else:
                                return_val.update({self.get("key", i) : str(self.get("val", i)).strip(other_i)})
                        elif type(self.get("val", i)) is str:
                            if str_to_num(self.get("val", i)) and str_to_num(other_i):
                                return_val.update({self.get("key", i) : str_to_num(self.get("val", i)) - str_to_num(other_i)})
                            else:
                                return_val.update({self.get("key", i) : self.get("val", i).strip(other_i)})
                        else:
                            error(3, self.name, "-", other_name)
                else:
                    if len(self) > len(other):
                        return_val.update({self.get("key", i) : self.get("val", i)})
                    elif len(other) > len(self):
                        if type(other) is list:
                            other_i = other[i]
                        elif type(other) is cdh:
                            other_i = other.get("val", i)
                        return_val.update({i : other_i})
                i += 1
            return return_val
        else:
            error(3, self.name, "-", other_name)

    def __mul__(self, other):
        if type(other) in [int, float, complex, str, list, dict, cdh]:
            i = 0
            return_val = cdh()
            other_name = ''
            if type(other) in [int, float, complex, str]:
                other_name = [k for k,v in locals().items() if v == other][0]
                other = [other]
            elif type(other) is list:
                other_name = [k for k,v in locals().items() if v == other][0]
            elif type(other) is dict:
                other = cdh(other)
                other_name = other.name
            elif type(other) is cdh:
                other_name = other.name             
            while i < max(len(self), len(other)):
                if i < min(len(self), len(other)):
                    if type(other) is list:
                        other_i = other[i]
                    elif type(other) is cdh:
                        other_i = other.get("val", i)
                    if type(other_i) in [int, float, complex]:
                        if type(self.get("val", i)) in [int, float, complex]:
                            return_val.update({self.get("key", i) : self.get("val", i) * other_i})
                        elif type(self.get("val", i)) is str:
                            if str_to_num(self.get("val", i)):
                                return_val.update({self.get("key", i) : str_to_num(self.get("val", i)) * other})
                            else:
                                return_val.update({self.get("key", i) : str_mul(self.get("val", i), str(other_i))})
                        else:
                            error(3, self.name, "*", other_name)
                    elif type(other_i) is str:
                        if type(self.get("val", i)) in [int, float, complex]:
                            if str_to_num(other_i):
                                return_val.update({self.get("key", i) : self.get("val", i) * str_to_num(other_i)})
                            else:
                                return_val.update({self.get("key", i) : str_mul(str(self.get("val", i)), other_i)})
                        elif type(self.get("val", i)) is str:
                            if str_to_num(self.get("val", i)) and str_to_num(other_i):
                                return_val.update({self.get("key", i) : str_to_num(self.get("val", i)) * str_to_num(other_i)})
                            else:
                                return_val.update({self.get("key", i) : str_mul(self.get("val", i), other_i)})
                        else:
                            error(3, self.name, "*", other_name)
                else:
                    if len(self) > len(other):
                        return_val.update({self.get("key", i) : self.get("val", i)})
                    elif len(other) > len(self):
                        if type(other) is list:
                            other_i = other[i]
                        elif type(other) is cdh:
                            other_i = other.get("val", i)
                        return_val.update({i : other_i})
                i += 1
            return return_val
        else:
            error(3, self.name, "*", other_name)

    def __truediv__(self, other):
        if type(other) in [int, float, complex, str, list, dict, cdh]:
            i = 0
            return_val = cdh()
            other_name = ''
            if type(other) in [int, float, complex, str]:
                other_name = [k for k,v in locals().items() if v == other][0]
                other = [other]
            elif type(other) is list:
                other_name = [k for k,v in locals().items() if v == other][0]
            elif type(other) is dict:
                other = cdh(other)
                other_name = other.name
            elif type(other) is cdh:
                other_name = other.name             
            while i < max(len(self), len(other)):
                if i < min(len(self), len(other)):
                    if type(other) is list:
                        other_i = other[i]
                    elif type(other) is cdh:
                        other_i = other.get("val", i)
                    if type(other_i) in [int, float, complex]:
                        if type(self.get("val", i)) in [int, float, complex]:
                            return_val.update({self.get("key", i) : self.get("val", i) / other_i})
                        elif type(self.get("val", i)) is str:
                            if str_to_num(self.get("val", i)):
                                return_val.update({self.get("key", i) : str_to_num(self.get("val", i)) / other})
                            else:
                                return_val.update({self.get("key", i) : self.get("val", i).split(str(other_i))[0] + self.get("val", i).split(str(other_i))[1]})
                        else:
                            error(3, self.name, "/", other_name)
                    elif type(other_i) is str:
                        if type(self.get("val", i)) in [int, float, complex]:
                            if str_to_num(other_i):
                                return_val.update({self.get("key", i) : self.get("val", i) / str_to_num(other_i)})
                            else:
                                return_val.update({self.get("key", i) : str(self.get("val", i)).split(other_i)[0] + str(self.get("val", i)).split(other_i)[1]})
                        elif type(self.get("val", i)) is str:
                            if str_to_num(self.get("val", i)) and str_to_num(other_i):
                                return_val.update({self.get("key", i) : str_to_num(self.get("val", i)) / str_to_num(other_i)})
                            else:
                                return_val.update({self.get("key", i) : self.get("val", i).split(other_i)[0] + self.get("val", i).split(other_i)[1]})
                        else:
                            error(3, self.name, "/", other_name)
                else:
                    if len(self) > len(other):
                        return_val.update({self.get("key", i) : self.get("val", i)})
                    elif len(other) > len(self):
                        if type(other) is list:
                            other_i = other[i]
                        elif type(other) is cdh:
                            other_i = other.get("val", i)
                        return_val.update({i : other_i})
                i += 1
            return return_val
        else:
            error(3, self.name, "/", other_name)

    def get(self, index = None, id = None):
        if index == None:
            if id != None:
                if type(id) is int and id <= len(self.id) and id >= -len(self.id):
                    return {list(self[id].keys())[0] : list(self[id].values())[0]}
                else:
                    error(5, self.name)
            else:
                return self
        else:
            if id != None:
                if index == "val":
                    if type(id) is int and id < len(self.id) and id >= -len(self.id):
                        return list(self[id].values())[0]
                    else:
                        error(5, self.name)
                elif index == "key":
                    if type(id) is int and id < len(self.id) and id >= -len(self.id):
                        return list(self[id].keys())[0]
                    else:
                        error(5, self.name)
                else:
                    error(5, self.name)
            else:
                if index == "val":
                    return_val = []
                    for value in self.values():
                        return_val.append(value)
                    return return_val
                elif index == "key":
                    return_val = []
                    for key in self.keys():
                        return_val.append(key)
                    return return_val
                else:
                    error(5, self.name)
    
    def set(self, other):
        if type(other) is list:
            self.clear()
            self.id.clear()
            i = 0
            while i < len(other):
                self.update({str(len(self.id)) : other[i]})
                i = i + 1
        elif type(other) is dict:
            self.clear()
            self.id.clear()
            for key,value in other.items():
                self.update({key : value})
        elif type(other) is cdh:
            if self.read_only == False and other.read_only == False:
                self.clear()
                self.id.clear()
                for key,value in other.items():
                    self.update({key : value})
            else:
                if self.read_only == True:
                    error(2, self.name)
                elif other.read_only == True:
                    error(2, other.name)
                else:
                    error(2, self.name)
                    error(2, other.name)
        elif type(other) in [int, float, complex, str]:
            self.clear()
            self.id.clear()
            self.update({'0' : other})
        else:
            error(6, self.name)

    def update(self, value):
        if self.read_only == False:
            if type(value) in [int, float, complex, str]:
                super(cdh, self).update({str(len(self.id)) : value})
                self.id.append(len(self.id))
            elif type(value) is list:
                i = 0
                while i < len(value):
                    super(cdh, self).update({str(len(self.id)) : value[i]})
                    self.id.append(len(self.id))
                    i = i + 1
            elif type(value) in [dict, cdh]:
                for key in value.keys():
                    if key not in self.keys():
                        self.id.append(len(self.id))
                super(cdh, self).update(value)
            else:
                error(7, self.name)
        else:
            error(2, self.name)

    def pop(self, index):
        if type(index) is int:
            if index >= 0 and index < len(self.id):
                for each in self.id:
                    if index == each:
                        super(cdh, self).pop(self.get('key', each))
                        index = None
                        break
            elif index < 0 and index >= -len(self.id):
                for each in range(1, len(self.id)+1):
                    if index == -each:
                        super(cdh, self).pop(self.get('key', index))
                        index = None
                if index != None:
                    error(1, self.name)
            else:
                error(1, self.name)
        else:
            super(cdh, self).pop(index)

    def common(self, other, index = 'key'):
        if type(other) in [int, float, complex, str]:
            if index == 'key':
                if str(other) in self.keys():
                    self.clear()
                    self.id.clear()
                    self.update({str(other) : None})
                else:
                    error(8, self.name, index, other)
            elif index == 'val':
                if other in self.values():
                    self.clear()
                    self.id.clear()
                    self.update({'0' : other})
                else:
                    error(8, self.name, index, other)
            else:
                error(9, self.name)
        elif type(other) is list:
            temp = list()
            i = 0
            while i < len(other):
                if index == 'key':
                    if str(other[i]) in self.keys():
                        temp.update({str(other[i]) : None})
                elif index == 'val':
                    if other[i] in self.values():
                        temp.update({str(i) : other[i]})
                i += 1
            self.clear()
            self.id.clear()
            self.set(temp)
            del temp
            if len(self) == 0:
                error(8, self.name, index, other)
        elif type(other) in [dict, cdh]:
            if type(other) is dict:
                other = cdh(other)
            if self.read_only == False and other.read_only == False:
                temp = cdh()
                if index == 'key':
                    i = 0
                    for key,value in other.items():
                        if key in self.keys():
                            temp.update({key : value})
                        i += 1
                elif index == 'val':
                    i = 0
                    for key,value in other.items():
                        if value in self.values():
                            temp.update({key : value})
                        i += 1
                else:
                    error(9, self.name)
                self.clear()
                self.id.clear()
                self.set(temp)
                del temp
                if len(self) == 0:
                    error(8, self.name, index, other.name)
            else:
                if self.read_only == True:
                    error(2, self.name)
                elif other.read_only == True:
                    error(2, other.name)
                else:
                    error(2, self.name)
                    error(2, other.name)

        else:
            error(6, self.name)

    def ro(self):
        self.read_only = True
