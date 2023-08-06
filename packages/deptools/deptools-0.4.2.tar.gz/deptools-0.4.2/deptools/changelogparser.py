'''Change Log Parser

This utility is capable of parsing Markdown files that follow the "keep a
change log" v1.0.0 format. More than one input file can be used simultaneously.
In this case, the logs are merged, but keep the dates, title and info from the
first file.

Usage:
  changelogparser version    (-i <input>)...
  changelogparser tohtml     (-i <input>)... [-p] <output>
  changelogparser tomd       (-i <input>)... [-p] <output>
  changelogparser todeb      (-i <input>)... [-p] <package_name> <output>
  changelogparser expandspec (-i <input>)... [-p] <src_spec>     <output>
  changelogparser tospec     (-i <input>)... [-p] <output>
  changelogparser -h | --help
  changelogparser --version

Commands:
  version     Prints out the version number of the program based on the inputs.
  tohtml      Converts the inputs in an HTML file
  tomd        Converts the inputs in a .md file
  todeb       Converts the inputs in a .deb file
  expandspec  Completes the .spec file passed as argument by replacing any
              instance of "@VERSION@" with the version number of the change
              log, and adding the log entries at the end of the file

Options:
  -h --help     Show this screen.
  -p            Export internal (private) entries.
  --version     Show version.

'''

from collections import defaultdict, namedtuple
from enum import Enum
import datetime
import re

from docopt import docopt

from parsimonious.exceptions import ParseError
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


class EntryType(Enum):
    '''The types of changes'''
    Added = 1
    Changed = 2
    Deprecated = 3
    Removed = 4
    Fixed = 5
    Security = 6


def public_entry_text(text):
    '''Strips any "[#NN]" part of the text'''
    return re.sub(' *\[#[0-9]+\]', '', text)

def entry_text(text, internal):
    if internal:
        return text
    else:
        return public_entry_text(text)


# Represents an entry in a change log
EntryLog = namedtuple('EntryLog', [ 
    'internal',  # type: bool
    'text',      # type: str
    ])


# A category of change logs for a given version
CategoryLog = namedtuple('CategoryLog', [
    'entry_type',  # type: EntryType
    'logs',        # type: List[EntryLog]
    ])

# A version number that follows semantic versioning
VersionNumber = namedtuple('VersionNumber', [
    'unreleased',  # type: bool
    'major',       # type: int
    'minor',       # type: int
    'patch',       # type: int
    ])

# Represents the identity of a version log (version number, 
# release date, etc.)
VersionInfo = namedtuple('VersionInfo', [
    'version',  # type: VersionNumber
    'date',     # type: datetime.date
    'yanked',   # type: bool
    ])

# List of logs for version numbers
VersionLog = namedtuple('VersionLog', [
    'info',  # type: VersionInfo
    'logs',  # type: List[CategoryLog]
    ])

# A complete change log file
ChangeLog = namedtuple('ChangeLog', [
    'title',  # type: str
    'intro',  # type: str
    'logs',   # type: List[VersionLog]
    ])

