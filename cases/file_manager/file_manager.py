"""
经典案例 3：文件管理器
覆盖知识点：tmp_path 内置 fixture、文件读写测试、yield 清理、monkeypatch
运行方式：py312 -m pytest test_file_manager.py -v
"""
import json
from pathlib import Path


class FileManager:
    """简单的文件读写管理器"""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def write_text(self, name: str, content: str) -> Path:
        """写入文本文件（自动建目录）"""
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def read_text(self, name: str) -> str:
        """读取文本文件；不存在抛 FileNotFoundError"""
        path = self.root / name
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {name}")
        return path.read_text(encoding="utf-8")

    def save_json(self, name: str, data: dict) -> Path:
        """保存 JSON 数据"""
        path = self.root / name
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def load_json(self, name: str) -> dict:
        """读取 JSON 文件"""
        return json.loads(self.read_text(name))

    def list_files(self) -> list:
        """列出根目录下的所有文件（不含子目录内）"""
        return [p.name for p in self.root.iterdir() if p.is_file()]

    def delete(self, name: str) -> bool:
        """删除文件，返回是否删除成功"""
        path = self.root / name
        if path.exists() and path.is_file():
            path.unlink()
            return True
        return False
