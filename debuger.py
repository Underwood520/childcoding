# 创建实例
from langchain_core.messages import HumanMessage

from llms.kimi import Kimi

llm = Kimi()


instructions = """
查找输入代码中的bug
返回格式如下：
bug_id：序号
bug_row：行数
bug_info：信息
以JSON格式返回答案
注意，可能有多个bug
"""

# 参考：17个C++编程常见错误及其解决方案：https://cloud.tencent.com/developer/article/2414336
# 工具：在线多行文本连接成一行 https://www.lddgo.net/string/line-reduce


# # 1
# codes = "int* ptr = nullptr;\nstd::cout << *ptr;"
# prompt = (instructions+codes)
# output = llm.invoke([HumanMessage(content=prompt)])
# print(output)
# """
# bug序号：1
# bug所在行数：2
# bug信息：解引用空指针可能导致程序崩溃
# """


# 2
# codes = "std::mutex mtx;\nint shared_var = 0;\nvoid thread_func() {\nfor (int i = 0; i < 1000000; ++i) {\nstd::lock_guard<std::mutex> lock(mtx);\nshared_var++;\n}\n}"
# prompt = (instructions+codes)
# output = llm.invoke([HumanMessage(content=prompt)])
# print(output)
# """
# bug序号：1
# bug所在行数：5
# bug信息：在多线程环境下，对共享变量shared_var的递增操作没有进行原子操作，可能导致数据竞争和不一致的问题。
# 建议解决方案：使用原子操作来确保对共享变量的递增操作是原子的，例如使用std::atomic<int>代替int，或者使用其他同步机制（如互斥锁）来保护共享变量的访问。
# """


# 3
# codes = "std::mutex m1, m2;\nbool flag1 = false, flag2 = false;\nvoid func1() {\nstd::unique_lock<std::mutex> lck1(m1);\nstd::unique_lock<std::mutex> lck2(m2, std::defer_lock);\nwhile (!flag2) {\nlck2.lock();\n// ...\n}\n}\nvoid func2() {\nstd::unique_lock<std::mutex> lck2(m2);\nstd::unique_lock<std::mutex> lck1(m1, std::defer_lock);\nwhile (!flag1) {\nlck1.lock();\n// ...\n}\n}"
# prompt = (instructions+codes)
# output = llm.invoke([HumanMessage(content=prompt)])
# print(output)
# """
# bug序号：1
# bug所在行数：第5行
# bug信息：在func1()函数中，lck2.lock()可能永远不会被调用，因为flag2可能永远不会被设置为true。这将导致死锁。
#
# bug序号：2
# bug所在行数：第12行
# bug信息：在func2()函数中，lck1.lock()可能永远不会被调用，因为flag1可能永远不会被设置为true。这同样会导致死锁。
#
# 这两个bug都与死锁有关，因为两个函数都依赖于对方设置的标志（flag1和flag2）来解锁。如果这些标志没有被正确设置，那么两个函数将无法继续执行，从而导致死锁。为了避免这种情况，可以考虑使用条件变量或其他同步机制来确保在解锁之前，相应的标志已经被设置。
#
# """


# 4
# codes = 'char str[10];\nstrcpy(str, "This is a very long string.");'
# prompt = (instructions+codes)
# output = llm.invoke([HumanMessage(content=prompt)])
# print(output)
# """
# bug序号：1
# bug所在行数：2
# bug信息：目标字符串数组str的大小不足以容纳源字符串"This is a very long string."，这将导致缓冲区溢出。
# """


# 5
# codes = 'int* p = new int(5);\ndelete p;\n*p = 10;.");'
# prompt = (instructions+codes)
# output = llm.invoke([HumanMessage(content=prompt)])
# print(output)
# """
# bug序号：1
# bug所在行数：3
# bug信息：在delete p后，指针p不再指向有效的内存，尝试解引用p将导致未定义行为。
# """


# 6
# codes = 'void mayThrowException() {\nthrow std::runtime_error("An error occurred.");\n}\nint main() {\nmayThrowException();\nreturn 0;\n}'
# prompt = (instructions+codes)
# output = llm.invoke([HumanMessage(content=prompt)])
# print(output)
# """
# bug序号：1
# bug所在行数：3
# bug信息：函数`mayThrowException`抛出异常，但`main`函数没有捕获或处理这个异常，导致程序可能在运行时崩溃。
#
# 修复建议：在`main`函数中添加异常捕获和处理逻辑，例如：
#
# ```cpp
# int main() {
#     try {
#         mayThrowException();
#     } catch (const std::runtime_error& e) {
#         std::cerr << "Caught an exception: " << e.what() << std::endl;
#     }
#     return 0;
# }
# ```
# """


