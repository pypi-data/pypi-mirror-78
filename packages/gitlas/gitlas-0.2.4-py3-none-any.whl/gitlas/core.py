#!/usr/bin/python3
# -*- coding : UTF-8 -*-

"""

 Name        : gitlas/core\n
 Author      : Abhi-1U <https://github.com/Abhi-1U> \n
 Description : A core library of gitlas\n
 Encoding    : UTF-8\n
 Version     : 0.2.4\n
 Build       : 0.2.4/06-09-2020\n

"""

# *---------------------------------------------------------------------------*
# * MIT License
# *
# * Copyright (c) 2020 Abhi-1U <https://github.com/Abhi-1U>
# *
# * Permission is hereby granted, free of charge, to any person obtaining a copy
# * of this software and associated documentation files (the "Software"), to deal
# * in the Software without restriction, including without limitation the rights
# * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# * copies of the Software, and to permit persons to whom the Software is
# * furnished to do so, subject to the following conditions:
# *
# * The above copyright notice and this permission notice shall be included in all
# * copies or substantial portions of the Software.
# *
# * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# * SOFTWARE.
# *
# *---------------------------------------------------------------------------*

# *---------------------------------------------------------------------------*
# * RegularExpression /JSON /datetime are imported
import re
import json
import datetime as dt

# *---------------------------------------------------------------------------*


# *---------------------------------------------------------------------------*
# * This method converts the usual shorthand notation of months
# * (eg. 'Jan','Feb') into the corresponding month number with
# * leading zeros wherever required.
# *
def monthnumberSwap(monthShortHand):
    """Generates the month number based on the shorhand name of the month.
    """
    monthmanager = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }
    return monthmanager[monthShortHand]


# *---------------------------------------------------------------------------*


# *---------------------------------------------------------------------------*
# * This method returns a datetime object from the existing data
# * about date and time as indivisual data .
# *
def datetimeConvertor(date, month, year, time, timezone):
    """
    Converts raw date/time data into an object of datetime class.
    """

    Date = date + "/" + monthnumberSwap(month) + "/" + year
    Time = time + " " + timezone
    return dt.datetime.strptime(Date + " " + Time, "%d/%m/%Y %H:%M:%S %z")


# *---------------------------------------------------------------------------*


# *---------------------------------------------------------------------------*
# * Join String method is applicable in scenarios where a string needs to be
# * appended with a list/tuple of strings.
def joinString(str1, list):
    """This method joins a list of strings to a input string.\n
        returns a string object.
    """

    for i in list:
        str1 += i
        str1 + " "
    str1 + " "
    return str1


# *---------------------------------------------------------------------------*


# *---------------------------------------------------------------------------*
# * Class Commit :
# * This class is basically a data Object which serves as cleaner
# * implementation to store the commit data in a log full of commits.
class Commit:
    def __init__(self, hashid):
        self.author = None
        self.authorEmail = None
        self.comment = ""
        self.time = None
        self.date = None
        self.day = None
        self.year = None
        self.month = None
        self.timezone = None
        self.hashid = hashid
        self.isMerger = False

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError(name)

    def __delattr__(self, name):
        del self.__dict__[name]


# *---------------------------------------------------------------------------*


