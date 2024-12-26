from tkinter import ttk
from src.core.constants import COLORS

def setup_styles():
    """设置控件样式"""
    style = ttk.Style()
    
    # 强制使用 clam 主题
    style.theme_use('clam')
    
    # 创建进度条布局
    style.layout('Custom.TProgressbar', 
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                            {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'})])
    
    # 配置进度条样式
    style.configure('Custom.TProgressbar',
                   troughcolor=COLORS['TROUGH_COLOR'],
                   background=COLORS['PRIMARY'],
                   thickness=25,
                   borderwidth=0)
    
    # 确保进度条样式被正确应用
    style.theme_settings('clam', {
        'Custom.TProgressbar': {
            'layout': [
                ('Custom.Horizontal.Progressbar.trough', {'sticky': 'nswe'}),
                ('Custom.Horizontal.Progressbar.pbar', {'side': 'left', 'sticky': 'ns'})
            ]
        }
    }) 