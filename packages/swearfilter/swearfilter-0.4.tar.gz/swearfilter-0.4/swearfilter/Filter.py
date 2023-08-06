class Filter:
    def DefaultFilter(self, StringName):
        UpperList = []
        WordList = ['fucker', 'arse', 'ass', 'asshole', 'bastard', 'bitch', 'bollocks', 'bugger', 'child-fucker', 'child fucker', 'Christ on a bike', 'Christ on a cracker', 'crap', 'cunt', 'damn', 'effing', 'frigger', 'fuck', 'fucking', 'shitting', 'goddamn', 'hell', 'holy shit', 'horseshit', 'Jesus fuck', 'Jesus wept', 'motherfucker', 'motherfucking', 'fucker' 'nigga', 'nigger', 'prick', 'shit', 'shit ass', 'shitass', 'slut', 'son of a bitch', 'son of a whore', 'twat', 'piss', 'cum', 'penis', 'dick', 'vagina', 'boobs', 'sex', 'tits', 'boob', 'tit', 'arsehole', 'balls', 'bullshit', 'son of a bitch', 'cock', 'dickhead', 'pussy', 'twat']
        StringSplit = StringName.split(' ')
        LIST = []
        ret = ''
        for i in StringSplit:
            if i in WordList:
                StringLength = len(i)
                NewString = '*' * StringLength
                LIST.append(NewString)
            else:
                LIST.append(i)
        for i in LIST:
            ret += i + ' '
        Filtered = ret[:-1]
        return Filtered
    
    def ConfigureFilter(self, StringName, WordList):
        UpperList = []
        StringSplit = StringName.split(' ')
        LIST = []
        ret = ''
        for i in StringSplit:
            if i in WordList:
                StringLength = len(i)
                NewString = '*' * StringLength
                LIST.append(NewString)
            else:
                LIST.append(i)
        for i in LIST:
            ret += i + ' '
        Filtered = ret[:-1]
        return Filtered
    
    def GetListLength(self, WordList):
        WordListLength = len(WordList)
        return WordListLength
    
    def PrintPremadeList(self):
        WordList = ['fucker', 'arse', 'ass', 'asshole', 'bastard', 'bitch', 'bollocks', 'bugger', 'child-fucker', 'child fucker', 'Christ on a bike', 'Christ on a cracker', 'crap', 'cunt', 'damn', 'effing', 'frigger', 'fuck', 'fucking', 'shitting', 'goddamn', 'hell', 'holy shit', 'horseshit', 'Jesus fuck', 'Jesus wept', 'motherfucker', 'motherfucking', 'fucker' 'nigga', 'nigger', 'prick', 'shit', 'shit ass', 'shitass', 'slut', 'son of a bitch', 'son of a whore', 'twat', 'piss', 'cum', 'penis', 'dick', 'vagina', 'boobs', 'sex', 'tits', 'boob', 'tit', 'arsehole', 'balls', 'bullshit', 'son of a bitch', 'cock', 'dickhead', 'pussy', 'twat']
        print(WordList)