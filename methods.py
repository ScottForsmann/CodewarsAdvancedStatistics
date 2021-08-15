from data import *
from bs4 import BeautifulSoup
import requests
import json
import objectpath
from math import ceil


def waitTillContinue():
    input("Press Enter to go back to menu...")


def setDefaultUsername():
    statusCode = 0
    while statusCode != 200:
        print("What is your username (this value is case-sensitive): ", end='')
        username = input()
        url = ('https://www.codewars.com/api/v1/users/' + username)
        source = requests.get(url)
        statusCode = source.status_code
        if statusCode == 200:
            f = open('defaultUsername', 'w')
            f.write(username)
            print('Your username has been written to the defaultUsername file')
            print()
        else:
            print('Username does not exist')


def getDefaultUsername():
    f = open('defaultUsername', 'r')
    return f.read()


class PageData:

    def __init__(self):
        if getDefaultUsername() == '':
            statusCode = 0
            while statusCode != 200:
                print("What is your username (this value is case-sensitive): ", end='')
                username = input()
                self.url = ('https://www.codewars.com/api/v1/users/' + username)
                source = requests.get(self.url)
                statusCode = source.status_code
                if statusCode == 200:
                    break
                else:
                    print('Username does not exist')
        else:
            self.url = ('https://www.codewars.com/api/v1/users/' + getDefaultUsername())

        self.source = requests.get(self.url).text
        self.soup = BeautifulSoup(self.source, 'html.parser')
        self.soupXML = BeautifulSoup(self.source, 'lxml')
        self.contents = self.soup.text
        self.jsonData = json.loads(self.contents)
        self.langObject = objectpath.Tree(self.jsonData)

        # Creates a list of userLang, which has all languages user has trained
        # And one of userInvalidLang, which has all languages user has not trained
        self.userTrained = []
        self.userUntrained = []
        for lang in validLanguages:
            try:
                if self.jsonData['ranks']['languages'][lang]:
                    self.userTrained.append(lang)
            except KeyError:
                self.userUntrained.append(lang)

    def printOverallStats(self):
        print('*** Overall ***')
        print('Rank:', self.jsonData['ranks']['overall']['name'])
        print('Color:', self.jsonData['ranks']['overall']['color'])
        print('Exp:', self.jsonData['ranks']['overall']['score'])

    def printTrainedLanguages(self):
        print(','.join(self.userTrained))

    def promptLanguages(self):
        print('Your trained languages are: ', end='')
        self.printTrainedLanguages()
        if len(self.userTrained) < 2:
            separateLanguages = input(
                '\nPlease enter the languages you would like to have stats returned for separating'
                ' each with a comma.\nFor example: ' +
                self.userTrained[0] + ',fortran'
                + '\nPrompt: ')
        elif len(self.userTrained) < 6:
            separateLanguages = input(
                '\nPlease enter the languages you would like to have stats returned for separating'
                ' each with a comma.\nFor example: ' +
                ','.join(self.userTrained[0:len(self.userTrained)])
                + '\nPrompt: ')
        else:
            separateLanguages = input(
                '\nPlease enter the languages you would like to have stats returned for separating'
                ' each with a comma.\nFor example: ' +
                ','.join(self.userTrained[0:5])
                + '\nPrompt: ')
        separateLanguagesList = separateLanguages.lower().split(',')
        print()
        invalidList = []
        for lang in separateLanguagesList:
            if lang in self.userTrained:
                print('**', lang.capitalize(), '**')
                print('Rank:', self.jsonData['ranks']['languages'][lang]['name'])
                print('Color:', self.jsonData['ranks']['languages'][lang]['color'])
                print('Exp:', self.jsonData['ranks']['languages'][lang]['score'])
                print()
            elif lang in self.userUntrained:
                print('*', lang.capitalize(), '*')
                print('Rank: 8 kyu')
                print('Exp: 0')
            else:
                invalidList.append(lang)
        if len(invalidList) > 0:
            print('"', end='')
            for i in range(len(invalidList)):
                if i < len(invalidList) - 1:
                    print(invalidList[i], end=',')
                else:
                    print(invalidList[i], end='')
            if len(invalidList) > 1:
                print('" are invalid languages')
                print()
            else:
                print('" is an invalid language')
                print()

    def printAllLanguageStats(self):
        for lang in self.userTrained:
            print('**', lang.capitalize(), '**')
            print('Rank:', self.jsonData['ranks']['languages'][lang]['name'])
            print('Color:', self.jsonData['ranks']['languages'][lang]['color'])
            print('Exp:', self.jsonData['ranks']['languages'][lang]['score'])
            print()

    def overallEXPLevel(self):
        print('*** Overall ***')
        print('Rank:', self.jsonData['ranks']['overall']['name'])
        print('Color:', self.jsonData['ranks']['overall']['color'])
        print('Exp:', self.jsonData['ranks']['overall']['score'])
        print()

        validOverallRank = []
        desiredOverallRank = ''

        for rank in expTable.keys():
            if self.jsonData['ranks']['overall']['name'] == rank:
                break
            else:
                validOverallRank.append(rank)

        if int(self.jsonData['ranks']['overall']['rank']) == '2':
            print('You are max dan')
        else:
            print('Better ranks than you are: ' + ', '.join(validOverallRank))
            print()

            while desiredOverallRank not in validOverallRank:
                desiredOverallRank = input('Which rank you would like to level up to (Ex: 2 dan): ')
                if desiredOverallRank not in validOverallRank:
                    print('ERROR:', desiredOverallRank, 'is not a valid rank. Please try again')

            print()
            expUntilOverallRankUp = expTable[desiredOverallRank] - self.jsonData['ranks']['overall']['score']
            print('EXP until', desiredOverallRank + ':', expUntilOverallRankUp)
            print()
            for kyu in awardedExp.keys():
                print(kyu + ' challenges until', desiredOverallRank + ':',
                      ceil(expUntilOverallRankUp / awardedExp[kyu]))

    def specificEXPLevel(self):
        print('Your trained languages are: ', end='')
        self.printTrainedLanguages()

        separateLanguages = input('\nPlease enter the languages you would like to have stats returned for separating'
                                  ' each with a comma. For example(cpp,python): ')
        languageList = separateLanguages.split(',')
        invalidList = []

        for lang in languageList:
            lang = lang.lower()
            try:
                if self.jsonData['ranks']['languages'][lang]:
                    print('')
                    print('**', lang.capitalize(), '**')
                    print('Rank:', self.jsonData['ranks']['languages'][lang]['name'])
                    print('Color:', self.jsonData['ranks']['languages'][lang]['color'])
                    print('Exp:', self.jsonData['ranks']['languages'][lang]['score'])
                    print()

                    validSpecificRank = []
                    desiredSpecificRank = ''

                    for rank in expTable.keys():
                        if self.jsonData['ranks']['languages'][lang]['name'] == rank:
                            break
                        else:
                            validSpecificRank.append(rank)

                    if int(self.jsonData['ranks']['languages'][lang]['rank']) == '2':
                        print('You are max dan')
                        print()
                    else:
                        print('Better ranks than you are: ' + ', '.join(validSpecificRank))
                        print()
                        while desiredSpecificRank not in validSpecificRank:
                            desiredSpecificRank = input('Which rank you would like to level up to (Ex: 2 dan): ')
                            if desiredSpecificRank not in validSpecificRank:
                                print('ERROR:', desiredSpecificRank, 'is not a valid rank. Please try again')

                        expUntilSpecificRankUp = \
                            expTable[desiredSpecificRank] - self.jsonData['ranks']['languages'][lang]['score']
                        print()
                        print('EXP until', desiredSpecificRank + ':', expUntilSpecificRankUp)
                        print()
                        for kyu in awardedExp.keys():
                            print(kyu, lang, "challenges until", desiredSpecificRank + ":",
                                  ceil(expUntilSpecificRankUp / awardedExp[kyu]))
                        print()

            except KeyError:
                invalidList.append(lang)
        if len(invalidList) > 0:
            print('ERROR: "', end='')
            for i in range(len(invalidList)):
                if i < len(invalidList) - 1:
                    print(invalidList[i], end=',')
                else:
                    print(invalidList[i], end='')
            if len(invalidList) > 1:
                print('" are invalid languages')
                print()
            else:
                print('" is an invalid language')
                print()
