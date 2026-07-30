// ============ global.cpp ============
#include <iostream>

// 定义全局变量（这才是真正分配内存的地方）
int g_counter = 0;

void increment() {
    g_counter++;
}