

class ShortCutButtonModel:
    def __init__(self, iconPath, buttonText, darkIcon):
        self._darkIcon = darkIcon

        self._icon = iconPath
        self._text = buttonText

    def getDarkIcon(self):
        return self._darkIcon
    def getIcon(self):
        return self._icon
    def getText(self):
        return self._text