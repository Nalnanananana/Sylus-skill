"""校验秦彻 Skill 结构是否合法。"""

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/inner-world.md",
    "references/thinking.md",
    "references/voice.md",
    "references/relationships.md",
    "references/agent-mode.md",
    "references/canon.md",
    "references/examples.md",
]


def check_frontmatter(text: str) -> list[str]:
    errors = []
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return ["缺少 YAML frontmatter"]
    fm = m.group(1)
    if "name: qinche-agent" not in fm:
        errors.append("frontmatter 缺少 name: qinche-agent")
    if "description:" not in fm:
        errors.append("frontmatter 缺少 description")
    return errors


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        path = SKILL_DIR / rel
        if not path.is_file():
            errors.append(f"缺少文件：{rel}")
            continue
        if path.stat().st_size == 0:
            errors.append(f"文件为空：{rel}")

    skill_md = SKILL_DIR / "SKILL.md"
    if skill_md.is_file():
        text = skill_md.read_text(encoding="utf-8")
        errors.extend(check_frontmatter(text))

    openai_yaml = SKILL_DIR / "agents" / "openai.yaml"
    if openai_yaml.is_file():
        text = openai_yaml.read_text(encoding="utf-8")
        if "allow_implicit_invocation" not in text:
            errors.append("agents/openai.yaml 缺少 policy 配置")

    for md in (SKILL_DIR / "references").glob("*.md"):
        text = md.read_text(encoding="utf-8")
        if "——" in text:
            errors.append(f"{md.name} 含禁用破折号「——」")

    if errors:
        print("校验失败：")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("Skill 结构校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
