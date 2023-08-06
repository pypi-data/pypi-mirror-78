"""
FileName: logger.py
Description: 
Time: 2020/7/28 15:18
Project: CiLog
Author: Shurui Gui
"""

import logging, os, shutil, time
from traceback import extract_stack, print_list, StackSummary
from logging.handlers import SMTPHandler

logging.IMPORTANT = 35
logging.MAIL = 60
logging.addLevelName(logging.IMPORTANT, 'IMPORTANT')
logging.addLevelName(logging.MAIL, 'MAIL')
# ------------------------------ set new levels --------------------------------
class CustomLogger(logging.Logger):

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level=logging.NOTSET)

    def important(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'IMPORTANT'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "major disaster", exc_info=1)
        """
        if self.isEnabledFor(logging.IMPORTANT):
            self._log(logging.IMPORTANT, msg, args, **kwargs)

    def mail(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'MAIL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "major disaster", exc_info=1)
        """
        if self.isEnabledFor(logging.MAIL):
            self._log(logging.MAIL, msg, args, **kwargs)


s2l = {
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'IMPORTANT': logging.IMPORTANT,
    'MAIL': logging.MAIL,
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'NOTSET': logging.NOTSET
}

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
COLORS = {
    'WARNING': YELLOW,
    'IMPORTANT': CYAN,
    'MAIL': CYAN,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': MAGENTA,
    'ERROR': RED
}


def bold_msg(message, use_color):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


class CustomFormatter(logging.Formatter):

    def __init__(self, use_color, stack_level, msg_fmt=None, file=False):
        super().__init__("%(levelno)s: %(msg)s")
        self.use_color = use_color if not file else False
        self.stack_level = stack_level
        self._stack_prune = -8 if not file else -9
        self.msg_fmt = msg_fmt or \
            {
                'DEBUG': "%(levelname)s: %(asctime)s : $BOLD%(message)s$RESET",
                'INFO': "%(levelname)s: $BOLD%(message)s$RESET",
                'WARNING': "%(levelname)s: %(filename)s - line %(lineno)d : $BOLD%(message)s$RESET",
                'IMPORTANT': "%(levelname)s: %(asctime)s : $BOLD%(message)s$RESET",
                'ERROR': "%(levelname)s: %(asctime)s - %(filename)s - line %(lineno)d : $BOLD%(message)s$RESET",
                'CRITICAL': "%(levelname)s: %(asctime)s - %(filename)s - line %(lineno)d : $BOLD%(message)s$RESET",
                'MAIL': "%(levelname)s: %(asctime)s : $BOLD%(message)s$RESET"
            }
        for key in self.msg_fmt.keys():
            self.msg_fmt[key] = bold_msg(self.msg_fmt[key], self.use_color)

    def format(self, record) -> str:

        # set for different levels
        format_orig = self._style._fmt
        self._style._fmt = self.msg_fmt[record.levelname]
        if record.levelno >= self.stack_level:
            record.stack_info = ''.join(StackSummary.from_list(extract_stack()[:self._stack_prune]).format())

        # make it colorful
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + record.levelname + RESET_SEQ
            record.levelname = levelname_color

        self.datefmt = '%m/%d/%Y %I:%M:%S %p'
        result = logging.Formatter.format(self, record)

        self._style._fmt = format_orig
        record.levelname = levelname

        return result



class FileFormatter(CustomFormatter):

    def __init__(self, stack_level, msg_fmt=None):
        __file = True
        __use_color = False
        super().__init__(__use_color, stack_level, msg_fmt=msg_fmt, file=__file)


class CustomFileHandler(logging.FileHandler):

    def __init__(self, filename, mode='a', encoding=None, delay=False):
        file = os.path.abspath(os.fspath(filename))
        file_path, file_name_ext = os.path.split(file)
        if os.path.exists(file):
            file_name, file_ext = os.path.splitext(file_name_ext)
            if len((f := open(file, 'r', encoding=encoding)).readlines()) > 1e4:
                f.close()
                shutil.copy(file,
                            os.path.join(file_path,
                                         f'{file_name}-{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}{file_ext}'))
                mode = 'w'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        super().__init__(filename, mode=mode, encoding=encoding, delay=delay)


