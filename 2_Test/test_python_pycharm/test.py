import locale
import sys


def get_windows_locale():
    """获取 Windows 系统语言"""
    try:
        # 方法1：获取默认区域设置
        lang_code, encoding = locale.getencoding()
        if lang_code:
            return lang_code
    except:
        pass

    # 方法2：设置 locale 后再获取
    try:
        locale.setlocale(locale.LC_ALL, '')
        lang_code, encoding = locale.getlocale()
        if lang_code:
            return lang_code
    except:
        pass

    return 'en_US'  # 默认


# 测试
lang = get_windows_locale()
print(f"Windows 系统语言: {lang}")