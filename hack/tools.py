from __future__ import annotations
from typing import Tuple, List
import re
import sh
from pathlib import Path
import requests
from dataclasses import dataclass
import tomli, tomli_w

VALID_VERSION_TAG_PATTERN = re.compile("^refs/tags/(\d+)\.(\d+)\.(\d+)$")
MIN_VSCODE_SERVER_VERSION = (1, 50, 0)

@dataclass
class Tag:
    version: Tuple[int, int, int]
    commit_id: str

    def __hash__(self) -> int:
        return hash(self.version)

    def __lt__(self, other) -> bool:
        return self.version < other.version

    def __eq__(self, other) -> bool:
        return self.version == other.version


def fetch_tags(git_url: str) -> list[Tag]:
    ret = sh.git("ls-remote", "--refs", "--tags", git_url)
    ret = ret.strip().split("\n")
    commit_to_tags: List[Tuple[str, str]] = list(map(str.split, ret))

    tags = []
    for commit_id, tag_ref in commit_to_tags:
        re_ret = VALID_VERSION_TAG_PATTERN.match(tag_ref)
        if re_ret is None:
            continue
        major, minor, micro = re_ret.groups()
        tags.append(
            Tag(version=(int(major), int(minor), int(micro)), commit_id=commit_id)
        )
    return sorted(tags)


def fetch_vscode_server_tags() -> list[Tag]:
    return list(filter(lambda tag: tag.version >= MIN_VSCODE_SERVER_VERSION ,fetch_tags("https://github.com/microsoft/vscode.git")))


def fetch_self_repo_tags() -> list[Tag]:
    return fetch_tags("https://github.com/zen-xu/vscode-server-bin.git")


def filter_unreleased_vscode_server_tags() -> list[Tag]:
    return sorted(set(fetch_vscode_server_tags()) - set(fetch_self_repo_tags()))


def update_server_bin(tag: Tag):
    rsp = requests.get(f"https://update.code.visualstudio.com/commit:{tag.commit_id}/server-linux-x64/stable")
    rsp.raise_for_status()
    module_root =Path(__file__).parent.parent
    module_dir = module_root /  "vscode_server_bin"
    (module_dir / "bin.tar.gz").write_bytes(rsp.content)
    (module_dir / "vscode-commit-id").write_text(tag.commit_id)
    pyproject_toml = module_root / "pyproject.toml"
    with open(pyproject_toml, "rb") as f:
        config = tomli.load(f)
    config["tool"]["poetry"]["version"] = ".".join(map(str, tag.version))
    with open(pyproject_toml, "wb") as f:
        tomli_w.dump(config, f)