# 7
# codes = 'double a = 0.1;\ndouble b = 0.2;\nif (a + b == 0.3) {\n// ...\n}'
# prompt = (instructions+codes)
# output = llm.invoke([HumanMessage(content=prompt)])
# print(output)
# """
# bug序号：1
# bug所在行数：3
# bug信息：浮点数比较错误
#
# 解释：在代码中，第3行的if语句试图比较两个浮点数a + b和0.3是否相等。由于浮点数的表示和计算可能会有精度问题，直接使用"=="进行比较可能会导致错误的结果。建议使用一个小的误差范围来比较浮点数，例如：
#
# ```c
# if (fabs(a + b - 0.3) < 1e-9) {
#     // ...
# }
# ```
#
# 这里使用了fabs函数来计算两个数之间的绝对差值，如果差值小于1e-9（一个很小的数），则认为它们是相等的。这样可以避免由于浮点数精度问题导致的比较错误。
# """


# 8
# codes = 'unsigned int a = 0;\nunsigned int b = 1;\nstd::cout << a - b;'
# prompt = (instructions+codes)
# output = llm.invoke([HumanMessage(content=prompt)])
# print(output)
# """
# bug序号：1
# bug所在行数：3
# bug信息：输出语句缺少结束的分号。
# 此处Kimi判断错误，对无符号整数执行减法，当结果小于零时可能会导致意外的大数值。
# """


# 9
# codes = 'long long num1 = LLONG_MAX;\nint num2 = INT_MAX;\nlong long result = num1 + num2;'
# prompt = (instructions+codes)
# output = llm.invoke([HumanMessage(content=prompt)])
# print(output)
# """
# bug序号：1
# bug所在行数：3
# bug信息：整数溢出。`num1` 和 `num2` 都是它们类型的最大值，相加会导致溢出。
# """


# 10
# codes = 'std::ofstream file("output.txt");\nfile << "Some content";'
# prompt = (instructions+codes)
# output = llm.invoke([HumanMessage(content=prompt)])
# print(output)
# """
# bug序号：1
# bug所在行数：1
# bug信息：std::ofstream file("output.txt"); 没有检查文件是否成功打开。如果文件无法打开，后续的写入操作将失败。
#
# 修复建议：
# ```cpp
# #include <fstream>
# #include <iostream>
#
# int main() {
#     std::ofstream file("output.txt");
#     if (!file.is_open()) {
#         std::cerr << "无法打开文件" << std::endl;
#         return 1;
#     }
#     file << "Some content";
#     file.close();
#     return 0;
# }
# ```
# 这个修复建议添加了文件打开检查，并在无法打开文件时输出错误信息并返回非零值。
# """


# 11
# codes = 'unsigned int counter = 5;\nwhile (counter >= 0) {\n--counter;\n}'
# prompt = (instructions+codes)
# output = llm.invoke([HumanMessage(content=prompt)])
# print(output)
# """
# bug序号：1
# bug所在行数：1
# bug信息：变量 `counter` 的初始值设置为5，但循环条件是 `counter >= 0`，这意味着循环将执行5次，而不是无限次。这可能导致逻辑错误，因为循环可能在需要继续执行时停止。
#
# 修复建议：如果目的是创建一个无限循环，可以将循环条件更改为 `true` 或删除条件。如果需要根据 `counter` 的值执行特定次数的循环，请确保循环条件与预期的循环次数相匹配。
# """


# 12
codes = 'double d = 3.14;\nint i = d;\nif (d == 3) {\n...\n}'
prompt = (instructions+codes)
output = llm.invoke([HumanMessage(content=prompt)])
print(output)
"""
bug序号：1
bug所在行数：2
bug信息：类型转换错误，将double类型的变量d赋值给int类型的变量i，可能导致精度损失。

bug序号：2
bug所在行数：3
bug信息：条件判断错误，由于d是3.14，与3进行比较时永远为false，导致if语句内的代码不会被执行。
"""


# 13
# codes = 'for (std::vector<int>::iterator it = vec.begin(); it != vec.end(); ++it) {\nif (*it == target) {\nit = vec.erase(it);\n}\n}'
# prompt = (instructions+codes)
# output = llm.invoke([HumanMessage(content=prompt)])
# print(output)
# """
# bug序号：1
# bug所在行数：3
# bug信息：在删除元素后，未对迭代器进行递增操作，导致迭代器可能进入无限循环。
#
# 修复建议：
# 在删除元素后，应该对迭代器进行递增操作，以避免进入无限循环。可以使用以下代码修复此问题：
#
# ```cpp
# for (std::vector<int>::iterator it = vec.begin(); it != vec.end(); /* empty */) {
#     if (*it == target) {
#         it = vec.erase(it);
#     } else {
#         ++it;
#     }
# }
# ```
# """






