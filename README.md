# Complete Data Handler

*_This version is outdated please consider using version 2+ instead. This version is kept just for operators support management._*

## Introduction

Complete data handler is a Python class that merges numbers (int, float, complex), strings, lists and dictionaries. It can store and operate with those data types as a whole, using simple and intuitive rules listed below. CDH has been created to suppress the need of operating with dictionaries and lists as separate entities and to be able to call \_\_getitem\_\_ and \_\_setitem\_\_ operators (square brakets) with either an int, a slice or a string as argument. To do so, it has been introduced the concept of ID which is list indexing transposed to dictionaries. As matter of fact CDH structures store an ID, which is always a positive integer ; a Key, which is always a string, and a Value for each element. It has also been introduced a new set method, that allows to assign a number, string, list, dict or cdh to an existing cdh without aliasing. Recalling thet the latter is given by = operator. The new get method allows to retrive keys and values using IDs, pop method has been updated to handle IDs and a ro method is used to set a cdh to read only state. Union can be performed using update while intersection is done with common method, both save the result of the operation to the object calling it.

## Requirements

\- Python >=3.9

## Install

*- Using pip installer from “dist” folder:*

pip install cdh\_main-1.0.0-py2.py3-none-any.whl

*- Using source cdh\_main.py:*

copy cdh\_main.py in your root project folder

*-  Class import:*

from cdh\_main import cdh

## Methods

**\_\_init\_\_**

Cdh objects can be instantiated using as argument one or more number, string, list, dictionaryor cdh. In the case of numbers, strings and lists each element given as argument gets added to the object istance using as key the ID converted to string. Example:

a = cdh(1, 2) → a = {(0) 0 : 1, (1) 1 : 2}

b = cdh('a', 'b') → b = {(0) 0 : a, (1) 1 : b}

c = cdh([1,'a'], [2,['b','c']]) → c = {(0) 0 : [1,’a’], (1) 1 : [2, [‘b’,’c’]]}

While any dictionary or cdh given as argument will produce an object in which each element is an element of the firsts. 

Example:

d = cdh({'zero' : 0, 1 : 'one'}, {'three' : 3}) → d = {(0) zero: 0, (1) 1: one, (2) three: 3}

e = cdh(d, {'a': 'b'}) → d = {(0) zero: 0, (1) 1: one, (2) three: 3, (3) a: b}

**\_\_getitem\_\_   \_\_setitem\_\_**

Both used as square braket operator [ ] can be used in the most intuitive way, by calling it with an integer ID or a string Key. If used with ID argument it will return or modify the correspond dictionary while if used with Key argument it will return or modify the corresponding Value.

Example:

a = cdh(1,2)

print(a[0]) → {0 : 1}

print(a[‘0’]) → 1

a[0] = 0

a['1'] = 1

print(a) → {(0) 0: 0, (1) 1: 1}

Hence using square brakets to set a value with an integer ID one is able to change a dictionary element, thus both Key and the corresponding Value. To do so it is mandatory that the value is a dictionary or a cdh with exactly one element.

` `Example:

a = cdh({'a' : 0, 'b' : 1, 'c' : 2})

a[1] = {'d' : 3}

print(a) → {(0) a: 0, (1) d: 3, (2) c: 2}

If the value is a dict or a cdh with more than one element, given the lack of a 1-1 correspondence, only the value corresponding to the key linked to the ID will be set equal to the entire dict or cdh. The same procedure is applied to any other type which is resolved as value linked to the same key.

Example:

a = cdh({'a' : 0, 'b' : 1, 'c' : 2})

a[0] = {0: 1, 1: 2}

a[1] = 3

print(a) → {(0) a: {(0) 0: 1, (1) 1: 2}, (1) b: 3, (2) c: 2}

**\_\_add\_\_	\_\_sub\_\_	\_\_mult\_\_	\_\_truediv\_\_**

Any of these operators always have as left operand a cdh and as right operand  a number (int, float, complex), string, dict or cdh. If the left operand is number or a string they get treated as a one dimensional cdh with Key ‘0’ and value corresponding to the variable. The same concept applies for lists where each element is itself a Value of a cdh with Key corresponding to the index converted to string. In this very case it’s meanful to remark that the Key in a cdh is always a string, if not, it gets automatically converted on each operation. 