class ChangeLogRuleVisitor(NodeVisitor):
    '''Parses keepachangelog.org v1.0.0 change logs'''
    grammar = Grammar(r"""
        changelog = h1 maybe_textparagraph versionlogs
        h1 = "# " textline _
        textline = ~".+"
        versionlogs = versionlog*
        versionlog = h2 categorylogs
        h2 = ( released_h2 / unreleased_h2 )
        released_h2 = "## " version " - " date maybe_yanked _
        version = "[" number "." number "." number "]"
        date = number "-" number "-" number
        number = ~"[0-9]+"
        maybe_yanked = (~" \[YANKED\]"i)?
        unreleased_h2 = "## " ~"\[unreleased\]"i _
        categorylogs = categorylog*
        categorylog = h3 entries
        h3 = "### " word _
        word = ~"[\w]+"
        entries = entry+
        entry = "- " maybe_internal textparagraph _
        maybe_internal = (~"\[INTERNAL\]"i)?

        maybe_textparagraph = textparagraph?
        # `textparagraph` matches any text, and stops at either a dash or a
        # pound characters at the start of a line.
        textparagraph = ~"[^-#].+?((?=^-)|(?=^#)|\Z)"ms
        _ = meaningless*
        meaningless = ~"[\s]+"
        """)

    def generic_visit(self, _, __):
        pass

    def visit_maybe_textparagraph(self, node, _):
        if node.text:
            return node.text.strip()
        return ""

    def visit_textparagraph(self, node, _):
        return node.text.strip()

    def visit_maybe_internal(self, node, _):
        if node.text:
            return True
        return False

    def visit_entry(self, _, childs):
        return EntryLog(childs[1], childs[2])

    def visit_entries(self, _, childs):
        return childs

    def visit_word(self, node, _):
        return node.text

    def visit_h3(self, _, childs):
        return EntryType[childs[1]]

    def visit_categorylog(self, _, childs):
        return CategoryLog(childs[0], childs[1])

    def visit_categorylogs(self, _, childs):
        return childs

    def visit_number(self, node, _):
        return int(node.text)

    def visit_maybe_yanked(self, node, _):
        if node.text:
            return True
        return False

    def visit_unreleased_h2(self, _, __):
        return VersionInfo(
            VersionNumber(True, 0, 0, 0), datetime.date.today(), False)

    def visit_date(self, _, childs):
        return datetime.date(childs[0], childs[2], childs[4])

    def visit_version(self, _, childs):
        return VersionNumber(False, childs[1], childs[3], childs[5])

    def visit_released_h2(self, _, childs):
        return VersionInfo(childs[1], childs[3], childs[4])

    def visit_h2(self, _, childs):
        return childs[0]

    def visit_versionlog(self, _, childs):
        return VersionLog(childs[0], childs[1])

    def visit_versionlogs(self, _, childs):
        return childs

    def visit_textline(self, node, _):
        return node.text

    def visit_h1(self, _, childs):
        return childs[1]

    def visit_changelog(self, _, childs):
        return ChangeLog(childs[0], childs[1], childs[2])


def version_log_empty(vlog, output_internal=False):
    '''A version log is considered empty if it would not output any entry'''

    for categorylog in vlog.logs:
        for log in categorylog.logs:
            if not log.internal or output_internal:
                return False

    return True


def categorylogs_merge(logs):
    if not logs:
        return

    entrylogs = []
    for categorylog in logs:
        entrylogs = entrylogs + categorylog.logs

    return CategoryLog(logs[0].entry_type, entrylogs)


def versionlogs_merge(logs):
    if not logs:
        return

    # Create map from EntryType to List[CategoryLog]
    categorylogsmap = defaultdict(list)
    for versionlog in logs:
        for categorylog in versionlog.logs:
            categorylogsmap[categorylog.entry_type].append(categorylog)

    # Reduce map into List[CategoryLog]
    categorylogs = []
    for entry_type in categorylogsmap:
        categorylogs.append(categorylogs_merge(categorylogsmap[entry_type]))

    return VersionLog(logs[0].info, categorylogs)


def changelogs_merge(logs):
    if not logs:
        return

    # Create map from Version to List[VersionLog]
    versionlogsmap = defaultdict(list)
    for changelog in logs:
        for versionlog in changelog.logs:
            versionlogsmap[versionlog.info.version].append(versionlog)

    versionlogs = []
    for version in reversed(sorted(versionlogsmap)):
        versionlogs.append(versionlogs_merge(versionlogsmap[version]))

    return ChangeLog(logs[0].title, logs[0].intro, versionlogs)


def changelog_version(changelog):
    return changelog.logs[0].info.version


def version_string(version):
    if version.unreleased:
        return "Unreleased"
    return "{}.{}.{}".format(version.major, version.minor, version.patch)


def changelog_to_html(changelog, output_internal=False):
    out = """<h1>{}</h1>
<p>{}</p>\n""".format(changelog.title, changelog.intro)

    for versionlog in changelog.logs:
        ver = versionlog.info.version
        dat = versionlog.info.date
        if ver.unreleased:
            out = out + "<h2>[Unreleased]</h2>\n"
        else:
            out = out + "<h2>[{}]".format(version_string(ver))
            out = out + " - " + "{}-{}-{}".format(dat.year, dat.month, dat.day)
            out = out + "</h2>\n"

        if version_log_empty(versionlog, output_internal):
            out = out + "<ul><li>No user-visible change</li></ul>\n"
            continue

        for cat in versionlog.logs:
            out = out + "<h3>{}</h3>\n".format(cat.entry_type.name)
            out = out + "<ul>\n"
            for entry in cat.logs:
                if entry.internal and not output_internal:
                    continue
                out = out + "    <li>{}</li>\n".format(entry_text(entry.text, output_internal))
            out = out + "</ul>\n"
    return out


