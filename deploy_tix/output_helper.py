"""Module for formatting text output for Bugzilla comments and Jenkins
console output readability."""

LINE = '------------------'
NL = '\n'

class OutputHelper(object):

    @staticmethod
    def get_header(label):
        return '\n{}\n{}\n{}\n'.format(LINE, label, LINE)

    @staticmethod
    def get_sub_header(label):
        return '\n{}\n'.format(label)

if __name__ == '__main__':

    out = OutputHelper()
    print out.get_header('YOUR HEADER')
    print out.get_sub_header('MY_SUB_HEADER')


