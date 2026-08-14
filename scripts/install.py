"""一键安装秦彻 Skill 到 Codex 技能目录。"""

import os
import shutil
import sys
from pathlib import Path

SKILL_NAME = "qinche-agent"


def codex_skill_dir() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    return codex_home / "skills"


def main() -> int:
    source = Path(__file__).resolve().parent.parent
    if not (source / "SKILL.md").exists():
        print(f"未找到 SKILL.md：{source}")
        return 1

    target = codex_skill_dir() / SKILL_NAME
    if target.exists():
        answer = input(f"{target} 已存在，覆盖安装？[y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("已取消。")
            return 0
        shutil.rmtree(target)

    shutil.copytree(source, target, ignore=shutil.ignore_patterns(".git", "scripts", "*.md", "LICENSE"))
    print(f"已安装到 {target}")
    print("在 Codex 中输入 $qinche-agent 或说「秦彻，过来。」即可使用。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
