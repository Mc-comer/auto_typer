import customtkinter as ctk
from tkinter import messagebox
import keyboard
import time


class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("打字丸 - Auto Typer")
        self.root.geometry("900x800")
        self.root.minsize(800, 800)
        self.is_typing = False
        
        # 设置主题
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # 设置UI
        self.setup_ui()
        
        # 更新窗口后立即最大化
        self.root.update()
        self.root.state('zoomed')
    
    def setup_ui(self):
        # 主滚动框架
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.root,
            fg_color=("#F0F0F0", "#1A1A2E"),
            scrollbar_button_color=("#6366F1", "#8B5CF6"),
            scrollbar_button_hover_color=("#4F46E5", "#7C3AED")
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ctk.CTkLabel(
            self.scroll_frame,
            text="权威打字丸⌨️",
            font=("Microsoft YaHei UI", 32, "bold"),
            text_color=("#1E293B", "#FFFFFF")
        )
        title_label.pack(pady=(0, 5))
        
        # 副标题
        subtitle_label = ctk.CTkLabel(
            self.scroll_frame,
            text="志霸不配用！",
            font=("Microsoft YaHei UI", 16),
            text_color=("#64748B", "#94A3B8")
        )
        subtitle_label.pack(pady=(0, 30))
        
        # 文本输入区域
        input_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=("#FFFFFF", "#252542"),
            corner_radius=12,
            border_width=2,
            border_color=("#E2E8F0", "#3A3A5E")
        )
        input_frame.pack(fill="x", pady=(0, 20), padx=5)
        
        input_label = ctk.CTkLabel(
            input_frame,
            text="请输入打字内容【仅英文】",
            font=("Microsoft YaHei UI", 16, "bold"),
            anchor="w",
            text_color=("#6366F1", "#8B5CF6")
        )
        input_label.pack(fill="x", padx=25, pady=(25, 15))
        
        # 文本框 - 使用CTkTextbox
        self.text_entry = ctk.CTkTextbox(
            input_frame,
            height=200,
            font=("Microsoft YaHei UI", 12),
            fg_color=("#F8FAFC", "#1E293B"),
            text_color=("#1E293B", "#F8FAFC"),
            border_width=1,
            border_color=("#E2E8F0", "#4A4A6E"),
            corner_radius=8,
            scrollbar_button_color=("#6366F1", "#8B5CF6"),
            scrollbar_button_hover_color=("#4F46E5", "#7C3AED")
        )
        self.text_entry.pack(fill="x", padx=25, pady=(0, 25))
        
        # 速度设置区域
        speed_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=("#FFFFFF", "#252542"),
            corner_radius=12,
            border_width=2,
            border_color=("#E2E8F0", "#3A3A5E")
        )
        speed_frame.pack(fill="x", pady=(0, 20), padx=5)
        
        speed_label = ctk.CTkLabel(
            speed_frame,
            text="打字速度（秒/字）",
            font=("Microsoft YaHei UI", 16, "bold"),
            anchor="w",
            text_color=("#8B5CF6", "#F472B6")
        )
        speed_label.pack(fill="x", padx=25, pady=(25, 20))
        
        # 速度控制框架
        speed_control_frame = ctk.CTkFrame(speed_frame, fg_color="transparent")
        speed_control_frame.pack(fill="x", padx=25, pady=(0, 25))
        
        # 速度显示和调节
        self.speed_var = ctk.DoubleVar(value=0.1)
        
        # 减号按钮
        decrease_btn = ctk.CTkButton(
            speed_control_frame,
            text="−",
            width=60,
            height=50,
            font=("Microsoft YaHei UI", 24, "bold"),
            fg_color=("#6366F1", "#8B5CF6"),
            hover_color=("#4F46E5", "#7C3AED"),
            command=lambda: self.adjust_speed(-0.05)
        )
        decrease_btn.pack(side="left", padx=(0, 15))
        
        # 速度输入框
        self.speed_entry = ctk.CTkEntry(
            speed_control_frame,
            textvariable=self.speed_var,
            width=150,
            height=50,
            font=("Microsoft YaHei UI", 18, "bold"),
            fg_color=("#F8FAFC", "#1E293B"),
            text_color=("#1E293B", "#F8FAFC"),
            border_color=("#E2E8F0", "#4A4A6E"),
            border_width=2
        )
        self.speed_entry.pack(side="left", padx=(0, 15))
        
        # 加号按钮
        increase_btn = ctk.CTkButton(
            speed_control_frame,
            text="+",
            width=60,
            height=50,
            font=("Microsoft YaHei UI", 24, "bold"),
            fg_color=("#6366F1", "#8B5CF6"),
            hover_color=("#4F46E5", "#7C3AED"),
            command=lambda: self.adjust_speed(0.05)
        )
        increase_btn.pack(side="left", padx=(0, 20))
        
        # 速度说明
        speed_info_label = ctk.CTkLabel(
            speed_control_frame,
            text="范围: 0.02秒(快) - 5.0秒(慢) | 默认: 0.1秒",
            font=("Microsoft YaHei UI", 12),
            text_color=("#64748B", "#94A3B8")
        )
        speed_info_label.pack(side="left", pady=(10, 0))
        
        # 按钮区域
        button_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 20))
        
        # 开始按钮
        self.start_button = ctk.CTkButton(
            button_frame,
            text="▶ 开始打字",
            font=("Microsoft YaHei UI", 18, "bold"),
            width=200,
            height=60,
            fg_color=("#22C55E", "#10B981"),
            hover_color=("#16A34A", "#059669"),
            text_color="#FFFFFF",
            corner_radius=12,
            command=self.start_typing
        )
        self.start_button.pack(side="left", padx=(0, 15), expand=True)
        
        # 结束按钮
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="⏹ 停止",
            font=("Microsoft YaHei UI", 18, "bold"),
            width=200,
            height=60,
            fg_color=("#EF4444", "#DC2626"),
            hover_color=("#DC2626", "#B91C1C"),
            text_color="#FFFFFF",
            corner_radius=12,
            command=self.stop_typing,
            state="disabled"
        )
        self.stop_button.pack(side="left", expand=True)
        
        # 状态显示区域
        status_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=("#FFFFFF", "#252542"),
            corner_radius=12,
            border_width=2,
            border_color=("#E2E8F0", "#3A3A5E")
        )
        status_frame.pack(fill="x", pady=(0, 20), padx=5)
        
        # 状态标签
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="状态: 等待开始",
            font=("Microsoft YaHei UI", 15, "bold"),
            anchor="w",
            text_color=("#22C55E", "#10B981")
        )
        self.status_label.pack(fill="x", padx=25, pady=(20, 10))
        
        # 提示标签
        tip_label = ctk.CTkLabel(
            status_frame,
            text="点击开始后有5秒时间切换到打字位置",
            font=("Microsoft YaHei UI", 13),
            anchor="w",
            text_color=("#64748B", "#94A3B8")
        )
        tip_label.pack(fill="x", padx=25, pady=(0, 20))
        
        # 作者信息
        author_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        author_frame.pack(fill="x", pady=(15, 0))
        
        author_label = ctk.CTkLabel(
            author_frame,
            text="志霸爱海罗！",
            font=("Microsoft YaHei UI", 11),
            text_color=("#64748B", "#94A3B8")
        )
        author_label.pack()
    
    def center_window(self):
        """将窗口居中显示"""
        # 先隐藏窗口
        self.root.withdraw()
        self.root.update_idletasks()
        
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 获取窗口尺寸
        width = 1000
        height = 1000
        
        # 计算居中位置，稍微向下偏移50像素
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2 + 50
        
        # 设置窗口位置和大小
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # 显示窗口
        self.root.deiconify()
        self.root.update()
    
    def adjust_speed(self, delta):
        """调整打字速度"""
        try:
            current = float(self.speed_var.get())
            new_speed = round(current + delta, 2)
            new_speed = max(0.02, min(5.0, new_speed))
            self.speed_var.set(new_speed)
        except ValueError:
            pass
    
    def validate_text(self, text):
        """验证文本是否只包含英文字符和基本标点"""
        allowed_chars = set(
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            " ,.!?;:'\"()-_=+[]{}<>/\\|@#$%^&*~`\n\t"
        )
        return all(c in allowed_chars for c in text)
    
    def start_typing(self):
        # 获取文本内容
        text = self.text_entry.get("1.0", "end").strip()
        
        if not text:
            messagebox.showwarning("警告", "废物张冠楠，快点输入")
            return
        
        # 验证文本
        if not self.validate_text(text):
            messagebox.showwarning("警告", "sb枪丸，只能输入英文内容和基本标点符号！")
            return
        
        # 获取打字速度
        try:
            speed = float(self.speed_var.get())
            if speed < 0.02 or speed > 5.0:
                messagebox.showwarning("警告", "打字速度应在 0.02 到 5.0 秒之间！")
                return
        except ValueError:
            messagebox.showwarning("警告", "请输入有效的打字速度！")
            return
        
        # 更新状态
        self.is_typing = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(text="状态: 准备中...请在5秒内切换到打字位置", text_color=("#F59E0B", "#F59E0B"))
        self.root.update()
        
        # 等待5秒
        for i in range(5, 0, -1):
            if not self.is_typing:
                break
            self.status_label.configure(text=f"状态: 倒计时 {i} 秒...", text_color=("#F59E0B", "#F59E0B"))
            self.root.update()
            time.sleep(1)
        
        if not self.is_typing:
            self.reset_ui()
            self.status_label.configure(text="状态: 已停止", text_color=("#EF4444", "#EF4444"))
            return
        
        # 开始打字 - 使用keyboard库模拟真实用户输入
        self.status_label.configure(text="状态: 正在打字...", text_color=("#3B82F6", "#3B82F6"))
        self.root.update()
        
        try:
            for char in text:
                if not self.is_typing:
                    break
                
                # 使用keyboard库发送按键事件，完全模拟用户真实输入
                keyboard.write(char, delay=0)
                
                time.sleep(speed)
                self.root.update()
        except Exception as e:
            messagebox.showerror("错误", f"打字过程中出错: {str(e)}")
        
        # 完成
        if self.is_typing:
            self.status_label.configure(text="状态: 打字完成", text_color=("#22C55E", "#22C55E"))
        else:
            self.status_label.configure(text="状态: 已停止", text_color=("#EF4444", "#EF4444"))
        
        self.reset_ui()
    
    def stop_typing(self):
        self.is_typing = False
        self.status_label.configure(text="状态: 正在停止...", text_color=("#F59E0B", "#F59E0B"))
        self.root.update()
    
    def reset_ui(self):
        self.is_typing = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")


def main():
    root = ctk.CTk()
    app = AutoTyperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
