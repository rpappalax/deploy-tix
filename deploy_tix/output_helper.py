"""Module for formatting text output for Bugzilla comments and Jenkins
console output readability."""

LINE = '------------------'
LINE_LONG = '------------------------------------'
LINE_DBL = '=================================================='
NL = '\n'

class OutputHelper(object):

    @staticmethod
    def get_header(label):
        return '\n{}\n{}\n{}\n'.format(LINE, label, LINE)


    @staticmethod
    def get_sub_header(label):
        return '\n{}\n'.format(label)


    @staticmethod
    def log(msg, header=False, header_dbl=False):
        """Log activity for console monitoring"""

        if header:
            line = LINE_DBL if header_dbl else LINE_LONG
            print '\n{}\n{}\n{}\n'.format(line, msg, line)
        else:
            print '{}'.format(msg)


if __name__ == '__main__':

    out = OutputHelper()
    print out.get_header('YOUR HEADER')
    print out.get_sub_header('MY_SUB_HEADER')


