# rename_step_via_powershell.py
"""
用 Python 遍历文件，逐个调用 PowerShell 的 Rename-Item 改名。
PowerShell 在 DRM 白名单里，改名不会被拦截。
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ============ 配置区 ============
SRC_DIR = Path(r"C:\Users\zwsoft\Desktop\ZW\step_as_txt")
PATTERN = r"\.(step|stp)\.txt$"   # 匹配 .step.txt / .stp.txt
RECURSE = True
DRY_RUN = True                     # 先 True 预演，确认没问题再改 False
LOG_FILE = SRC_DIR / "rename_log.txt"
# ================================


def log(msg: str, level: str = "INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}][{level}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass


def ps_rename(old_full: Path, new_name: str) -> tuple[bool, str]:
    """
    调 PowerShell 执行 Rename-Item。
    返回 (成功?, 错误信息)。
    """
    # 用单引号包裹路径，路径里的单引号用 '' 转义（PowerShell 规则）
    old_escaped = str(old_full).replace("'", "''")
    new_escaped = new_name.replace("'", "''")

    ps_cmd = (
        f"Rename-Item -LiteralPath '{old_escaped}' "
        f"-NewName '{new_escaped}' -ErrorAction Stop"
    )

    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return False, "PowerShell 超时"
    except FileNotFoundError:
        return False, "找不到 powershell.exe"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"

    if result.returncode == 0:
        return True, ""

    err = (result.stderr or result.stdout or "").strip()
    return False, err or f"returncode={result.returncode}"


def main():
    if not SRC_DIR.exists():
        log(f"目录不存在: {SRC_DIR}", "FAIL")
        return 1

    log("========== 开始批量改名 ==========")
    log(f"目录: {SRC_DIR}")
    log(f"递归: {RECURSE}")
    log(f"DryRun: {DRY_RUN}")
    log(f"日志: {LOG_FILE}")

    # 收集文件
    if RECURSE:
        all_files = [p for p in SRC_DIR.rglob("*") if p.is_file()]
    else:
        all_files = [p for p in SRC_DIR.iterdir() if p.is_file()]

    import re
    pat = re.compile(PATTERN, re.IGNORECASE)
    targets = [p for p in all_files if pat.search(p.name)]

    if not targets:
        log("没有找到 .step.txt / .stp.txt 文件", "SKIP")
        return 0

    log(f"共找到 {len(targets)} 个文件")

    ok = fail = skip = 0

    for src in targets:
        new_name = pat.sub(lambda m: f".{m.group(1).lower()}", src.name)
        dst = src.parent / new_name

        if dst.exists():
            log(f"跳过（目标已存在）: {src.name} -> {new_name}", "SKIP")
            skip += 1
            continue

        if DRY_RUN:
            log(f"[预演] {src.name} -> {new_name}", "DRY")
            continue

        success, err = ps_rename(src, new_name)
        if success:
            log(f"OK: {src.name} -> {new_name}", "OK")
            ok += 1
        else:
            log(f"失败: {src.name} -> {new_name} | {err}", "FAIL")
            fail += 1

    log("========== 完成 ==========")
    log(f"成功: {ok}  失败: {fail}  跳过: {skip}")

    if DRY_RUN:
        print()
        print(">>> 这是预演模式，没有实际改名。")
        print(">>> 把 DRY_RUN 改成 False 再跑一次即可真正执行。")

    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())