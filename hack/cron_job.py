from tools import filter_unreleased_vscode_server_tags, update_server_bin


if __name__ == "__main__":
    for tag in filter_unreleased_vscode_server_tags():
        print(f'update server bin: {tag}')
        update_server_bin(tag)

