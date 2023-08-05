def copydoc(src):
    def _(dst):
        dst.__doc__ = src.__init__.__doc__
        return dst
    return _