def changelog_to_md(changelog,
                    output_internal=False):
    out = "# {}\n\n{}\n".format(changelog.title, changelog.intro)

    for versionlog in changelog.logs:
        ver = versionlog.info.version
        dat = versionlog.info.date
        if ver.unreleased:
            out = out + "\n## [Unreleased]"
        else:
            out = out + "\n## [{}]".format(version_string(ver))
            out = out + " - " + "{:04d}-{:02d}-{:02d}".format(dat.year, dat.month, dat.day)

        if version_log_empty(versionlog, output_internal):
            out = out + "\n- No user-visible change\n"
            continue

        for cat in versionlog.logs:
            out = out + "\n### {}".format(cat.entry_type.name)
            for entry in cat.logs:
                if entry.internal:
                    if output_internal:
                        out = out + "\n- [Internal] {}".format(entry_text(entry.text, output_internal))
                else:
                    out = out + "\n- {}".format(entry_text(entry.text, output_internal))
            out = out + "\n"
    return out


def changelog_to_deb(changelog, package_name,
                     output_internal=False):
    out = ""
    for versionlog in changelog.logs:
        ver = versionlog.info.version
        dat = versionlog.info.date
        out = out + "{} ({}.{}.{}) UNRELEASED; urgency=medium\n\n".format(package_name, ver.major, ver.minor, ver.patch)

        if version_log_empty(versionlog, output_internal):
            out = out + "  * No user-visible change\n"
        else:
            for cat in versionlog.logs:
                for entry in cat.logs:
                    if entry.internal and not output_internal:
                        continue
                    out = out + "  * {}: {}\n".format(cat.entry_type.name, entry_text(entry.text, output_internal))

        out = out + "\n -- AlazarTech <support@alazartech.com>  {} 12:12:00 -0400\n\n".format(dat.strftime('%a, %d %b %Y'))
    return out


def expand_spec(changelog, input_text,
                output_internal=False):
    out = input_text.replace("@VERSION@",
                             version_string(changelog_version(changelog)))
    for versionlog in changelog.logs:
        dat = versionlog.info.date
        ver = versionlog.info.version
        out = out + "* {} AlazarTech <support@alazartech.com>\n".format(dat.strftime('%a %b %d %Y'))
        out = out + "- Version {}\n".format(version_string(ver))

        if version_log_empty(versionlog, output_internal):
            out = out + "- No user-visible change\n"
            continue

        for cat in versionlog.logs:
            for entry in cat.logs:
                if entry.internal and not output_internal:
                    continue
                out = out + "- {}: {}\n".format(cat.entry_type.name, entry_text(entry.text, output_internal))

    return out

def parse_changelog(filename):
    visitor = ChangeLogRuleVisitor()
    with open(filename, 'r') as clfile:
        return visitor.parse(clfile.read())


def main():
    arguments = docopt(__doc__, version='ChangeLog Parser')

    inputs = []
    visitor = ChangeLogRuleVisitor()
    for filename in arguments['<input>']:
        with open(filename, 'r') as clfile:
            inputs.append(visitor.parse(clfile.read()))

    changelog = changelogs_merge(inputs)

    if arguments['version']:
        print(version_string(changelog_version(changelog)))

    if arguments['tohtml']:
        output = changelog_to_html(changelog, arguments['-p'])
        with open(arguments['<output>'], 'w') as outf:
            outf.write(output)

    if arguments['tomd']:
        output = changelog_to_md(changelog, arguments['-p'])
        with open(arguments['<output>'], 'w') as outf:
            outf.write(output)

    if arguments['todeb']:
        output = changelog_to_deb(changelog, arguments['<package_name>'],
                                  arguments['-p'])
        with open(arguments['<output>'], 'w') as outf:
            outf.write(output)

    if arguments['expandspec']:
        input_text = ""
        with open(arguments['<src_spec>'], 'r') as inf:
            input_text = inf.read()

        output = expand_spec(changelog, input_text, arguments['-p'])
        with open(arguments['<output>'], 'w') as outf:
            outf.write(output)

    if arguments['tospec']:
        output = expand_spec(changelog, "", arguments['-p'])
        with open(arguments['<output>'], 'w') as outf:
            outf.write(output)


if __name__ == '__main__':
    main()
