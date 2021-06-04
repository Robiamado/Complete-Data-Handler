import time
from cdh_main import *

def main():
    section_divisor = '='*50

    a = cdh(2)
    b = cdh('a')
    c = cdh ([0,1])
    d = cdh([[0,1],[0,1]])
    e = cdh({'e' : 'e'})
    f = cdh(0, 1)
    g = cdh(0, [1,2], 'a', ['b', ['c','d']], {'g' : 'g'})
    print('a =', a,'\nb =', b,'\nc =', c,'\nd =', d, '\ne =', e, '\nf =', f, '\ng =', g)

    print('\n')
    # Operators
    print('a+1 =', a+1)
    print('a+\'a\' =', a+'a')
    print('a+[0,1] =', a+[0,1])
    print('a+{0 : 1} =', a+{0 : 1})
    print('a+{\'a\' : \'b\'} =', a+{'a' : 'b'})
    print('a+b =', a+b)
    print('b+a =', b+a)

    print('a-1 =', a-1)
    print('a-\'a\' =', a-'a')
    print('a-[0,1] =', a-[0,1])
    print('a-{0 : 1} =', a-{0 : 1})
    print('a-{\'a\' : \'b\'} =', a-{'a' : 'b'})
    print('a-b =', a-b)
    print('b-a =', b-a)

    print('a*1 =', a*1)
    print('a*\'a\' =', a*'a')
    print('a*[0,1] =', a*[0,1])
    print('a*{0 : 1} =', a*{0 : 1})
    print('a*{\'a\' : \'b\'} =', a*{'a' : 'b'})
    print('a*b =', a*b)
    print('b*a =', b*a)
    # Aliasing
    a.set(b)
    print('a.set(b) -> a is b =', a is b,', a =', a, 'b =', b)
    a = b
    print('a = b -> a is b =', a is b,', a =', a, 'b =', b)
    
    print('\n', section_divisor)

    fruits = cdh({0 : 'apple', 1 : 'banana', 2 : 'pear'})
    print('fruits =', fruits)

    print('\n')
    # Operators
    print('fruits+{1 : \'app\', 0 : \'nana\'} =', fruits+{1 : 'app', 0 : 'nana'})
    print('fruits-{1 : \'app\', 0 : \'nana\'} =', fruits-{1 : 'app', 0 : 'nana'})
    print('fruits*{1 : \'app\', 0 : \'nana\'} =', fruits*{1 : 'app', 0 : 'nana'})
    print('fruits/{1 : \'app\', 0 : \'nana\'} =', fruits/{1 : 'app', 0 : 'nana'})
    # __getitem__
    print('fruits[0] =', fruits[0])
    print('fruits[1:3] =', fruits[1:3])
    print('fruits[-1] =', fruits[-1])
    print('fruits to dict =', fruits[:])
    # get
    print('fruits.get(1) =', fruits.get(id = 1))
    print('fruits.get(\'key\') =', fruits.get(index = 'key'))
    print('fruits.get(\'val\') =', fruits.get(index = 'val'))
    print('fruits.get(\'key\', 1) =', fruits.get('key', 1))
    print('fruits.get(\'val\', 1) =', fruits.get('val', 1))
    # __setitem__
    fruits['1'] = 'cherry'
    print('fruits[\'1\'] = \'cherry\' -> fruits =', fruits)
    fruits[0] = 'orange'
    print('fruits[0] = \'orange\' -> fruits =', fruits)
    # cycles
    for number,name in fruits.items():
        print(number, 'is a', name)
    for i in fruits.id:
        print('id =', i, 'key =', fruits.get('key', i), 'name =', fruits.get('val', i))

    print('\n', section_divisor)

    vegetables = cdh({'orange' : 'carrot', 'red' : 'raddish', 'yellow' : 'corn'})
    print('vegetables =', vegetables)

    print('\n')
    # set, pop, clear
    vegetables.set(fruits)
    print('vegetables.set(fruits -> vegetables =', vegetables)
    vegetables.pop('1')
    print('vegetables.pop(\'1\') -> vegetables =', vegetables)
    vegetables.pop(0)
    print('vegetables.pop(0) -> vegetables =', vegetables)
    vegetables.clear()
    print('vegetables.clear() -> vegetables =', vegetables)
    vegetables.set({'orange' : 'carrot', 'red' : 'raddish', 'yellow' : 'corn'})
    print('vegetables.set({\'orange\' : \'carrot\', \'red\' : \'raddish\', \'yellow\' : \'corn\'}) \n -> vegetables =', vegetables)
    # cycles
    for i in vegetables.id:
        print(i, ')', vegetables.get('val', i), 'is', vegetables.get('key', i))
    # common
    fruits[1] = 'tomato'
    vegetables[1] = 'tomato'
    print('fruits[1] = \'tomato\', vegetables[1] = \'tomato\' ->')
    print('fruits =', fruits, '\nvegetables =', vegetables)
    fruits.common(vegetables, 'val')
    print('fruits.common(vegetables, \'val\') -> fruits =', fruits)
   
    print('\n', section_divisor)

    a = cdh({'zero': 0, 'one': 1})
    b = cdh({'zero': 'no zero', 'two': 1})
    c.set(a)
    d.set(b)
    print('a =', a)
    print('b =', b)
    # update
    print('\n')
    a.update(b)
    print('a.update(b) -> a =', a)

    print('\n')
    
    a.set(c)
    b.set(d)
    print('a =', a)
    print('b =', b)
    # common
    a.common(b)
    print('IF a.common(b) -> a =', a)

    a.set(c)
    b.common(a)
    print('IF b.common(a) -> b =', b)

    b.set(d)
    a.common(b, 'key')
    print('IF a.common(b, \'key\') -> a =', a)

    a.set(c)
    a.common(b, 'val')
    print('IF a.common(b, \'val\') -> a =', a)
    
    

start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))