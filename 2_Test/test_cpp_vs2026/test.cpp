#include <iostream>
using namespace std;

// 全局变量声明
int g = 99;

// 函数声明
int func();

int main()
{
    // 局部变量声明
    int g = 10;
    cout << g << endl;
    int kk = func();
    //cout << kk;


    auto a = 0;

	cout << a << endl;

    return 0;
}

// 函数定义
int func()
{
    return g;
}