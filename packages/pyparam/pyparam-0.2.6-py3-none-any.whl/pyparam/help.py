"""Help stuff for help message"""
import sys
import re
from os import path
import colorama
import pygments
from pygments import lexers, formatters
from diot import OrderedDiot
from .defaults import (THEMES,
                       DEFAULTS,
                       OPT_POSITIONAL_NAME,
                       MAX_PAGE_WIDTH,
                       MIN_OPTDESC_LEADING,
                       MAX_OPT_WIDTH)
from .utils import wraptext

class NotAnOptionException(Exception):
    """Raises while item is not an option"""

def _match(selector, item, regex=False):
    if isinstance(selector, str):
        if regex:
            selector = re.compile(selector, re.IGNORECASE)
        elif len(selector) > 2 and selector[0] == '/' and selector[-1] == '/':
            selector = re.compile(selector[1:-1], re.IGNORECASE)

    if hasattr(selector, 'search'):
        return bool(selector.search(item[0] if isinstance(item, tuple) \
                                            else item))

    if isinstance(item, tuple):
        items = item[0].split(' | ') if ' | ' in item[0] \
                                     else item[0].split(', ')
        items = [itm.lower() for itm in items] + \
                [itm.lstrip('-').lower() for itm in items]
        return selector.lower() in items
    return selector.lower() in item.lower()

class HelpItems(list):
    """
    An item of a help message without divisions.
    For example, a line of description, usage or example.
    """
    def __init__(self, *args):
        super(HelpItems, self).__init__()
        for arg in args:
            self.add(arg)

    def add(self, item):
        """Add an item. Expected a list, if not will be .splitlines() for str.
        """
        if not isinstance(item, list):
            item = item.splitlines()
        self.extend(item)
        return self

    def query(self, selector, regex=False):
        """Get the index of the matched item"""
        for i, item in enumerate(self):
            if _match(selector, item, regex):
                return i
        raise ValueError('No element found by selector: %r' % selector)

    def after(self, selector, item, **kwargs):
        """Add an item after the item matched selector"""
        index = self.query(selector, kwargs.pop('regex', False)) + 1
        if not isinstance(item, list):
            item = item.splitlines()
        self[index:index] = item
        return self

    def before(self, selector, item, **kwargs):
        """Add an item before the item matched selector"""
        index = self.query(selector, kwargs.pop('regex', False))
        if not isinstance(item, list):
            item = item.splitlines()
        self[index:index] = item
        return self

    def replace(self, selector, content, **kwargs):
        """Replace the content of the item matching the selector"""
        index = self.query(selector, kwargs.pop('regex', False))
        self[index] = content
        return self

    def select(self, selector, **kwargs):
        """Select the content of the item matching the selector"""
        return self[self.query(selector, kwargs.pop('regex', False))]

    def delete(self, selector, **kwargs):
        """Delete the item matching the selector"""
        del self[self.query(selector, kwargs.pop('regex', False))]
        return self
    remove = delete

class HelpOptionDescriptions(HelpItems):
    """Option description in help page"""

