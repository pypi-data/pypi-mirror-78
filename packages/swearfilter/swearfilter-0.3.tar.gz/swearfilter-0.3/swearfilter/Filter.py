class Filter:
    def DefaultFilter(self, StringName):
        WordList = ['arse', 'ass', 'asshole', 'bastard', 'bitch', 'bollocks', 'bugger', 'child-fucker', 'child fucker', 'Christ on a bike', 'Christ on a cracker', 'crap', 'cunt', 'damn', 'effing', 'frigger', 'fuck', 'goddamn', 'hell', 'holy shit', 'horseshit', 'Jesus fuck', 'Jesus wept', 'motherfucker', 'nigga', 'nigger', 'prick', 'shit', 'shit ass', 'shitass', 'slut', 'son of a bitch', 'son of a whore', 'twat', 'piss', 'cum', 'penis', 'dick', 'vagina', 'boobs', 'sex', 'tits', 'boob', 'tit', 'arsehole', 'balls', 'bullshit', 'son of a bitch', 'cock', 'dickhead', 'pussy', 'twat']
        if StringName in WordList:
            StringLength = len(StringName)
            NewString = '*' * StringLength
            Filtered = StringName.replace(StringName, NewString)
            return Filtered
        else:
            return StringName
    
    def ConfigureFilter(self, StringName, WordList):
        if StringName in WordList:
            StringLength = len(StringName)
            NewString = '*' * StringLength
            Filtered = StringName.replace(StringName, NewString)
            return Filtered
        else:
            return StringName
    
    def GetListLength(self, WordList):
        WordListLength = len(WordList)
        return WordListLength
    
    def PrintPremadeList(self):
        WordList = ['arse', 'ass', 'asshole', 'bastard', 'bitch', 'bollocks', 'bugger', 'child-fucker', 'child fucker', 'Christ on a bike', 'Christ on a cracker', 'crap', 'cunt', 'damn', 'effing', 'frigger', 'fuck', 'goddamn', 'hell', 'holy shit', 'horseshit', 'Jesus fuck', 'Jesus wept', 'motherfucker', 'nigga', 'nigger', 'prick', 'shit', 'shit ass', 'shitass', 'slut', 'son of a bitch', 'son of a whore', 'twat', 'piss', 'cum', 'penis', 'dick', 'vagina', 'boobs', 'sex', 'tits', 'boob', 'tit', 'arsehole', 'balls', 'bullshit', 'son of a bitch', 'cock', 'dickhead', 'pussy', 'twat']
        print(WordList)