#include <iostream>
using namespace std;


typedef int* pint;
#define PINT int *

int i1 = 1, i2 = 2;

const pint p1 = &i1;    //p不可更改，p指向的内容可以更改，相当于 int * const p;
const PINT p2 = &i2;    //p可以更改，p指向的内容不能更改，相当于 const int *p；或 int const *p；

pint s1, s2;    //s1和s2都是int型指针
PINT s3, s4;    //相当于int * s3，s4；只有一个是指针。

void TestPointer()
{
    cout << "p1:" << p1 << "  *p1:" << *p1 << endl;
    //p1 = &i2; //error C3892: 'p1' : you cannot assign to a variable that is const
    *p1 = 5;
    cout << "p1:" << p1 << "  *p1:" << *p1 << endl;

    cout << "p2:" << p2 << "  *p2:" << *p2 << endl;
    //*p2 = 10; //error C3892: 'p2' : you cannot assign to a variable that is const
    p2 = &i1;
    cout << "p2:" << p2 << "  *p2:" << *p2 << endl;
}

int main()
{
	TestPointer();
    return 0;
}