class HelpOptions(HelpItems):
    """All options of an option section"""

    def __init__(self, *args, **kwargs):
        self.prefix = kwargs.pop('prefix', 'auto')
        super(HelpOptions, self).__init__()
        options = self._tuple_to_option(list(args))
        self.add(options)

    def _prefix_name(self, name):
        if name.startswith('-') or not self.prefix:
            return name
        if self.prefix != 'auto':
            return self.prefix + name
        return '-' + name if len(name) <= 1 or name[1] == '.' else '--' + name

    def _tuple_to_option(self, item):
        if isinstance(item, list):
            return [self._tuple_to_option(itm) for itm in item]
        if not isinstance(item, tuple) or len(item) != 3:
            raise NotAnOptionException(
                'Expect a 3-element tuple as an option item in help page.'
            )
        if not isinstance(item[2], HelpOptionDescriptions):
            return (item[0], item[1], HelpOptionDescriptions(item[2]))
        return item

    def add_param(self, param, aliases=None, ishelp=False):
        """Add a param"""
        aliases = aliases or []
        aliases.append(param.name)
        aliases = list(set(aliases))
        if param.type == 'verbose:':
            aliases[aliases.index(param.name)] = '-' + '|'.join(
                param.name * (i+1) for i in range(3))
        paramtype = '<VERBOSITY>' \
                    if param.type == 'verbose:' and len(aliases) > 1 \
                    else '' \
                    if ishelp or (param.type == 'verbose:' and
                                  len(aliases) == 1) \
                    else '[BOOL]' \
                    if param.type == 'bool:' \
                    else '' \
                    if not param.type \
                    else '<AUTO>' \
                    if param.type == 'NoneType' \
                    else '<%s>' % param.type.rstrip(':').upper()
        paramdesc = param.desc[:]
        if ishelp and paramdesc and paramdesc[-1].endswith('Default: False'):
            paramdesc[-1] = paramdesc[-1][:-14].rstrip(' ')
            if not paramdesc[-1]:
                del paramdesc[-1]
        return self.add((
            ', '.join(self._prefix_name(alias) if alias != OPT_POSITIONAL_NAME \
                                              else 'POSITIONAL'
                      for alias in sorted(aliases, key=lambda alia: (
                          0 if '|' in alia else len(alia),
                          # try to lower case first
                          [a.lower() + '1' if a.isupper() else a
                           for a in list(alia)]
                      ))),
            paramtype,
            paramdesc))

    def add_command(self, params, aliases, ishelp=False):
        """Add a set of params"""
        cmdtype = '[COMMAND]' if ishelp else ''
        return self.add((
            ' | '.join(sorted(set(aliases),
                              key=lambda alias: (len(alias), alias))),
            cmdtype,
            params['_desc'] if ishelp else params._desc
        ))

    def add(self, item, aliases=None, ishelp=False):
        # pylint: disable=arguments-differ
        from . import Param, Params
        if isinstance(item, Param):
            self.add_param(item, aliases, ishelp)
        elif isinstance(item, (dict, Params)):
            self.add_command(item, aliases, ishelp)
        elif isinstance(item, list):
            for itm in item:
                self.add(itm)
        else:
            self.append(self._tuple_to_option(item))
        self.fix_mixed()
        return self

    def insert(self, index, item):
        """Insert an item at index"""
        if isinstance(item, HelpOptions):
            self[index:index] = item
        elif isinstance(item, list):
            self[index:index] = self._tuple_to_option(item)
        else:
            self[index:index] = [self._tuple_to_option(item)]
        return self

    def after(self, selector, item, **kwargs):
        """Add an item after the item matched selector"""
        index = self.query(selector, kwargs.pop('regex', False)) + 1
        return self.insert(index, item)

    def before(self, selector, item, **kwargs):
        """Add an item before the item matched selector"""
        index = self.query(selector, kwargs.pop('regex', False))
        return self.insert(index, item)

    @property
    def is_mixed(self):
        """Tell whether options are mixed with short and long ones
        check only if first option has a short name.
        """
        firstopts = [item[0]
                     for item in self
                     if item[0].startswith('-') and '|' not in item[0]]
        if not firstopts or firstopts[0].startswith('--'):
            return False
        _, mixed = divmod(sum([opt[:2].count('-') for opt in firstopts]),
                          len(firstopts))
        return bool(mixed)

    def fix_mixed(self):
        """
        Fix indention of mixed option names
        For example, fix this:
          -o, --output <STR>     - The output file.
          --all [BOOL]           - Run all steps.
        into:
          -o, --output <STR>     - The output file.
              --all [BOOL]       - Run all steps.
        """
        if not self.is_mixed:
            return
        for i, item in enumerate(self):
            if not item[0].startswith('--'):
                continue
            #           -a, --
            self[i] = ('    ' + item[0], item[1], item[2])

