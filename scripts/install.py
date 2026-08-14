"""一键安装秦彻 Skill 到 Codex 技能目录。"""

import os
import shutil
import sys
import tempfile
from pathlib import Path

SKILL_NAME = "qinche-agent"

# 只复制 Skill 运行所需内容，不包含 README、LICENSE、脚本
INCLUDE = ["SKILL.md", "agents", "references"]


def candidate_skill_dirs() -> list[Path]:
    """按优先级返回可能的技能目录。"""
    home = Path.home()
    dirs = []
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        dirs.append(Path(codex_home) / "skills")
    dirs.append(home / ".codex" / "skills")
    dirs.append(home / ".agents" / "skills")
    return dirs


def main() -> int:
    source = Path(__file__).resolve().parent.parent
    if not (source / "SKILL.md").exists():
        print(f"未找到 SKILL.md：{source}")
        return 1

    target = None
    for d in candidate_skill_dirs():
        if (d / SKILL_NAME).exists():
            target = d / SKILL_NAME
            break
        if d.parent.exists():
            target = d / SKILL_NAME
            break
    if target is None:
        print("未找到可用的技能目录，请设置 CODEX_HOME 后重试。")
        return 1

    if target.exists():
        try:
            answer = input(f"{target} 已存在，覆盖安装？[y/N] ").strip().lower()
        except EOFError:
            answer = "n"
        if answer not in ("y", "yes"):
            print("已取消。")
            return 0

    # 先复制到临时目录，成功后再替换，避免半途失败丢失旧安装
    with tempfile.TemporaryDirectory(prefix=f"{SKILL_NAME}-install-") as tmp:
        tmp_path = Path(tmp) / SKILL_NAME
        tmp_path.mkdir()
        for item in INCLUDE:
            src = source / item
            if not src.exists():
                print(f"缺少必要内容：{item}，安装中止。")
                return 1
            if src.is_dir():
                shutil.copytree(src, tmp_path / item)
            else:
                shutil.copy2(src, tmp_path / item)

        if target.exists():
            backup = target.with_name(target.name + ".bak")
            if backup.exists():
                shutil.rmtree(backup)
            os.replace(target, backup)
            try:
                os.replace(tmp_path, target)
            except Exception:
                os.replace(backup, target)
                raise
            shutil.rmtree(backup, ignore_errors=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(tmp_path, target)

    print(f"已安装到 {target}")
    print("在 Codex 中输入 $qinche-agent，或说「秦彻，过来。」即可使用。")
    print("若新会话无法激活，请确认技能目录已被 Codex 识别。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
