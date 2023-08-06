from textstat.textstat import textstatistics as TextStatistics


class TextStat(TextStatistics):
    """Over-rides the `textstatistics` class because of weirdnesses in the way it
    was written such as lack of PEP8 and not having an `init`.
    """

    def __init__(self, language=None):
        """
        :param args: :class:`argparse.Namespace` like object to populate this
            class
        """
        super(TextStat, self).__init__()
        if language:
            self.set_lang(language)
