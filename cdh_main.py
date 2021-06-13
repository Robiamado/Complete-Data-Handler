class cdh():
    def __init__(self, arg = None, *argv):
        if arg == None:
            self.items = []
            len_arg = 0
        elif type(arg) in (tuple, list):
            len_arg = 1
            if len(arg) == 2:          
                self.items = [(0, str(arg[0]), arg[1])]
            else:
                self.items = [(0, '0', arg)]
        elif type(arg) is dict:
            len_arg = len(arg)
            self.items = [(0, str(tuple(arg.keys())[0]), tuple(arg.values())[0])]
            j = 1
            while j < len(arg):
                self.items.append((j, str(tuple(arg.keys())[j]), tuple(arg.values())[j]))
                j += 1
        elif type(arg) is cdh:
            len_arg = len(arg)
            self.items = [(0, arg.items[0][1], arg.items[0][2])]
            j = 1
            while j < len(arg):
                self.items.append((j, arg.items[j][1], arg.items[j][2]))
                j += 1
        else:
            len_arg = 1
            self.items = [(0, '0', arg)]

        if len(argv) != 0:
            i = 0
            while i < len(argv):
                if type(argv[i]) in (tuple, list):
                    if len(argv[i]) == 2:
                        self.items.append((len_arg+i, str(argv[i][0]), argv[i][1]))
                    else:
                        self.items.append((len_arg+i, str(len_arg+i), argv[i]))
                elif type(argv[i]) is dict:
                    j = 0
                    while j < len(argv[i]):
                        self.items.append((len_arg+i, str(tuple(argv[i].keys())[j]), tuple(argv[i].values())[j]))
                        j += 1
                elif type(argv[i]) is cdh:
                    j = 0
                    while j < len(argv[i]):
                        self.items.append((len_arg+i, argv[i].items[j][1], argv[i].items[j][2]))
                        j += 1
                else:
                    self.items.append((len_arg+i, str(len_arg+i), argv[i]))
                i += 1

    def __str__(self):
        return_str = "{"
        for each in self.items:
            return_str = return_str + "(" + str(each[0]) + ") " + str(each[1]) + ": " + str(each[2]) + ", "
        return_str = return_str.strip(", ") + "}"
        return return_str

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        len_self = len(self)
        if type(index) is int:
            if index < len_self and index >= -len_self:
                return {self.items[index][1]: self.items[index][2]}
            else:
                print('Index out of range.')
                exit(0)
        elif type(index) is slice:
            start = index.start
            end = index.stop
            steps = index.step
            if start == None:
                start = 0
            if end == None:
                end = len_self-1
            if steps == None:
                steps = 1
            if start >= 0 and end >= start and end < len(self.items) and steps > 0 and steps < len_self:
                return_dict = dict()
                while start <= end:
                    return_dict.update({self.items[start][1]: self.items[start][2]})
                    start += steps
                return return_dict
            else:
                print('Index out of range.')
                exit(0)
        elif type(index) is str:
            i = 0
            return_value = []
            while i < len_self:
                if index == self.items[i][1]:
                    return_value.append(self.items[i][2])
                i += 1
            if len(return_value) == 1:
                return return_value[0]
            else:
                return return_value
        else:
            print('Invalid index.')
            exit(0)
    
    def __setitem__(self, index, value):
        len_self = len(self)
        if type(index) is int:
            if index < len_self and index >= -len_self:
                if index < 0:
                    index += len_self
                if type(value) is dict and len(value) == 1:
                    self.items[index] = (index, tuple(value.keys())[0], tuple(value.values())[0])
                else:
                    self.items[index] = (index, str(index), value)
            else:
                print('Index out of range.')
                exit(0)
        elif type(index) is slice:
            start = index.start
            end = index.stop
            steps = index.step
            if start == None:
                start = 0
            if end == None:
                end = len_self-1
            if steps == None:
                steps = 1
            if type(value) in (tuple, list, dict, cdh) and start >= 0 and end >= start and end < len_self and steps > 0 and steps < len_self and len(value) == end-start+1:
                i = 0
                while start <= end:
                    if type(value) is dict:
                        self.items[start] = (start, tuple(value.keys())[i], tuple(value.values())[i])
                    elif type(value) is cdh:
                        self.items[start] = (start, value.items[i][1], value.items[i][2])
                    else:
                        self.items[start] = (start, tuple(self.keys())[start], value[i])
                    start += steps
                    i += 1
            else:
                print('Index out of range.')
                exit(0)
        elif type(index) is str:
            i = 0
            while i < len_self:
                if index == self.items[i][1]:
                    self.items[i] = (i, index, value)
                i += 1
        else:
            print('Invalid index.')
            exit(0)

    def __add__(self, other):
        return_cdh = cdh()
        if len(self) == len(other):
            for i in range(len(self)):
                try:
                    return_cdh.update((i, self.items[i][1], self.items[i][2] + other.items[i][2]))
                except:
                    print('Error at cdh sum at id', i)
                    exit(0)
        else:
            print('Error at sum, cdhs of different length.')
            exit(0)
        return return_cdh

    def __sub__(self, other):
        return_cdh = cdh()
        if len(self) == len(other):
            for i in range(len(self)):
                try:
                    return_cdh.update((i, self.items[i][1], self.items[i][2] - other.items[i][2]))
                except:
                    print('Error at cdh subtract at id', i)
                    exit(0)
        else:
            print('Error at subtraction, cdhs of different length.')
            exit(0)
        return return_cdh

    def __mul__(self, other):
        return_cdh = cdh()
        if len(self) == len(other):
            for i in range(len(self)):
                try:
                    return_cdh.update((i, self.items[i][1], self.items[i][2] * other.items[i][2]))
                except:
                    print('Error at cdh multiplicate at id', i)
                    exit(0)
        else:
            print('Error at multiplication, cdhs of different length.')
            exit(0)
        return return_cdh

    def __truediv__(self, other):
        return_cdh = cdh()
        if len(self) == len(other):
            for i in range(len(self)):
                try:
                    return_cdh.update((i, self.items[i][1], self.items[i][2] / other.items[i][2]))
                except:
                    print('Error at cdh division at id', i)
                    exit(0)
        else:
            print('Error at division, cdhs of different length.')
            exit(0)
        return return_cdh

    # updates a cdh by adding as elements arg and argv. if arg or argv are dicts or chs replace same key's values.
    def update(self, arg, *argv):
        if arg == None:
            temp = cdh(self)
            self = cdh(temp)
        elif type(arg) in (tuple, list):
            len_arg = 1
            self.items.append((len(self), str(len(self)), arg))
        elif type(arg) is dict:
            len_arg = len(arg)
            j = 0
            while j < len_arg:
                i = 0
                is_replaced = False
                while i < len(self):
                    if str(tuple(arg.keys())[j]) == self.items[i][1]:
                        self.items[i] = (i, str(tuple(arg.keys())[j]), tuple(arg.values())[j])
                        is_replaced = True
                    i += 1
                if is_replaced == False:
                    self.items.append((len(self), str(tuple(arg.keys())[j]), tuple(arg.values())[j]))
                j += 1
        elif type(arg) is cdh:
            len_arg = len(arg)
            j = 0
            while j < len_arg:
                i = 0
                is_replaced = False
                while i < len(self):
                    if arg.items[j][1] == self.items[i][1]:
                        self.items[i] = (i, arg.items[j][1], arg.items[j][2])
                        is_replaced = True
                    i += 1
                if is_replaced == False:
                    self.items.append((len(self), arg.items[j][1], arg.items[j][2]))
                j += 1
        else:
            len_arg = 1
            self.items.append((len(self), str(len(self)), arg))
        if len(argv) != 0:
            i = 0
            while i < len(argv):
                if type(argv[i]) in (tuple, list):
                    self.items.append((len(self), str(len(self)), argv[i]))
                elif type(argv[i]) is dict:
                    j = 0
                    while j < len(argv[i]):
                        k = 0
                        is_replaced = False
                        while k < len(self):
                            if str(tuple(argv[i].keys())[j]) == self.items[k][1]:
                                self.items[k] = (k, str(tuple(argv[i].keys())[j]), tuple(argv[i].values())[j])
                                is_replaced = True
                            k += 1
                        if is_replaced == False:
                            self.items.append((len(self), str(tuple(argv[i].keys())[j]), tuple(argv[i].values())[j]))
                        j += 1
                elif type(argv[i]) is cdh:
                    j = 0
                    while j < len(argv[i]):
                        k = 0
                        is_replaced = False
                        while k < len(self):
                            if argv[i].items[j][1] == self.items[k][1]:
                                self.items[k] = (k, argv[i].items[j][1], argv[i].items[j][2])
                                is_replaced = True
                            k += 1
                        if is_replaced == False:
                            self.items.append((len(self), argv[i].items[j][1], argv[i].items[j][2]))
                        j += 1
                else:
                    self.items.append((len(self), str(len(self)), argv[i]))
                i += 1

    # appends arg and argv as elements to a cdh. (can duplicate keys)
    def append(self, arg, *argv):
        if arg == None:
            pass
        elif type(arg) in (tuple, list):
            len_arg = 1
            self.items.append((len(self), str(len(self)), arg))
        elif type(arg) is dict:
            len_arg = len(arg)
            j = 0
            while j < len_arg:
                self.items.append((len(self), str(tuple(arg.keys())[j]), tuple(arg.values())[j]))
                j += 1
        elif type(arg) is cdh:
            len_arg = len(arg)
            j = 0
            while j < len_arg:
                self.items.append((len(self), arg.items[j][1], arg.items[j][2]))
                j += 1
        else:
            len_arg = 1
            self.items.append((len(self), str(len(self)), arg))
        if len(argv) != 0:
            i = 0
            while i < len(argv):
                if type(argv[i]) in (tuple, list):
                    self.items.append((len(self), str(len(self)), argv[i]))
                elif type(argv[i]) is dict:
                    j = 0
                    while j < len(argv[i]):
                        self.items.append((len(self), str(tuple(argv[i].keys())[j]), tuple(argv[i].values())[j]))
                        j += 1
                elif type(argv[i]) is cdh:
                    j = 0
                    while j < len(argv[i]):
                        self.items.append((len(self), argv[i].items[j][1], argv[i].items[j][2]))
                        j += 1
                else:
                    self.items.append((len(self), str(len(self)), argv[i]))
                i += 1

    # removes all elements from a cdh with index id, key or value.
    def pop(self, value, arg = None):
        init_len_self = len(self)
        if arg == 'id' or (type(value) == int and arg == None):
            try:
                value = int(value)
            except:
                print('Invalid id in pop method.')
                exit(0)
            k = 0
        elif arg == 'key' or (type(value) == str and arg == None):
            try:
                value = str(value)
            except:
                print('Invalid key in pop method.')
                exit(0)
            k = 1
        elif arg == 'val':
            k = 2
        else:
            print('Invalid argument, can intersect on \'key\' or \'val\' only.')
            exit(0)
        i = 0
        while i < len(self):
            if value == self.items[i][k]:
                self.items.pop(i)
                if i != len(self):
                    j = i
                    while j < len(self):
                        self.items[j] = (j, self.items[j][1], self.items[j][2])
                        j += 1
            i += 1
        if len(self) == init_len_self:
            print('Invalid value or key in pop method.')
            exit(0)

    # returns a cdh built with self and other elemenmt's. overlapping keys are not merged. (can duplicate keys)
    def join(self, other):
        return_ch = cdh(self)
        if type(other) is cdh:
            i = 0
            j = len(return_ch)
            while i < len(other):
                return_ch.items.append((j, other.items[i][1], other.items[i][2]))
                i += 1
                j += 1
        else:
            print('Invalid Type, can join only chs.')
            exit(0)
        return return_ch

    # returns a cdh built with self and other. overlapping keys are merged with other's value.
    def merge(self, other):
        return_ch = cdh(self)
        if type(other) is cdh:
            i = 0
            j = len(self)
            while i < len(other):
                k = 0
                while k < len(self):
                    if other.items[i][1] == return_ch.items[k][1]:
                        return_ch.items[k] = (k, other.items[i][1], other.items[i][2])
                        k = -1
                        break
                    k += 1
                if k != -1:
                    return_ch.items.append((j, other.items[i][1], other.items[i][2]))
                    j += 1
                i += 1
        else:
            print('Invalid Type, can merge only chs.')
            exit(0)
        return return_ch

    # returns a cdh built with elements of common keys or values (can duplicate keys)
    def common(self, other, arg = None):
        return_ch = cdh()
        if arg == 'key' or arg == None:
            k = 1
        elif arg == 'val':
            k = 2
        else:
            print('Invalid argument, can intersect on \'key\' or \'val\' only.')
        i = 0
        l = 0
        while i < len(self):
            j = 0
            while j < len(other):
                if self.items[i][k] == other.items[j][k]:
                    return_ch.items.append((l, self.items[i][1], self.items[i][2]))
                    l += 1
                j += 1
            i += 1
        return return_ch