# *---------------------------------------------------------------------------*
# * Class Log:
# * This is the main class where the logfile is filtered ,Seperated as
# * indivisual commits and stored as Commit objects.
# * there are also methods present which mostly return dictionary objects
# * as stat reports.so calling these methods directly wont print the results.
# * You need to store them in variables first and later choose to print it out
# * or export it as JSONfiles.
class Log:

    """
    Class Log initiates with\n 
    file = path to gitlog.txt file\n
    type = usually a parameter to store the type of file the input file is.
    """

    # *-----------------------------------------------------------------------*
    # * Initializer/Constructor
    # * opens the file, seperates out each commit and stores its data in a
    # * Commit Object and these Commit Objects are listed down in the Log
    # * Object.
    # * Currently it supports multiline comments as well
    # * using the word 'commit' in comments with just two input words in it
    # * may cause the constructor to misinterpret the comment.
    # * Will Try to fix it soon. ;)
    # *
    def __init__(self, file, type):
        self.commits = []
        self.merge = []
        self.type = type
        self.filename = file
        i = -1
        with open(file, "r") as logfile:
            strings = logfile.readlines()
            for line in strings:
                data = line.split()
                if len(data) is not 0:
                    newcommit = re.match("^commit", data[0])
                    newauthor = re.match("^Author:", data[0])
                    newdate = re.match("^Date:", data[0])
                    newmerge = re.match("^Merge:", data[0])
                    if (newcommit) and (len(data) == 2):
                        i += 1
                        ncommit = Commit(hashid=data[1])
                        self.commits.append(ncommit)
                        continue
                    if newmerge:
                        self.commits[i].isMerger = True
                        setattr(self.commits[i], "Mergerhash1", data[1])
                        setattr(self.commits[i], "Mergerhash2", data[2])
                    if newauthor:
                        self.commits[i].author = joinString("", data[1:-1])
                        self.commits[i].authorEmail = data[-1]
                        continue
                    if newdate:
                        self.commits[i].day = data[1]
                        self.commits[i].month = data[2]
                        self.commits[i].date = data[3]
                        self.commits[i].time = data[4]
                        self.commits[i].year = data[5]
                        self.commits[i].timezone = data[6]
                        continue

                    else:
                        text = self.commits[i].comment
                        final = joinString(text, data)
                        self.commits[i].comment = final
                else:
                    pass

    # *-----------------------------------------------------------------------*

    # *-----------------------------------------------------------------------*
    # * These methods in this block deal with the properties of the Log
    # * Objects and hence make it easy to set/get/del attributes.
    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError(name)

    def __delattr__(self, name):
        del self.__dict__[name]

    # *-----------------------------------------------------------------------*

    # *-----------------------------------------------------------------------*
    # * These Methods in this block manage the print statement and print
    # * something about the source of Log object and its type.
    def __str__(self):
        return "Log Object for file: " + self.filename + " of Type: " + self.type

    def __repr__(self):
        pass

    __str__ == __repr__
    # *-----------------------------------------------------------------------*

    # *-----------------------------------------------------------------------*
    # * merge counts return the total merges made in the logs
    def mergeCounts(self):
        """
        Total merges in the Git Log
        """

        mergecounts = 0
        for i in self.commits:
            if i.isMerger:
                mergecounts += 1
        return mergecounts

    # *-----------------------------------------------------------------------*

    # *-----------------------------------------------------------------------*
    # * This method will calculate(more like retrieve) and store the total
    # * count of commits in a propety "TotalCommits" and also return the same.
    def commitCounts(self):
        """
        The total Count of all commits.
        """

        setattr(self, "TotalCommits", len(self.commits))
        return len(self.commits)

    # *-----------------------------------------------------------------------*

    # *-----------------------------------------------------------------------*
    # * This statistics are useful for creating bar charts of commits made on
    # * a specific day only in the entirity of the active development duration.
    # * for example i want to know which day are usually most merges handled?
    # * i can analyze the dayWise Statistics for all 7 days ,plot a chart maybe
    # * and find which day has the highest commits/merges.
    def specificWeekDayStats(self, dayname):
        """
        dayname should be shorthand string of the day eg.("Mon") 
        This one is an interesting Statistics set where i can select a specific day of
        the week and generate all counts of commits/merges throughout the entireity of the log.
        """

        commitcount = 0
        mergerscount = 0
        for i in self.commits:
            if (i.day == dayname) and (i.isMerger):
                mergerscount += 1
                commitcount += 1
                continue
            if i.day == dayname:
                commitcount += 1
                continue
        finalreport = {}
        finalreport["Commits"] = commitcount
        finalreport["Mergers"] = mergerscount
        return finalreport

    # *-----------------------------------------------------------------------*

    # *-----------------------------------------------------------------------*
    # * This metric could be controversial since the duration of git log
    # * usually does not represent the total duration of project as there may
    # * have been some development done at an earlier point and later commited.
    # * However this could also be the best shot at representing the active
    # * development period on github.
    def activeDevelopmentDuration(self):
        """
        active Development Duration is considered as the Gap between first commit and the latest commit.\n
        Hence effectively represents the duration of the project if it was abandoned long ago.
        """

        finalObj = self.commits[0]
        initialObj = self.commits[-1]
        finaldate = datetimeConvertor(
            finalObj.date,
            finalObj.month,
            finalObj.year,
            finalObj.time,
            finalObj.timezone,
        )
        initialdate = datetimeConvertor(
            initialObj.date,
            initialObj.month,
            initialObj.year,
            initialObj.time,
            initialObj.timezone,
        )
        timedelta = finaldate - initialdate
        return str(timedelta)

    # *-----------------------------------------------------------------------*

    # *-----------------------------------------------------------------------*
    # * Provides Stats of a single month of a year. simple enough
    def singleMonthStats(self, month, year):
        """
        Month name should be a shorthand name as eg.("Jan")
        Provides commit/merge counts of a specific month of a year.
        """

        if not isinstance(year, str):
            year = str(year)
        commitcount = 0
        mergerscount = 0
        for i in self.commits:
            if (i.month == month) and (i.year == year) and (i.isMerger):
                mergerscount += 1
                commitcount += 1
                continue
            if (i.month == month) and (i.year == year):
                commitcount += 1
                continue
        finalreport = {}
        finalreport["Commits"] = commitcount
        finalreport["Mergers"] = mergerscount
        return finalreport

    # *-----------------------------------------------------------------------*

    # *-----------------------------------------------------------------------*
    # * This stat is a big one the yearly stat does not only represent the
    # * total commits/merges made in a year but also the breakdown of each
    # * month is also provided.It also Highlights active months as well
    def yearStats(self, year):
        """
        Provides Monthly commit/merge counts in the whole year.\n
        also Highlights the active months and total Counts.
        """

        if not isinstance(year, str):
            year = str(year)
        commitcount = 0
        mergerscount = 0
        monthlycommitreport = {}
        monthlymergerreport = {}
        months = []
        for i in self.commits:
            if (i.month not in months) and (i.year == year):
                if (i.year == year) and (i.isMerger):
                    mergerscount += 1
                    commitcount += 1
                    months.append(i.month)
                    monthlycommitreport[i.month] = 1
                    monthlymergerreport[i.month] = 1
                    continue
                if i.year == year:
                    commitcount += 1
                    months.append(i.month)
                    monthlycommitreport[i.month] = 1
                    monthlymergerreport[i.month] = 0
                    continue
            else:
                if (i.year == year) and (i.isMerger):
                    mergerscount += 1
                    commitcount += 1
                    counts = monthlycommitreport[i.month]
                    mergers = monthlymergerreport[i.month]
                    mergers += 1
                    counts += 1
                    monthlycommitreport[i.month] = counts
                    monthlymergerreport[i.month] = mergers
                    continue
                if i.year == year:
                    commitcount += 1
                    counts = monthlycommitreport[i.month]
                    counts += 1
                    monthlycommitreport[i.month] = counts
                    continue
        finalreport = {}
        finalreport["Commits"] = commitcount
        finalreport["Mergers"] = mergerscount
        finalreport["ActiveMonths"] = months
        finalreport["MonthlyCommitReports"] = monthlycommitreport
        finalreport["MonthlyMergerReports"] = monthlymergerreport
        return finalreport

    # *-----------------------------------------------------------------------*

    # *-----------------------------------------------------------------------*
    # * This metric is really usefull in cases where the project has multiple
    # * contributers and then there is a race for finding who has the most
    # * commits/merges.
    def authorStats(self):
        """
        Provides authorwise commit/merge counts
        """

        authors = []
        authorsEmail = []
        authorcommitreport = {}
        authormergerreport = {}
        for i in self.commits:
            if i.author not in authors:
                authors.append(i.author)
                authorsEmail.append(i.authorEmail)
                authorcommitreport[i.author] = 1
                if i.isMerger:
                    authormergerreport[i.author] = 1
                else:
                    authormergerreport[i.author] = 0
                continue
            else:
                count = authorcommitreport[i.author]
                count += 1
                authorcommitreport[i.author] = count
                if i.isMerger:
                    mergers = authormergerreport[i.author]
                    mergers += 1
                    authormergerreport[i.author] = mergers
        finalreport = {}
        for i in range(len(authors)):
            authordata = {}
            authordata["Name"] = authors[i]
            authordata["Email"] = authorsEmail[i]
            authordata["Commits"] = authorcommitreport[authors[i]]
            authordata["Mergers"] = authormergerreport[authors[i]]
            finalreport["Author-" + str(i + 1)] = authordata
        return finalreport

    # *-----------------------------------------------------------------------*