class Helps(OrderedDiot):
    """All sections of help"""

    @staticmethod
    def _section(*args, **kwargs):
        if len(args) == 1 and isinstance(args[0], HelpOptions):
            return args[0]
        if len(args) == 1 and isinstance(args[0], HelpItems):
            return args[0]
        sectype = kwargs.pop('sectype', '').lower()
        if sectype == 'option':
            return HelpOptions(*args, **kwargs)
        if sectype in ('item', 'plain'):
            return HelpItems(*args, **kwargs)
        try:
            return HelpOptions(*args, **kwargs)
        except NotAnOptionException:
            return HelpItems(*args, **kwargs)

    def query(self, selector, regex=False):
        """Get the  key matching the selector"""
        for key in self:
            if _match(selector, key, regex):
                return key
        raise ValueError('No section found by selector: %r\n'
                         '- Available sections:\n  %s' % (
                             selector,
                             '\n  '.join(self.keys())
                         ))

    def select(self, selector, regex=False):
        """Select the selection of the  key matching the selector"""
        return self[self.query(selector, regex=regex)]

    def add(self, section, *args, **kwargs):
        """Add a selection"""
        sectionobj = Helps._section(*args, **kwargs)
        self[section] = sectionobj
        return self

    def before(self, selector, section, *args, **kwargs):
        """Add a section before one with titile matching selector"""
        key = self.query(selector, kwargs.pop('regex', False))
        sectionobj = Helps._section(*args, **kwargs)
        self.insert_before(key, (section, sectionobj))
        return self

    def after(self, selector, section, *args, **kwargs):
        """Add a section after one with titile matching selector"""
        key = self.query(selector, kwargs.pop('regex', False))
        sectionobj = Helps._section(*args, **kwargs)
        self.insert_after(key, (section, sectionobj))
        return self

    def delete(self, selector, regex=False):
        """Delete the section titile matching selector"""
        key = self.query(selector, regex=regex)
        del self[key]
        return self

    remove = delete

    def max_optname_width(self,
                          min_optdesc_leading=MIN_OPTDESC_LEADING,
                          max_opt_width=MAX_OPT_WIDTH):
        """Calculate the width of option name and type"""
        ret = 0

        for item in self.values():
            if not item or not isinstance(item, HelpOptions):
                continue

            # 3 = <first 2 spaces: 2> +
            #     <gap between name and type: 1> +
            itemlens = [
                len(itm[0] + itm[1]) + min_optdesc_leading + 3
                for itm in item
                if len(itm[0] + itm[1]
                       ) + min_optdesc_leading + 3 <= max_opt_width
            ]
            ret = ret if not itemlens else max(ret, max(itemlens))
        return ret or max_opt_width


