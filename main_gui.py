# main_gui.py
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from utils.calculator import process_files

class SubsidyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("差旅津贴计算器")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        self.root.eval('tk::PlaceWindow . center')

        # 文件路径存储
        self.company_path = None
        self.client_path = None

        # 标题
        title = ttk.Label(
            root,
            text="差旅津贴自动计算工具",
            font=("Microsoft YaHei", 14, "bold")
        )
        title.pack(pady=(20, 10))

        # 按钮区域
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        # 按钮1：导入公司报销表
        self.btn_company = ttk.Button(
            btn_frame,
            text="📁 导入公司报销表",
            command=self.select_company_file,
            bootstyle=INFO,
            width=25
        )
        self.btn_company.grid(row=0, column=0, padx=10, pady=5)

        # 按钮2：导入客户结算表
        self.btn_client = ttk.Button(
            btn_frame,
            text="📁 导入客户结算表",
            command=self.select_client_file,
            bootstyle=INFO,
            width=25
        )
        self.btn_client.grid(row=1, column=0, padx=10, pady=5)

        # 按钮3：计算并导出（初始禁用）
        self.btn_calculate = ttk.Button(
            btn_frame,
            text="✅ 计算津贴并导出",
            command=self.run_calculation,
            bootstyle=SUCCESS,
            width=25,
            state=DISABLED  # 初始禁用
        )
        self.btn_calculate.grid(row=2, column=0, padx=10, pady=15)

        # 文件路径显示区域
        path_frame = ttk.Frame(root)
        path_frame.pack(fill="x", padx=30, pady=(0, 10))

        self.company_label = ttk.Label(path_frame, text="公司报销表：未选择", foreground="gray", font=("Microsoft YaHei", 9))
        self.company_label.pack(anchor="w", pady=2)

        self.client_label = ttk.Label(path_frame, text="客户结算表：未选择", foreground="gray", font=("Microsoft YaHei", 9))
        self.client_label.pack(anchor="w", pady=2)

        # 底部提示
        tip = ttk.Label(
            root,
            text="支持 .xlsx / .xls 格式 | 作者：XXX",
            font=("Microsoft YaHei", 8),
            foreground="gray"
        )
        tip.pack(side="bottom", pady=5)

    def select_company_file(self):
        path = filedialog.askopenfilename(
            title="请选择【公司报销明细表】",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if path:
            self.company_path = path
            self.company_label.config(text=f"公司报销表：{os.path.basename(path)}", foreground="black")
            self.check_ready()

    def select_client_file(self):
        path = filedialog.askopenfilename(
            title="请选择【客户结算明细表】",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        if path:
            self.client_path = path
            self.client_label.config(text=f"客户结算表：{os.path.basename(path)}", foreground="black")
            self.check_ready()

    def check_ready(self):
        """检查两个文件是否都已选择，决定是否启用计算按钮"""
        if self.company_path and self.client_path:
            self.btn_calculate.config(state=NORMAL)
        else:
            self.btn_calculate.config(state=DISABLED)

    def run_calculation(self):
        try:
            result_df = process_files(self.company_path, self.client_path)

            base_name = os.path.splitext(self.client_path)[0]
            output_path = f"{base_name}_差旅津贴计算结果.xlsx"
            result_df.to_excel(output_path, index=False)

            # 自动打开结果所在文件夹（可选）
            import subprocess
            subprocess.Popen(f'explorer /select,"{output_path}"')

            messagebox.showinfo("✅ 成功", f"结果已保存并自动打开：\n{output_path}")

        except Exception as e:
            messagebox.showerror("❌ 错误", f"计算失败：\n{str(e)}")

def main():
    root = ttk.Window(themename="cosmo")  # 可换 "darkly", "minty" 等
    app = SubsidyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()