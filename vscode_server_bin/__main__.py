from pathlib import Path
import tarfile
import tempfile
import shutil

commit_id = (Path(__file__).parent / "vscode-commit-id").read_text(encoding="utf8").strip()

def members(tar, strip):
    members = []
    for member in tar.getmembers():
        p = Path(member.path)
        member.path = p.relative_to(*p.parts[:strip])
        members.append(member)
    return members

with tempfile.TemporaryDirectory() as tmp_dir:
    output_dir = Path(tmp_dir) / commit_id
    output_dir.mkdir(parents=True)
    with tarfile.open((Path(__file__).parent / "bin.tar.gz").absolute()) as tar_bin:
        tar_bin.extractall(output_dir, members=members(tar_bin, 1))

    vscode_server_bin_dir = Path.home() / ".vscode-server/bin"
    vscode_server_bin_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(output_dir), str(vscode_server_bin_dir))
