#!/usr/bin/env python3
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
# The upstream generator has no option to hide these footer counters.
STAR_PATH = (
    "M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 "
    "1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 "
    "1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28"
    "l4.21-.611L7.327.668A.75.75 0 018 .25zm0 2.445L6.615 5.5a.75.75 0 "
    "01-.564.41l-3.097.45 2.24 2.184a.75.75 0 01.216.664l-.528 3.084 2.769-"
    "1.456a.75.75 0 01.698 0l2.77 1.456-.53-3.084a.75.75 0 01.216-.664l2.24-"
    "2.183-3.096-.45a.75.75 0 01-.564-.41L8 2.694v.001z"
)
FORK_PATH = (
    "M5 3.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm0 2.122a2.25 2.25 0 10-1.5 "
    "0v.878A2.25 2.25 0 005.75 8.5h1.5v2.128a2.251 2.251 0 101.5 0V8.5h1.5"
    "a2.25 2.25 0 002.25-2.25v-.878a2.25 2.25 0 10-1.5 0v.878a.75.75 0 "
    "01-.75.75h-4.5A.75.75 0 015 6.25v-.878zm3.75 7.378a.75.75 0 11-1.5 0 "
    ".75.75 0 011.5 0zm3-8.75a.75.75 0 100-1.5.75.75 0 000 1.5z"
)
TARGET_ICON_PATHS = {STAR_PATH, FORK_PATH}


def _svg_tag(local_name):
    return f"{{{SVG_NS}}}{local_name}"


def remove_repository_stats(svg_path):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    parent_map = {child: parent for parent in root.iter() for child in parent}

    icon_paths = [
        node
        for node in root.iter(_svg_tag("path"))
        if node.get("d") in TARGET_ICON_PATHS
    ]

    removed = 0
    for icon_path in icon_paths:
        icon_group = parent_map.get(icon_path)
        group_parent = parent_map.get(icon_group)
        if icon_group is None or group_parent is None:
            continue

        siblings = list(group_parent)
        group_index = siblings.index(icon_group)
        value_node = (
            siblings[group_index + 1] if group_index + 1 < len(siblings) else None
        )
        if value_node is None or value_node.tag != _svg_tag("text"):
            continue

        group_parent.remove(icon_group)
        group_parent.remove(value_node)
        removed += 1

    if removed:
        ET.register_namespace("", SVG_NS)
        tree.write(svg_path, encoding="utf-8", xml_declaration=False)

    return removed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    for svg_path in args.paths:
        removed = remove_repository_stats(svg_path)
        print(f"{svg_path}: removed {removed} repository statistics")


if __name__ == "__main__":
    main()
