from src.gui.app import VideoOrganizerGUI
from ctypes import windll, byref, c_int, sizeof
from src.core.constants import COLORS

def main():
    app = VideoOrganizerGUI()
    
    # 等待窗口创建完成后再设置深色模式
    app.root.update()
    
    # 获取真实窗口句柄并应用深色模式
    try:
        hwnd = windll.user32.GetParent(app.root.winfo_id())
        
        # 将十六进制颜色字符串转换为整数
        # 假设 COLORS['BG_COLOR'] 格式为 '#RRGGBB'
        bg_color = int(COLORS['BG_COLOR'].replace('#', '0x'), 16)
        
        windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            35,  # DWMWA_CAPTION_COLOR
            byref(c_int(bg_color)),  # 使用背景色
            sizeof(c_int)
        )
        # 保持深色模式开启
        windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            20,  # DWMWA_USE_IMMERSIVE_DARK_MODE
            byref(c_int(1)),
            sizeof(c_int)
        )
    except:
        pass

    app.run()

if __name__ == "__main__":
    main()
