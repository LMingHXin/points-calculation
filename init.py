#!usr/bin/python3
import tkinter as tk
import json
from tkinter.messagebox import showinfo, showwarning, askyesno

grades = []  # Students Names


class Obj:

    def __init__(self) -> None:  # 创建GUI框架
        self.mainroot = tk.Tk()
        self.ety: list = []
        self.sety1: list = []
        self.cstu: list = []
        self.sety2: list = []
        self.lbs: list = []
        self.res: int = 0
        self.sres: int = 1
        self.grppoint: dict = {}
        self.block = True
        self.btn1 = tk.Button(self.mainroot, text='分组/改组操作', command=self.change_setup_UI)
        self.btn2 = tk.Button(self.mainroot, text='单周总结加分', command=self.sum)
        self.btn1.grid(row=0, column=0, padx=10, pady=4)
        self.btn2.grid(row=1, column=0, padx=10, pady=4)
        self.stu: dict = {}
        self.grades: list = grades
        with open("data.json", 'r', encoding='UTF-8') as dt:
            self.stu: dict = json.load(dt)
        with open("spcgrp.json", 'r', encoding='UTF-8') as spg:
            self.spgrp: int = json.load(spg)
        if self.stu:
            self.block = False
        self.mainroot.mainloop()

    def change_setup_UI(self) -> None:  # 分组/改组
        self.changeroot = tk.Tk()
        self.btn3 = tk.Button(self.changeroot, text='分组', command=self.group)
        self.btn4 = tk.Button(self.changeroot, text='改组', command=self.chgroup)
        self.btn3.grid(row=0, column=0, padx=10, pady=4)
        self.btn4.grid(row=1, column=0, padx=10, pady=4)

    def sum(self) -> None:  # 总分
        self.sumroot = tk.Tk()
        if self.block:
            showwarning(title='警告', message='暂未找到分组情况，请先进行分组后使用记分系统')
            self.sumroot.destroy()
            return
        print(self.sres)
        if self.sres > 9:
            tmplist: list = []
            tmps: int = -999
            for i in range(1, 10):
                if self.grppoint[i] > tmps:
                    tmps = i
                    tmplist = []
                    tmplist.append(i)
                if self.grppoint[i] == tmps:
                    tmplist.append(i)
            for i in tmplist:
                showinfo(title='提示', message=f'总分结束，分数最高的组为第{i}组')
            self.sumroot.destroy()
            return
        tk.Label(self.sumroot, text=f'请编辑第{self.sres}组的积分情况').grid(rowspan=1, columnspan=3)
        if self.sres == self.spgrp:
            for i in range(1, 8):
                tk.Label(self.sumroot, text=f'请输入{self.stu[str(self.sres)][i - 1]}的积分情况').grid(row=i + 1, column=0)
                tmp = tk.Entry(self.sumroot)
                self.sety1.append(tmp)  # type: ignore
                tmp.grid(row=i + 1, column=1)
                tmp1 = tk.Entry(self.sumroot)
                self.sety2.append(tmp)  # type: ignore
                tmp1.grid(row=i + 1, column=2)
            tk.Button(self.sumroot, text='下一组', command=self.sumn).grid(row=9, columnspan=3)
        else:
            for i in range(1, 7):
                tk.Label(self.sumroot, text=f'请输入{self.stu[str(self.sres)][i - 1]}的积分情况').grid(row=i + 1, column=0)
                tmp = tk.Entry(self.sumroot)
                self.sety1.append(tmp)  # type: ignore
                tmp.grid(row=i + 1, column=1)
                tmp1 = tk.Entry(self.sumroot)
                self.sety2.append(tmp)  # type: ignore
                tmp1.grid(row=i + 1, column=2)
                tmp.grid(row=i + 1, column=1)
            tk.Button(self.sumroot, text='下一组', command=self.sumn).grid(row=8, columnspan=3)

    def sumn(self) -> None:  # 真·总分
        self.grppoint[self.sres] = 0
        for i in range(len(self.sety1)):  # type: ignore
            if self.stu[str(self.sres)][i] in self.cstu:
                self.grppoint[self.sres] += eval('0' + self.sety1[i].get())*1.5 + eval('0' + self.sety2[i].get())
            else:
                self.grppoint[self.sres] += eval('0' + self.sety1[i].get())*0.75 + eval('0' + self.sety2[i].get())
        print(self.grppoint[self.sres])
        self.sres += 1
        self.sumroot.destroy()
        self.sum()

    def group(self) -> None:  # 重分组
        if not self.block:
            if askyesno(title='提示', message='已进行分组，是否全部重新分组'):
                with open("data.json", 'w', encoding='UTF-8') as dt:
                    replace: dict = {}
                    dt.write(json.dumps(replace))
                self.stu = {}
                self.engroup()
            else:
                self.changeroot.destroy()
        else:
            self.engroup()

    def engroup(self) -> None:  # 新分组
        self.spcgrp = tk.Tk()
        self.grpvar = tk.IntVar(self.spcgrp)
        self.spcgrp.title("请选择哪个小组为7人小组")
        for i in range(1, 8):
            tk.Radiobutton(self.spcgrp, text=f'{i}', value=i, variable=self.grpvar).pack(anchor=tk.W)  # type: ignore
        tk.Button(self.spcgrp, text='确定', command=self.Setspcgrp).pack(fill=tk.X)
        self.spcgrp.mainloop()

    def n_engroup(self) -> None:  # 真·新分组，录入
        self.ety = []
        self.res += 1
        if self.res > 9:
            self.stu['cstu'] = self.cstu
            with open('data.json', 'w', encoding='UTF-8') as dt:
                dt.write(json.dumps(self.stu))
            showinfo(title='提示', message='数据录入成功')
            self.changeroot.destroy()
            return
        self.egroup = tk.Tk()
        self.laen = tk.Label(self.egroup, text=f'请选择第{self.res}组的成员').grid(row=0, columnspan=1)
        if self.res == self.spgrp:
            for i in range(1, 8):
                tk.Label(self.egroup, text=f'请输入第{i}名成员姓名').grid(row=i, column=0)
                tmp = tk.Entry(self.egroup)
                self.ety.append(tmp)  # type: ignore
                tmp.grid(row=i, column=1)
            tk.Button(self.egroup, text='下一组', command=self.round).grid(row=8, columnspan=2)
        else:
            for i in range(1, 7):
                tk.Label(self.egroup, text=f'请输入第{i}名成员姓名').grid(row=i, column=0)
                tmp = tk.Entry(self.egroup)
                self.ety.append(tmp)  # type: ignore
                tmp.grid(row=i, column=1)
            tk.Button(self.egroup, text='下一组', command=self.round).grid(row=7, columnspan=2)
        self.egroup.mainloop()

    def round(self) -> None:  # 新分组轮换，判断，加入每组中的后进生
        tmpstu: list = []
        self.stu[self.res] = []
        tmpstusave: list = []
        for i in range(len(self.ety)):
            tmp = self.ety[i].get()
            if tmp in grades:
                if grades.index(tmp) in tmpstu:
                    showwarning(title='提示', message='好像有重名了，请返回并修改')
                    return
                tmpstu.append(grades.index(tmp))
                tmpstusave.append(grades.index(tmp))
            else:
                showwarning(title='提示', message='似乎有人不在该班级或出现空的情况，请检查并修改，如果是7人组选择错误，请返回主界面并重新选择7人组')
                return
        tmpstu.sort(reverse=True)
        for j in range(len(tmpstu)):
            if j <= 2:
                self.cstu.append(str(grades[tmpstu[j]]))
            self.stu[self.res].append(str(grades[tmpstusave[j]]))
        print(self.cstu)
        self.egroup.destroy()
        self.n_engroup()

    def chgroup(self) -> None:  # 更换组
        #  TODO change one's group
        showinfo(title='啊啊啊啊啊啊啊', message='我还没写我不想写我不会写')

    def Setspcgrp(self) -> None:  # 设置7人组
        self.spgrp = self.grpvar.get()
        with open('spcgrp.json', 'w', encoding='UTF-8') as spg:
            spg.write(json.dumps(self.spgrp))
        self.spcgrp.destroy()
        self.n_engroup()


cls = Obj()
