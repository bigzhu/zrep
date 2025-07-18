#!/usr/bin/env python3
# file_name=zrep.py
import argparse
import os
import sys
from shutil import move
from tempfile import mkstemp

import magic


def is_binary_file(file_path: str) -> bool:
    """Check if a file is binary using python-magic."""
    try:
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        return "text" not in file_type
    except Exception:
        # If magic fails, try to read a small chunk to detect binary
        try:
            with open(file_path, "rb") as f:
                chunk = f.read(1024)
                return b"\0" in chunk
        except Exception:
            return True


def check_pattern_in_file(file_path: str, pattern: str) -> bool:
    """检查文件中是否包含需要替换的内容"""
    try:
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            return pattern in f.read()
    except Exception:
        return False


def replace_in_file(file_path: str, pattern: str, subst: str) -> bool:
    """在文件中进行字符串替换"""
    if is_binary_file(file_path):
        return False

    if not check_pattern_in_file(file_path, pattern):
        return False

    try:
        print(f"替换: {file_path}")

        # Read original file
        with open(file_path, encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Replace content
        new_content = content.replace(pattern, subst)

        # Write to temp file first
        fh, temp_path = mkstemp(dir=os.path.dirname(file_path))
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            os.close(fh)

            # Atomic replacement
            move(temp_path, file_path)
            return True
        except Exception:
            os.close(fh)
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise
    except Exception as e:
        print(f"错误: 无法处理文件 {file_path}: {e}")
        return False


class ZRep:
    """主要的字符串替换工具类"""

    DEFAULT_EXCLUDED_DIRS = {
        ".git",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".venv",
        "venv",
        ".env",
        "dist",
        "build",
        ".tox",
    }

    DEFAULT_EXCLUDED_FILES = {
        ".gitignore",
        ".dockerignore",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        "*.so",
        "*.dll",
        "*.dylib",
        "*.egg-info",
    }

    def __init__(
        self,
        excluded_dirs: set[str] | None = None,
        excluded_files: set[str] | None = None,
    ):
        self.excluded_dirs = excluded_dirs or self.DEFAULT_EXCLUDED_DIRS
        self.excluded_files = excluded_files or self.DEFAULT_EXCLUDED_FILES

    def get_file_paths(self, root_path: str) -> list[str]:
        """递归获取所有需要处理的文件路径"""
        file_paths = []

        try:
            for item in os.listdir(root_path):
                if item in self.excluded_dirs:
                    continue

                item_path = os.path.join(root_path, item)

                if os.path.isdir(item_path):
                    file_paths.extend(self.get_file_paths(item_path))
                elif os.path.isfile(item_path):
                    # Check if file should be excluded
                    if not any(
                        item.endswith(pattern.lstrip("*"))
                        for pattern in self.excluded_files
                        if pattern.startswith("*")
                    ):
                        if item not in self.excluded_files:
                            file_paths.append(item_path)

        except PermissionError:
            print(f"警告: 没有权限访问目录 {root_path}")
        except Exception as e:
            print(f"错误: 访问目录时出错 {root_path}: {e}")

        return file_paths

    def replace_in_directory(self, root_path: str, pattern: str, subst: str) -> int:
        """在目录中进行字符串替换"""
        if not pattern:
            print("错误: 搜索模式不能为空")
            return 0

        file_paths = self.get_file_paths(root_path)
        replaced_count = 0

        print(f"发现 {len(file_paths)} 个文件需要检查")
        print(f"将 '{pattern}' 替换为 '{subst}'")

        for file_path in file_paths:
            if replace_in_file(file_path, pattern, subst):
                replaced_count += 1

        return replaced_count


def create_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description="zrep - 递归替换文件中的字符串",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  zrep "old_string" "new_string"                    # 在当前目录替换
  zrep "old_string" "new_string" --dir /path/to/dir  # 在指定目录替换
  zrep "old_string" "new_string" --dry-run           # 预览模式，不实际替换
        """,
    )

    parser.add_argument("pattern", help="要替换的字符串")
    parser.add_argument("replacement", help="替换成的字符串")
    parser.add_argument(
        "--dir",
        "-d",
        default=".",
        help="要处理的目录路径 (默认: 当前目录)",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="预览模式，显示会被替换的文件但不实际替换",
    )
    parser.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="额外排除的目录 (可多次使用)",
    )
    parser.add_argument(
        "--exclude-file",
        action="append",
        default=[],
        help="额外排除的文件模式 (可多次使用)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")

    return parser


def main() -> None:
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()

    # 创建 ZRep 实例
    excluded_dirs = set(ZRep.DEFAULT_EXCLUDED_DIRS)
    excluded_dirs.update(args.exclude_dir)

    excluded_files = set(ZRep.DEFAULT_EXCLUDED_FILES)
    excluded_files.update(args.exclude_file)

    zrep = ZRep(excluded_dirs=excluded_dirs, excluded_files=excluded_files)

    # 验证目录
    if not os.path.exists(args.dir):
        print(f"错误: 目录不存在: {args.dir}")
        sys.exit(1)

    if not os.path.isdir(args.dir):
        print(f"错误: 路径不是目录: {args.dir}")
        sys.exit(1)

    # 执行替换
    try:
        if args.dry_run:
            print("[预览模式] 以下文件将被处理:")
            file_paths = zrep.get_file_paths(args.dir)
            for file_path in file_paths:
                if check_pattern_in_file(file_path, args.pattern):
                    print(f"  - {file_path}")
            matching_files = [
                f for f in file_paths if check_pattern_in_file(f, args.pattern)
            ]
            print(f"\n总共找到 {len(matching_files)} 个包含模式的文件")
        else:
            replaced_count = zrep.replace_in_directory(
                args.dir, args.pattern, args.replacement
            )
            print(f"\n完成! 共替换了 {replaced_count} 个文件")
    except KeyboardInterrupt:
        print("\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
