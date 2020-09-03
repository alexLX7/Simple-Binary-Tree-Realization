# Simple-Binary-Tree-Realization

# Technical Task (The original version is written in Russian)

Design a class to represent a data structure in
the form of ***a binary tree***. Develop a separate class for ***a height-balanced binary tree***.
Classes have to contain an implementation of methods to add/remove an item, to display the elements.

Demonstrate the work by using int/float/str types.

Design a manual input for the elements. Develop a random tree generator, including n = 10, 50, 100, 200, 400, where n is a number of nodes in the tree.
Be able to compute the average height of each tree. The numbers must be in the range from -99 to 99.

Find (insert or remove if necessary) items
in accordance with the following options for tasks, the 9th variant:
* Find the maximum element of a binary tree and the number of repetitions of the maximum element in the given tree.
* Display the numbers, the sum of digits (modulo) of which is > N, where N is a number that the user can set. Determine the level of these elements. 

***Develop a graphical user interface.***



# Техническое задание
Разработать класс для представления структуры данных в
виде ***бинарного дерева***. Разработать отдельный класс для ***сбалансированного по высоте бинарного дерева***.
Реализуемые классы в качестве обязательных методов
должны иметь функции удаления/добавления элемента, вывод текущих элементов.

Продемонстрировать работу классов, используя типы int/float/str.

Предусмотреть ручной ввод элементов. Используя генератор случайных чисел, сформировать бинарное дерево, состоящее из n = 10, 50, 100, 200,
400 (n – количество вершин в дереве). Вычислить среднюю высоту АВЛ-дерева
для каждого случая. Причем числа должны лежать в диапазоне от -99 до 99. 

Произвести поиск (со вставкой или удалением при необходимости) элементов
в соответствии со следующими вариантами заданий, задания для 9 варианта:
* Найти максимальный элемент бинарного дерева и количество повторений максимального элемента в данном дереве.
* Отобразить числа, сумма цифр (по модулю) которых > N, где N - число, которое может задать пользователь. Определить уровень найденных элементов. 

***Разработать графический интерфейс пользователя.***


# Additional features
- An interface is written both in Russian and in English (switch the dictionaries in the source code)
- This is a crossplatform application based on PyQt5
- Ability to import/export trees as json file
- Ability to export trees as txt file
- Ability to export trees as png file


# Results
- All tasks are fully completed within the deadline (Dec of 2019)
- I'm sorry that I didn't initially add the README file


# How to run the code
The following steps assume using VS Code
```
python3 -m venv venv
pip install -r requirements.txt
run main.py
```