def create_logger(**kwargs) -> logging.Logger:
    """
    Create logger for logging

    :param Require[name] : str - logger name

    :param Optional[file] : str - File path

    :param Optional[file_mode] : str - File open mode. Default: 'a'

    :param Optional[file_level] : Literal['DEBUG', 'INFO', 'WARNING', 'IMPORTANT', 'ERROR', 'CRITICAL', 'MAIL'] - Default 'INFO'

    :param Optional[enable_mail] : bool - Default False

    :param Optional[mail_level] : Literal['DEBUG', 'INFO', 'WARNING', 'IMPORTANT', 'ERROR', 'CRITICAL', 'MAIL'] - Default 'MAIL'

    :param Optional[mail_setting] : dir - Required if enable_mail == True
        {
            mailhost:   string or tuple - YourMailHost or (host, port),
            fromaddr:   string          - YourSenderAddress,
            toaddrs:    list(string)    - List of YourTargetAddresses,
            subject:    string          - Mail Subject,
            credentials:tuple           - (YourUsername, YourPassword),
            secure:     tuple           - () or (KeyfileName) or (KeyfileName, CertificatefileName)
                                            use the secure protocol (TLS),
            timeout:    float           - Default 1.0
        }
    :param Optional[use_color] : bool - Signal for using colored info. Default False

    :param Optional[stack_level] : Literal['DEBUG', 'INFO', 'WARNING', 'IMPORTANT', 'ERROR', 'CRITICAL', 'MAIL'] - Default 'ERROR'

    :param Optional[msg_fmt] : Dict{'DEBUG': debug_fmt, 'INFO': info_fmt, 'WARNING': warning_fmt, 'IMPORTANT': important_fmt,
    'ERROR': error_fmt, 'CRITICAL': critical_fmt, 'MAIL': mail_fmt} - Custom design massage format.
    Please refer to CustomFormatter and url: https://docs.python.org/3/library/logging.html#logrecord-attributes

    :return: logger : logging.Logger
    """

    if not kwargs.get('name'):
        raise Exception('param [name] must be specified.')

    kwargs['file'] = kwargs.get('file') or None
    kwargs['file_mode'] = kwargs.get('file_mode') or 'a'
    kwargs['file_level'] = s2l.get(kwargs.get('file_level') or 'INFO')
    kwargs['enable_mail'] = kwargs.get('enable_mail') or False
    kwargs['mail_level'] = s2l.get(kwargs.get('mail_level') or 'MAIL')
    kwargs['mail_setting'] = kwargs.get('mail_setting') or None
    kwargs['use_color'] = kwargs.get('use_color') or False
    kwargs['stack_level'] = s2l.get(kwargs.get('stack_level') or 'ERROR')
    kwargs['msg_fmt'] = kwargs.get('msg_fmt') or None


    # create logger
    logging.Logger.manager.setLoggerClass(CustomLogger)
    logger = logging.getLogger(kwargs['name'])
    logger.setLevel(logging.DEBUG)

    # console handler and its formatter
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    cformatter = CustomFormatter(use_color=kwargs['use_color'],
                                 stack_level=kwargs['stack_level'],
                                 msg_fmt=kwargs['msg_fmt'])
    ch.setFormatter(cformatter)
    logger.addHandler(ch)

    # file handler
    if kwargs['file']:
        fh = CustomFileHandler(kwargs['file'], mode=kwargs['file_mode'])
        fh.setLevel(kwargs['file_level'])
        fformatter = FileFormatter(stack_level=kwargs['stack_level'], msg_fmt=kwargs['msg_fmt'])
        fh.setFormatter(fformatter)
        logger.addHandler(fh)

    if kwargs['enable_mail']:
        assert not(kwargs['mail_setting'] is None) and isinstance(kwargs['mail_setting'], dict)
        setting = kwargs['mail_setting']
        mh = SMTPHandler(setting.get('mailhost'), setting.get('fromaddr'), setting.get('toaddrs'),
                         setting.get('subject'), credentials=setting.get('credentials'),
                         secure=setting.get('secure'), timeout=setting.get('timeout'))
        mh.setLevel(kwargs['mail_level'])
        mformatter = FileFormatter(stack_level=kwargs['stack_level'], msg_fmt=kwargs['msg_fmt'])
        mh.setFormatter(mformatter)
        logger.addHandler(mh)

    return logger