class HelpAssembler:
    """A helper class to help assembling the help information page."""
    def __init__(self, prog=None, theme='default'):
        """
        Constructor
        @params:
            `prog`: The program name
            `theme`: The theme. Could be a name of `THEMES`,
                or a dict of a custom theme.
        """
        self.progname = prog or path.basename(sys.argv[0])
        self.theme = THEMES['default'].copy()
        if theme != 'default':
            self.theme.update(theme if isinstance(theme, dict) \
                                    else THEMES[theme])

    def error(self, msg, with_prefix=True):
        """
        Render an error message
        @params:
            `msg`: The error message
        """
        msg = msg.replace('{prog}', self.prog(self.progname))
        return '{colorstart}{prefix}{msg}{colorend}'.format(
            colorstart=self.theme['error'],
            prefix='Error: ' if with_prefix else '',
            msg=msg,
            colorend=colorama.Style.RESET_ALL
        )

    def warning(self, msg, with_prefix=True):
        """
        Render an warning message
        @params:
            `msg`: The warning message
        """
        msg = msg.replace('{prog}', self.prog(self.progname))
        return '{colorstart}{prefix}{msg}{colorend}'.format(
            colorstart=self.theme['warning'],
            prefix='Warning: ' if with_prefix else '',
            msg=msg,
            colorend=colorama.Style.RESET_ALL
        )

    warn = warning

    def title(self, msg, with_colon=True):
        """
        Render an section title
        @params:
            `msg`: The section title
        """
        return '{colorstart}{msg}{colorend}{colon}'.format(
            colorstart=self.theme['title'],
            msg=msg.capitalize(),
            colorend=colorama.Style.RESET_ALL,
            colon=':' if with_colon else ''
        )

    def prog(self, prog=None):
        """
        Render the program name
        @params:
            `msg`: The program name
        """
        if prog is None:
            prog = self.progname
        return '{colorstart}{prog}{colorend}'.format(
            colorstart=self.theme['prog'],
            prog=prog,
            colorend=colorama.Style.RESET_ALL
        )

    def plain(self, msg):
        """
        Render a plain message
        @params:
            `msg`: the message
        """
        msg = re.sub(r'`([^`]+)`', r'%s \1 %s' % (self.theme['codebg'],
                                                  colorama.Back.RESET),
                     msg)
        return msg.replace('{prog}', self.prog(self.progname))

    def optname(self, msg, prefix='  '):
        """
        Render the option name
        @params:
            `msg`: The option name
        """
        return '{colorstart}{prefix}{msg}{colorend}'.format(
            colorstart=self.theme['optname'],
            prefix=prefix,
            msg=msg,
            colorend=colorama.Style.RESET_ALL
        )

    def opttype(self, msg):
        """
        Render the option type or placeholder
        @params:
            `msg`: the option type or placeholder
        """
        trimmedmsg = msg.rstrip().upper()
        if not trimmedmsg:
            return msg
        return '{colorstart}{msg}{colorend}'.format(
            colorstart=self.theme['opttype'],
            msg=trimmedmsg,
            colorend=colorama.Style.RESET_ALL
        ) + ' ' * (len(msg) - len(trimmedmsg))

    def optdesc(self, msg, alldefault=False):
        """
        Render the option descriptions
        @params:
            `msg`: the option descriptions
        """
        msg = re.sub(r'`([^`]+)`', r'%s \1 %s' % (self.theme['codebg'],
                                                  colorama.Back.RESET),
                     msg)
        msg = msg.replace('{prog}', self.prog(self.progname))
        if alldefault:
            return '{colorstart}{msg}{colorend}'.format(
                colorstart=self.theme['default'],
                msg=msg,
                colorend=colorama.Style.RESET_ALL
            )

        default_index = -1
        for default in DEFAULTS:
            default_index = msg.rfind(default)
            if default_index != -1:
                break

        if default_index != -1:
            defaults = '{colorstart}{defaults}{colorend}'.format(
                colorstart=self.theme['default'],
                defaults=msg[default_index:],
                colorend=colorama.Style.RESET_ALL
            )
            msg = msg[:default_index] + defaults

        return '{colorstart}{msg}{colorend}'.format(
            colorstart=self.theme['optdesc'],
            msg=msg,
            colorend=colorama.Style.RESET_ALL
        )

    @staticmethod
    def _get_lexer_from_lang(lang):
        """Get lexer from language name"""
        # pylint: disable=no-member
        if not lang:
            return lexers.MIMELexer()

        try:
            return lexers.get_lexer_by_name(lang)
        except pygments.util.ClassNotFound:
            if '.' in lang:
                lang = lang.split('.', 1)
                lang[1] = lang[1].capitalize()
            if not lang[1].endswith('Lexer'):
                lang[1] += 'Lexer'
            try:
                lexers2 = __import__('pygments.lexers', fromlist=[lang[0]])
                return getattr(getattr(lexers2, lang[0]), lang[1])()
            except AttributeError:
                pass
            return lexers.MIMELexer()

    def _highlight_codeblock(self, lines):
        ret = []
        codeblock = dict(lang=None,
                         codes=[],
                         indent='',
                         ticks='')
        for line in lines:
            if not codeblock['ticks']:
                match = re.match(r'^(\s*)(`{3,})([\w_.]*)$', line)
                if match:
                    ret.append('__codestart__')
                    codeblock['lang'] = HelpAssembler._get_lexer_from_lang(
                        match.group(3)
                    )
                    codeblock['ticks'] = match.group(2)
                    codeblock['codes'] = []
                    codeblock['indent'] = match.group(1)
                else:
                    ret.append(line)
            elif line.strip() == codeblock['ticks']:
                # highlight
                codes = []
                maxlen = 0
                for code in codeblock['codes']:
                    if not code.startswith(codeblock['indent']):
                        raise ValueError('Codes in codeblock has different '
                                         'indentation as first line.')
                    codes.append(code[len(codeblock['indent']):])
                    maxlen = max(maxlen, len(code) - len(codeblock['indent']))
                lenspaces = [maxlen - len(code) for code in codes]
                codes = pygments.highlight(
                    '\n'.join(codes),
                    codeblock['lang'],
                    formatters.TerminalFormatter() #pylint: disable=no-member
                )
                ret.append('%s%s%s%s' % (codeblock['indent'],
                                         self.theme['codebg'],
                                         ' ' * (maxlen + 2),
                                         colorama.Back.RESET))
                ret.extend('%s%s %s%s%s%s %s' % (codeblock['indent'],
                                                 self.theme['codebg'],
                                                 line,
                                                 colorama.Back.RESET,
                                                 self.theme['codebg'],
                                                 ' ' * lenspaces[i],
                                                 colorama.Back.RESET)
                           for i, line in enumerate(codes.splitlines()))
                ret.append('%s%s%s%s' % (codeblock['indent'],
                                         self.theme['codebg'],
                                         ' ' * (maxlen + 2),
                                         colorama.Back.RESET))
                # end
                ret.append('__codeend__')
                codeblock['ticks'] = ''
                codeblock['indent'] = ''
                codeblock['codes'] = []
                codeblock['lang'] = None
            else:
                codeblock['codes'].append(line.replace('\t', '    '))
        return ret


    def assemble(self,
                 helps,
                 min_optdesc_leading=MIN_OPTDESC_LEADING,
                 max_opt_width=MAX_OPT_WIDTH):
        """
        Assemble the whole help page.
        @params:
            `helps`: The help items.
                A list with plain strings or tuples of 3 elements, which
                will be treated as option name,
                option type/placeholder and option descriptions.
            `progname`: The program name used to replace '{prog}' with.
        @returns:
            lines (`list`) of the help information.
        """
        # pylint: disable=too-many-branches,too-many-locals
        ret = []
        maxoptnamewith = helps.max_optname_width(min_optdesc_leading,
                                                 max_opt_width)

        for title, helpitems in helps.items():
            if not helpitems:
                continue
            ret.append(self.title(title))

            if not isinstance(helpitems, HelpOptions): # HelpItems
                codestart = False
                for desc in self._highlight_codeblock(helpitems):
                    if desc.strip() in ('__codestart__', '__codeend__'):
                        codestart = desc.strip() == '__codestart__'
                        continue
                    if codestart:
                        ret.append('  %s' % desc)
                        continue

                    ret.extend(self.plain(line)
                               for line in wraptext(desc,
                                                    MAX_PAGE_WIDTH,
                                                    defaults=None,
                                                    initial_indent='  '))
                ret.append('')
                continue

            # HelpOptions
            for optname, opttype, optdescs in helpitems:
                optdescs = self._highlight_codeblock(optdescs)
                descs = []
                codestart = False
                first = True
                alldefault = False
                #indent = 0
                for desc in optdescs:
                    if desc.strip() in ('__codestart__', '__codeend__'):
                        codestart = desc.strip() == '__codestart__'
                        continue
                    if codestart:
                        descs.append('%s %s' % ('-' if first else ' ',
                                                desc))
                        first = False
                        continue

                    for i, line in enumerate(wraptext(
                            desc,
                            MAX_PAGE_WIDTH - maxoptnamewith,
                            defaults=DEFAULTS
                    )):
                        descs.append(
                            #'%s%s %s' % ('-' if first and i == 0 else ' ',
                            '%s %s' % ('-' if first and i == 0 else ' ',
                                       # ' ' * indent,
                                       self.optdesc(line,
                                                    alldefault=alldefault))
                        )
                        first = False

                        if (not alldefault and
                                any(default in line for default in DEFAULTS) and
                                line.endswith(' \\')):
                            # indent = [line.rfind(default) + len(default)
                            #           for default in DEFAULTS
                            #           if default in line][-1]
                            alldefault = True
                        elif alldefault and not line.endswith(' \\'):
                            alldefault = False

                if len(optname + opttype
                       ) + min_optdesc_leading + 3 > max_opt_width:
                    ret.append('%s %s' % (
                        self.optname(optname, prefix='  '),
                        self.opttype(opttype)
                    ))
                    if descs:
                        ret.append('%s%s' % (
                            ' ' * maxoptnamewith,
                            descs.pop(0)
                        ))
                else:
                    desc = '%s %s' % (
                        self.optname(optname, prefix='  '),
                        self.opttype(opttype.ljust(
                            maxoptnamewith - len(optname) - 3
                        ))
                    )
                    desc = desc + descs.pop(0) if descs else desc
                    ret.append(desc)
                ret.extend(' ' * maxoptnamewith + line
                           for line in descs)
            ret.append('')

        ret.append('')
        return ret
