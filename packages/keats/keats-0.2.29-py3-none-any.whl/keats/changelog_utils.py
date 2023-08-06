import datetime
import json
from collections import OrderedDict
from os.path import isfile

from .utils import write_safe_file

ENTRY_TEMPLATE = """
## {version}
**{date}**
{description}

{changes}
"""


class ChangeLogWriter:

    DESCRIPTION = "description"
    CHANGES = "changes"
    RELEASE = "release"
    DATE = "date"

    def __init__(self, path, title, mdpath):
        self.path = path
        self.title = title
        self.mdpath = mdpath

    @property
    def log(self):
        return self._load()

    def _load(self):
        if isfile(self.path):
            with open(self.path, "r") as f:
                text = f.read()
                if text.strip() == "":
                    changelog = {}
                else:
                    changelog = json.loads(text)
        else:
            changelog = {}
        return self._sort_changelog(changelog)

    @classmethod
    def _sort_changelog(cls, changelog):
        sorted_entries = sorted(
            [(k, v) for k, v in changelog.items()],
            key=lambda x: x[1][cls.DATE],
            reverse=True,
        )
        return OrderedDict(sorted_entries)

    @classmethod
    def new_entry(cls, d, changes):
        now = datetime.datetime.now()
        return {cls.DESCRIPTION: d, cls.DATE: now.isoformat(), cls.CHANGES: changes}

    def to_markdown(self):
        if not self.title:
            s = "# change log"
        else:
            s = "# {} change log".format(self.title)

        entries = []
        for k, d in self.log.items():
            changes = "\n".join([" - " + c for c in d[self.CHANGES]])
            entry = ENTRY_TEMPLATE.format(
                version=k,
                date=d[self.DATE],
                description=d[self.DESCRIPTION],
                changes=changes,
            )
            if "released" in d:
                entry += "\n" + d["released"]
            entries.append(entry)
        s += "\n".join(entries)
        return s

    def save_to_markdown(self):
        write_safe_file(self.mdpath, self.to_markdown())

    def write(self, d):
        write_safe_file(self.path, json.dumps(self._sort_changelog(d), indent=2))

    def update(self, version, description, changes):
        changelog = self.log

        if version in changelog:
            entry = changelog[version]
            if description.strip():
                entry[self.DESCRIPTION] = description

            now = datetime.datetime.now()
            entry[self.DATE] = now.isoformat()
            unique_changes = []
            for e in entry[self.CHANGES] + changes:
                if e not in unique_changes:
                    unique_changes.append(e)
            entry[self.CHANGES] = unique_changes
        else:
            entry = self.new_entry(description, changes)
        changelog[version] = entry
        self.write(changelog)

    def mark_as_released(self, version):
        d = self.log
        now = datetime.datetime.now()
        if "released" not in d[version]:
            d[version]["released"] = now.isoformat()
        self.write(d)

    def update_interactive(self, version, description=None, changes=None):
        if not description:
            description = input(
                "Add a description for {} (ENTER to skip): ".format(version)
            )
        if isinstance(changes, str):
            changes = [c.strip() for c in changes.split(",")]
        if not changes:
            change_input = None
            if not changes:
                changes = []
                while change_input != "":
                    if change_input is not None:
                        changes.append(change_input)
                    change_input = input("Add a change (ENTER to finish): ").strip()
        self.update(version, description, changes)