As everything gets converted to a cdh it is possible to consider only the case in which both left and right operands are cdhs. As such each element Value gets in relation (+,-,\*,/) using the ID. 

As explicative example, consider a cdh A of length n and one B of length m<n, the sum C=A+B will be of length n in the form:

C[i]=A[i]+B[i] with 0<i<m and C[j]=A[j] with m<j<n.

- Operators works as inteded on numeric values where sum, subtraction, multiplication and division are the corresponding arithmetic operations. 
- Strings sum to numbers by converting numbers to strings and concatenating them.
- Strings sum to strings with concatenation.
- Strings multiply with numbers by string repetition. Floats are converted to the smallest integer and complex are by taking the real part.
- Strings multiply by strings using concatenation on each character as if the strings were two summed vectors.
- Strings divide by numbers converting them to strings and using split.
- Strings divide by strings using split.

Perform Arithmetic operation first when possible:

Any string which is convertible to a numerical value gets automatically converted and treated as such whenever possible. 

(examples: ‘1’ → 1,	‘0.6’ →0.6,	‘1+1j’→ 1+1j)

Further examples are given in examples.py file.

**get**

Returns dictionaries, keys or values from a chd given a fixed ID.

Example

fruits = cdh({0 : 'apple', 1 : 'banana', 2 : 'pear'})

print(fruits.get(1)) → {'1': 'banana'}

print(fruits.get('key')) →  ['0', '1', '2']

print(fruits.get('val')) →  ['apple', 'banana', 'pear']

print(fruits.get('key', 1)) →  1

print(fruits.get('val', 1)) →  banana

**set**

Used to assign a variable without aliasing. Any existing cdh can be set equal to any number, string, list, dictionary or cdh.

Example

a = cdh(2)

b = cdh('a')

a.set(b)

print('a is b =', a is b,', a =', a, 'b =', b) → a is b = False , a = {(0) 0: a} b = {(0) 0: a}

a.set(2)

a = b

print('a is b =', a is b,', a =', a, 'b =', b) → a is b = True , a = {(0) 0: a} b = {(0) 0: a}

**pop**

Used to remove an element from a cdh. The element to be removed can be detected using a key or an ID.

Example

fruits = cdh({0 : 'apple', 1 : 'banana', 2 : 'pear'})

fruits.pop(1)

print(fruits) → {(0) '0' : 'apple', (1) '2' : 'pear'}

fruits.pop('0')

print(fruits) → {(0) '2' : 'pear'}

**update**

The update method is the usual dictionary method with the cdh conversion of each of the most commonly used types (numbers, strings, lists, dictionaries). It modify the calling object to a cdh which is the matematical join of the two cdhs. As usual if two elements have the same key, the calling object’s value gets replaced by the argument’s value while the key remains unchanged.

Example

a = cdh({'zero': 0, 'one': 1})

b = cdh({'zero': 'no zero', 'two': 1})

a.update(b)

print(a) → {(0) zero: no zero, (1) one: 1, (2) two: 1}

**common**

The common method is the mathematical intersection counterpart of the update method and acts as expected. It modify the calling object to a cdh built using common keys or common values of the two cdhs. By default the intersection is given on common keys but can be changed to common values with the instruction index = ‘val’ in the method’s call arguments. Of course the keys intersection instruction counterpart is index = ‘key’. Similar to the update method it modifies the calling object’s keys or values to the argument’s ones, on matching values or keys.

Example

a = cdh({'zero': 0, 'one': 1})

b = cdh({'zero': 'no zero', 'two': 1})

IF a.common(b) -> a = {(0) zero: no zero}

IF b.common(a) -> b = {(0) zero: 0}

IF a.common(b, 'key') -> a = {(0) zero: no zero}

IF a.common(b, 'val') -> a = {(0) two: 1}

**ro**

This method sets the cdh to read only state, making it impossible to modify (if not through direct access).

## Release Notes:

- 1.0.0 Initial Release

## Planned Features:

- \_\_setitem\_\_ slice indexing
- Numpy support
- Operators on nested dictionaries and cdhs
- Sorting algorithms
