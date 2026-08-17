"""
通讯录列表（类版本 + 继承示例）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
继承链：
  ContactList                  ← 父类：核心增删查存
      ↑
  SearchableContactList        ← 子类：增加搜索功能
      ↑
  ColorContactList             ← 孙子类：增加彩色输出

每层继承只加新功能，不修改父类代码，这就是继承的核心价值。
"""
import json
import time


# ============================================================
# 第一层：ContactList（父类）—— 核心增删查存
# 【C++】class ContactList { ... };
# ============================================================
class ContactList:
    """通讯录基类：只有最基础的增删查存功能"""

    def __init__(self, filename="contact_list.json"):
        """【C++】构造函数：加载文件，不存在则用空列表"""
        self.filename = filename                        # 文件名存为属性，子类可复用
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.contact_list = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.contact_list = []

    # ---------- log 装饰器 ----------
    @staticmethod
    def log(func):
        """装饰器：记录方法执行时间"""
        def wrapper(self, *args, **kwargs):
            start = time.time()
            result = func(self, *args, **kwargs)
            print(f"  [{func.__name__}] 耗时: {time.time() - start:.4f}s")
            return result
        return wrapper

    # ---------- 核心 CRUD ----------
    @log
    def view_contacts(self):
        """【C++】void viewContacts() — 查看所有联系人"""
        if not self.contact_list:
            print("（空）")
            return
        for i, c in enumerate(self.contact_list, 1):
            print(f"  {i}. {c['name']} | {c.get('age','?')}岁 | {c.get('hobbies',[])}")

    @log
    def add_contact(self):
        """【C++】void addContact() — 添加联系人"""
        name = input("  姓名: ").strip()
        age = input("  年龄: ").strip()
        hobbies = input("  爱好(逗号分隔): ").strip().split(",")
        self.contact_list.append({
            "name": name,
            "age": int(age) if age.isdigit() else age,
            "hobbies": [h.strip() for h in hobbies if h.strip()]
        })
        print(f"  ✅ {name} 已添加")

    @log
    def delete_contact(self):
        """【C++】void deleteContact() — 删除联系人"""
        name = input("  要删除的姓名: ").strip()
        for c in self.contact_list:
            if c["name"] == name:
                self.contact_list.remove(c)
                print(f"  ✅ {name} 已删除")
                return
        print(f"  ❌ 未找到 {name}")

    @log
    def save_contacts(self):
        """【C++】void saveContacts() — 保存到文件"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.contact_list, f, ensure_ascii=False, indent=4)
        print(f"  💾 已保存到 {self.filename}")

    # ---------- 菜单 ----------
    def get_menu_options(self):
        """返回菜单选项（子类重写以扩展菜单）"""
        return [
            ("1", "查看联系人", self.view_contacts),
            ("2", "添加联系人", self.add_contact),
            ("3", "删除联系人", self.delete_contact),
            ("4", "保存并退出", self.save_contacts),
        ]

    def run(self):
        """主循环：打印菜单 → 分发 → 循环"""
        while True:
            options = self.get_menu_options()
            print(f"\n{'='*40}")
            for code, label, _ in options:
                print(f"  {code}. {label}")
            print("=" * 40)
            choice = input("请选择: ").strip()
            if choice == "4":
                self.save_contacts()
                print("再见！")
                break
            matched = [opt for opt in options if opt[0] == choice]
            if matched:
                matched[0][2]()                            # 调用对应方法
            else:
                print("无效选择")


# ============================================================
# 第二层：SearchableContactList（子类）—— 增加搜索功能
# 【C++】class SearchableContactList : public ContactList { ... };
# ============================================================
class SearchableContactList(ContactList):
    """继承 ContactList，增加搜索功能"""

    def __init__(self, filename="contact_list.json"):
        super().__init__(filename)                        # 【C++】: ContactList(filename)

    def search_by_name(self):
        """【新增】按姓名搜索"""
        keyword = input("  搜索姓名: ").strip()
        results = [c for c in self.contact_list if keyword in c["name"]]
        if results:
            for c in results:
                print(f"  🔍 {c['name']} | {c.get('age','?')}岁 | {c.get('hobbies',[])}")
        else:
            print(f"  ❌ 未找到包含 [{keyword}] 的联系人")

    def search_by_hobby(self):
        """【新增】按爱好搜索"""
        keyword = input("  搜索爱好: ").strip()
        results = [c for c in self.contact_list if any(keyword in h for h in c.get("hobbies", []))]
        if results:
            for c in results:
                print(f"  🔍 {c['name']} | 爱好: {c.get('hobbies',[])}")
        else:
            print(f"  ❌ 没人有 [{keyword}] 这个爱好")

    def get_menu_options(self):
        """【重写】在父类菜单基础上追加搜索选项"""
        options = super().get_menu_options()               # 先拿父类的菜单
        options.insert(-1, ("5", "搜索(按姓名)", self.search_by_name))
        options.insert(-1, ("6", "搜索(按爱好)", self.search_by_hobby))
        return options


# ============================================================
# 第三层：ColorContactList（孙子类）—— 增加彩色输出
# 【C++】class ColorContactList : public SearchableContactList { ... };
# ============================================================
class ColorContactList(SearchableContactList):
    """继承 SearchableContactList，增加彩色输出"""

    COLORS = {"HEAD": "\033[36m", "OK": "\033[32m", "ERR": "\033[31m", "END": "\033[0m"}

    def __init__(self, filename="contact_list.json"):
        super().__init__(filename)

    def view_contacts(self):
        """【重写】父类的查看方法，加上彩色标题"""
        c = self.COLORS
        if not self.contact_list:
            print(f"{c['ERR']}（空）{c['END']}")
            return
        for i, ct in enumerate(self.contact_list, 1):
            print(f"  {c['HEAD']}{i}. {ct['name']}{c['END']} | {ct.get('age','?')}岁 | {ct.get('hobbies',[])}")

    def get_menu_options(self):
        """【重写】加一个清空功能"""
        options = super().get_menu_options()
        options.insert(-1, ("7", "清空所有联系人", self.clear_all))
        return options

    def clear_all(self):
        """【新增】清空所有联系人"""
        confirm = input("  ⚠️ 确认清空? (yes/no): ").strip()
        if confirm.lower() == "yes":
            self.contact_list.clear()
            print("  ✅ 已清空")
        else:
            print("  已取消")


# ============================================================
# 程序入口
# ============================================================
if __name__ == "__main__":
    # 选一个来用：
    # app = ContactList()                # 基础版
    # app = SearchableContactList()      # 基础版 + 搜索
    app = ColorContactList()             # 基础版 + 搜索 + 彩色 + 清空
    app.run()