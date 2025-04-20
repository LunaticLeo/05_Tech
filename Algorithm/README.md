**<center>Algorithm Study Note</center>**  
Created by Yufu Liao  
Studying from Leetcode

Solved Leetcode with Tag

- 27 Remove Element. easy. one pointer
- 283 Move Zeroes. easy. two pointer
- 485 Max Consecutive Ones. easy.
- 705 Design HashSet. easy. binary search tree
- 217 Contains Duplicate. easy.
- 389 Find the Difference. easy. Ascii
- 215 Kth Largest Element in an Array. easy. quickselect
- 692 Top K Frequent Words. easy. heap
- 203 Remove Linked List Elements. easy.
- 206 Reverse Linked List. easy.
- 933 Number of Recent Calls. easy.
- 20 Valid Parentheses. easy.
- 496 Next Greater Element I. easy.
- 144 Binary Traversal. easy.
- 141 Linked List Cycle. easy. set, two pointers
- 1011 Capacity To Ship Packages Within D Days. binary search
- 11 Container With Most Water. two pointer
- 33 Search in Rotated Sorted Array. binary search

AI prompt

```
Please list `xxxxx` constructors and main functions in a table. Give me markdown code of table. Table should be three columns "full " "example" "description". For all functions, please provide functions information include Access Modifier, parameters, return type. And if function has multiple version, if parameter can conclude as T/E, please use T/E, or if function has different parameters, please list all. Template example are below.

# ArrayList

`public class ArrayList<E> extends AbstractList<E> implements List<E>, RandomAccess, Cloneable, Serializable`
`import java.util.ArrayList;`
A dynamic, resizable array-based list, fast for random access but slower for insertions/deletions

| Function                                         | Example                                                                                                      | Description                                                                                                                                                                                                                        |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Constructor**                                  |                                                                                                              |                                                                                                                                                                                                                                    |
| `ArrayList()`                                    | `ArrayList<String> al = new ArrayList<>();`                                                                  | Creates an empty `ArrayList` with an initial capacity of 10.                                                                                                                                                                        |
| | `ArrayList al = new ArrayList();` <br> `al.add("Hello");` <br> `(String) arrlist.get(0); // need to convert string` | Allowed, equals `ArrayList<Object>` |
| `ArrayList(int initialCapacity)`                 | `ArrayList<String> al = new ArrayList<>(20);`                                                                | Creates an empty `ArrayList` with a specified initial capacity.                                                                                                                                                                    |
| `ArrayList(Collection<? extends E> c)`            | `ArrayList<String> al = new ArrayList<>(otherList);`                                                          | Creates a new `ArrayList` containing the elements of the specified collection.                                                                                                                                                      |
| **Basic Functions**                              |                                                                                                              |                                                                                                                                                                                                                                    |
| `int size()`                                     | `al.size(); // 3`                                                                                            | Returns the number of elements in the `ArrayList`.                                                                                                                                                                                 |
| `boolean isEmpty()`                              | `al.isEmpty(); // false`                                                                                     | Checks if the `ArrayList` is empty (i.e., it contains no elements).                                                                                                                                                               |
| **Access & Change**|||
| `E get(int index)`                               | `al.get(0); // "abc"`                                                                                         | Returns the element at the specified position in the `ArrayList`.                                                                                                                                                                 |
| `E set(int index, E element)`                    | `al.set(0, "newElement");`                                                                                    | Replaces the element at the specified position in the `ArrayList` with the specified element.                                                                                                                                      |
|**Add**|||
| `boolean add(E e)`                               | `al.add("abc");`                                                                                             | Adds the specified element to the end of the `ArrayList`.                                                                                                                                                                         |
| `void add(int index, E element)`                  | `al.add(1, "abc");`                                                                                          | Inserts the specified element at the specified position in the `ArrayList`.                                                                                                                                                       |
| `boolean addAll(Collection<? extends E> c)`      | `al.addAll(otherList); // true`                                                                               | Appends all of the elements from the specified collection to the `ArrayList`.                                                                                                                                                      |
| `boolean addAll(int index, Collection<? extends E> c)` | `al.addAll(2, otherList); // true`                                                                             | Inserts all the elements from the specified collection into the `ArrayList` at the specified position.                                                                                                                             |
|**Remove**|||
| `E remove(int index)`                            | `al.remove(1); // "abc"`                                                                                     | Removes the element at the specified position in the `ArrayList` and returns it.                                                                                                                                                   |
| `boolean remove(Object o)`                       | `al.remove("abc"); // true`                                                                                  | Removes the first occurrence of the specified object from the `ArrayList`.                                                                                                                                                       |
| `boolean removeAll(Collection<?> c)`             | `al.removeAll(otherList); // true`                                                                            | Removes from the `ArrayList` all of its elements that are contained in the specified collection.                                                                                                                                  |
| `void clear()`                                   | `al.clear();`                                                                                                | Removes all of the elements from the `ArrayList`.                                                                                                                                                                                 |
|**Search**|||
| `int indexOf(Object o)`                          | `al.indexOf("abc"); // 0`                                                                                     | Returns the index of the first occurrence of the specified object in the `ArrayList`.                                                                                                                                              |
| `int lastIndexOf(Object o)`              | `al.lastIndexOf(10);`                 | Returns the index of the last occurrence of the element, or `-1` if not found. |
| `boolean contains(Object o)`                     | `al.contains("abc"); // true`                                                                                 | Checks if the `ArrayList` contains the specified object.                                                                                                                                                                          |
| `boolean containsAll(Collection<?> c)`           | `al.containsAll(otherList); // true`                                                                          | Checks if the `ArrayList` contains all of the elements of the specified collection.                                                                                                                                                 |
|**Others**|||
| `T[] toArray()`                             | `al.toArray(); // [abc, def]`                                                                                 | Converts the `ArrayList` to an array.                                                                                                                                                                                               |
| `String toString()`                              | `al.toString(); // "[abc, def]"`                                                                             | Returns a string representation of the `ArrayList`.                                                                                                                                                                              |
| `void ensureCapacity(int minCapacity)`           | `al.ensureCapacity(100);`                                                                                    | Ensures that the `ArrayList` can hold at least the specified number of elements without needing to resize.                                                                                                                       |
| `List<E> subList(int fromIndex, int toIndex)` | `List<Integer> sub = al.subList(1, 3);`        | Returns a sublist view from `fromIndex` to `toIndex - 1`. |
| `void sort(Comparator<? super E> c)`     | `al.sort(Comparator.naturalOrder());`               | Sorts the list using a comparator. |


```
