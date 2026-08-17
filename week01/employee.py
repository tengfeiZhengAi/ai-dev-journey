# ============================================================
#  Python 面向对象（class/self/继承/魔术方法）& C++ 对应写法
#  【Python】= Python 说明    【C++】= C++ 等价写法
# ============================================================

# ============================================================
# 1. 类定义 & 构造函数 & self
# ============================================================

# 【C++】class Employee { public: Employee(string n, int a) { ... } };
class Employee:
    # 【Python】类变量（所有实例共享）  【C++】static 成员
    company = "腾讯"

    # 【C++】Employee(string name, int age) { ... }
    def __init__(self, name, age):      # self 必须显式写，类似 C++ 的 this
        self.name = name                # 【Python】self.name  【C++】this->name
        self.age = age

    # 【C++】void introduce() { cout << this->name << endl; }
    def introduce(self):
        print(f"我是 {self.name}，{self.age} 岁，来自 {self.company}")

# 使用
# 【C++】Employee e("Alice", 25);
e = Employee("Alice", 25)               # 【Python】不需要 new 关键字
e.introduce()                            # 我是 Alice，25 岁，来自 腾讯
e.company = "字节跳动"
e.introduce()                            # 我是 Alice，25 岁，来自 字节跳动
print(Employee.company)                  #腾讯

# ============================================================
# 2. self 详解：Python 最反直觉的地方
# ============================================================

class Demo:
    def __init__(self, x):
        self.x = x                       # self.x = 实例属性，x = 参数

    def show(self):
        print(self.x)                    # 方法内访问属性必须加 self.

# 【Python】self 不是关键字，只是约定俗成的名字
class Demo2:
    def __init__(THIS, x):               # 可以叫 THIS，但没人这么干
        THIS.x = x

    def show(me):                        # 可以叫 me，但没人这么干
        print(me.x)

d = Demo2(10)
d.show()                                 # 10，但永远别这么写，用 self

d = Demo(100)
d.show()                                 # 100

# ============================================================
# 3. 访问控制：约定俗成，没有真正的 private
# ============================================================

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner               # 【Python】公开属性  【C++】public
        self._balance = balance          # 【Python】_前缀 = 约定私有  【C++】protected
        self.__pin = "1234"              # 【Python】__前缀 = 名称改写  【C++】private

    # 【Python】_ 前缀方法：约定"别在外面调"  【C++】protected
    def _update_balance(self, amount):
        self._balance += amount

    # 【Python】__ 前缀：名称被改写为 _BankAccount__pin，仍可访问但不该
    def check_pin(self, pin):
        return self.__pin == pin

acc = BankAccount("Alice", 1000)
print(acc.owner)                         # Alice ✅ 公开
print(acc._balance)                      # 1000 ⚠️ 能访问，但不该
# print(acc.__pin)                       # ❌ AttributeError（实际被改名为 _BankAccount__pin）
print(acc._BankAccount__pin)             # 1234 ⚠️ 强行绕过，但永远别这么干


# ============================================================
# 4. @property：优雅的属性访问控制
# ============================================================

class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    # 【Python】@property 把方法变成属性  【C++】getter
    @property
    def age(self):
        return self._age

    # 【Python】@xxx.setter 设置时校验  【C++】setter
    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("年龄不能为负数")
        self._age = value

    # 【Python】只读属性（没有 setter）  【C++】const 成员函数
    @property
    def name(self):
        return self._name

p = Person("Bob", 30)
print(p.age)                             # 30 — 像访问属性一样调用方法
p.age = 31                               # 触发 setter 校验
# p.name = "Tom"                         # ❌ AttributeError，没有 setter


# ============================================================
# 5. 继承 & super()
# ============================================================

# 【C++】class Developer : public Employee { ... };
class Developer(Employee):               # 【Python】父类写括号里  【C++】: public 父类
    def __init__(self, name, age, language):
        # 【C++】Employee(name, age);  在初始化列表里
        super().__init__(name, age)      # 【Python】super() 调用父类构造
        self.language = language

    # 重写父类方法
    def introduce(self):
        super().introduce()              # 先调父类方法
        print(f"我擅长 {self.language}")

dev = Developer("Charlie", 28, "Python")
dev.introduce()
# 我是 Charlie，28 岁，来自 腾讯
# 我擅长 Python


# ============================================================
# 6. 多继承（C++ 支持，Python 也支持）
# ============================================================

class Flyable:
    def fly(self):
        print("我真的会飞")

class Swimmable:
    def fly(self):
        print("我会飞")
    def swim(self):
        print("我会游泳")

class Duck(Flyable, Swimmable):          # 多继承，逗号分隔
    pass

duck = Duck()
duck.fly()                               # 我真的会飞，按MRO顺序
duck.swim()                              # 我会游泳


# ============================================================
# 7. 魔术方法（__xxx__）：让类像内置类型一样工作
# ============================================================

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 【C++】重载 << 运算符：friend ostream& operator<<(ostream&, const Vector&);
    def __str__(self):                   # str() 或 print() 时调用
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):                  # 调试输出，交互式环境显示
        return f"Vector({self.x}, {self.y})"

    # 【C++】Vector operator+(const Vector& other) { ... }
    def __add__(self, other):            # + 运算符
        return Vector(self.x + other.x, self.y + other.y)

    # 【C++】bool operator==(const Vector& other) { ... }
    def __eq__(self, other):             # == 运算符
        return self.x == other.x and self.y == other.y

    # 【C++】size_t operator()(size_t i) { ... }
    def __len__(self):                   # len() 时调用
        return 2

    # 【C++】v[i] 重载 []
    def __getitem__(self, index):        # 索引访问 v[0]
        return self.x if index == 0 else self.y

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1)                                # Vector(1, 2)  调用 __str__
print(v1 + v2)                           # Vector(4, 6)  调用 __add__
print(v1 == v2)                          # False         调用 __eq__
print(len(v1))                           # 2             调用 __len__
print(v1[0], v1[1])                      # 1 2           调用 __getitem__


# ============================================================
# 8. 常用魔术方法速查
# ============================================================

class DemoMagic:
    def __init__(self):                  # 构造     【C++】构造函数
        print("__init__: 对象创建时调用")

    def __del__(self):                   # 析构     【C++】~析构函数（Python 很少用）
        print("__del__: 对象销毁时调用")

    def __str__(self):                   # 打印     【C++】operator<<
        return "DemoMagic 实例"

    def __call__(self, x):               # 像函数一样调用  【C++】operator()
        print(f"__call__: 被当作函数调用，参数={x}")

    def __enter__(self):                 # with 进入  【C++】无直接对应
        print("__enter__: with 语句进入")
        return self

    def __exit__(self, *args):           # with 退出  【C++】析构函数
        print("__exit__: with 语句退出")

dm = DemoMagic()
dm(42)                                   # 调用 __call__
# __del__ 在程序结束或 del dm 时触发