# *---------------------------------------------------------------------------*
# * JSON Encoder does what it says exactly , it will convert all the objects
# * mentioned here i.e(Commit/Log Objects) are supported.
def JSONEncoder(object):
    """
    Encodes Log/CommitObject Data into the JSON format.
    However do note that only Commit/Log objects are supported.
    """

    if isinstance(object, Log):
        commit = {}
        for i in range(len(object.commits)):
            commit["commit" + str(i)] = object.commits[i].__dict__
        return commit
    if isinstance(object, dict):
        return object
    else:
        return object.__dict__


# *---------------------------------------------------------------------------*


# *---------------------------------------------------------------------------*
# * JSON Export will create a new JSON File and export the objects successfully
# * There is no need to manually encode objects as they are encoded anyways.
def JSONExport(Object, filename):
    """Exports the Object data as an JSON file to save the object permanantely.
    """

    data = JSONEncoder(Object)
    with open(filename, "w+") as outfile:
        json.dump(data, outfile)
        outfile.close()
    print("Export Of Object Data Successfull!")


# *---------------------------------------------------------------------------*


# *---------------------------------------------------------------------------*
# * This method is like a do it all "give me results now!" type .
def analyzeDataOverall(logobject, *args):
    """
    The Default year considered is the current year.
    To give a specific year as an input just pass it in parameter.
    Analyzes all data in different Parameters such as:\n
    1.Author wise Statistics
    2.Month Wise Statistics
    3.Yearly Statistics
    4.Active Development Duration
    6.Total Number of Commits
    7.Total Number of Merges
    """

    year = dt.datetime.now().year
    if len(args) != 0:
        for i in args:
            year = i
    authorStats = logobject.authorStats()
    yearStats = logobject.yearStats(str(year))
    totalduration = logobject.activeDevelopmentDuration()
    totalCommits = logobject.commitCounts()
    mergecounts = logobject.mergeCounts()
    finalreport = {}
    finalreport["Commits"] = totalCommits
    finalreport["merges"] = mergecounts
    finalreport["ActiveDevelopmentDuration"] = totalduration
    finalreport["AuthorWiseData"] = authorStats
    finalreport["yearlyReport-" + str(year)] = yearStats
    return finalreport


# *---------------------------------------------------------------------------*

# *---------------------------------------------------------------------------*
# Well done ! .You have Made it till the end of this file.
#      _______ __  __
#     / ____(_) /_/ /   ____ ______
#    / / __/ / __/ /   / __ `/ ___/
#   / /_/ / / /_/ /___/ /_/ (__  )
#   \____/_/\__/_____/\__,_/____/
# *---------------------------------------------------------------------------*
