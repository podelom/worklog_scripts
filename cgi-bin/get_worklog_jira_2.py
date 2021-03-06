#!/usr/local/bin/python3.7

from jira import JIRA, JIRAError
import get_issues_updated_jira_2
from datetime import datetime, timedelta
import urllib3
import securer_templates


jira_auth = securer_templates.jira_credentials_1
jira = jira = JIRA(basic_auth=(jira_auth['login'], jira_auth['password']), options = {'server': jira_auth['link'], 'verify':'certs.pem'})

fullnames = {}

urllib3.disable_warnings()
def Convert_Seconds_To_Hours(str):
    hours = 0
    hours = int(str)/3600
    rhours = round(hours, 3)
    #print("rhours: ", rhours)
    return(rhours)

def Worklog_Date(d):
    source_date = d[0:10]  # - timedelta(days=days_to_subtract)
    convert_string_to_date = datetime.strptime(source_date, '%Y-%m-%d')
    date = datetime.date(convert_string_to_date)
    return(date)

def Today_Date():
    d = datetime.now()
    date = datetime.date(d)
    return(date)

def Yesterday_Date():
    today = datetime.now()
    date = datetime.date(today)
    yesterday = date - timedelta(days=1)
    return(yesterday)

def Start_Of_The_Month_Date():
    d = datetime.now()
    date = datetime.date(d)
    first_day_month = date.replace(day=1)
    return(first_day_month)

def Start_Of_The_Previous_Month_Date():
    d = datetime.now()
    date = datetime.date(d)
    previuos_month = date.replace(month=date.month - 1)
    first_day_previous_month = previuos_month.replace(day=1)
    return(first_day_previous_month)

def Get_Today_Logged_Work(person, projects):
    person_with_hours = {person: 0}
    for issue in get_issues_updated_jira_2.Get_Today_Updated_Issues(person, projects):
        try:
            for item in jira.worklogs(issue):
                worklog = jira.worklog(issue, item)
                if Worklog_Date(worklog.started) == Today_Date():
                    if  worklog.author.name == person:
                        hours = Convert_Seconds_To_Hours(worklog.timeSpentSeconds)
                        person_with_hours[person] += hours

        except JIRAError as e:
            print("FUCK OFF: ", e.status_code, e.text)
            continue
    #        print ("id: ", issue.id)
    #        print ("key: ", issue.key)
    #print("epmployees_worklog_today: ", epmployees_worklog_today)
    return(person_with_hours)

def Get_Yesterday_Logged_Work(person, projects):
    person_with_hours = {person: 0}
    for issue in get_issues_updated_jira_2.Get_Currnet_Month_Updated_Issues(person, projects):
        try:
            for item in jira.worklogs(issue):
                worklog = jira.worklog(issue, item)
                if Worklog_Date(worklog.started) == Yesterday_Date():
                    if  worklog.author.name == person:
                        hours = Convert_Seconds_To_Hours(worklog.timeSpentSeconds)
                        person_with_hours[person] += hours

        except JIRAError as e:
            print("FUCK OFF: ", e.status_code, e.text)
            continue
    #print("epmployees_worklog_yesterday: ", epmployees_worklog_yesterday)
    return(person_with_hours)

def Get_Current_Month_Logged_Work(person, projects):
    person_with_hours = {person: 0}
    for issue in get_issues_updated_jira_2.Get_Currnet_Month_Updated_Issues(person, projects):
        try:
            for item in jira.worklogs(issue):
                worklog = jira.worklog(issue, item)
                if Worklog_Date(worklog.started) >= Start_Of_The_Month_Date() and Worklog_Date(worklog.started) <= Today_Date():
                    if  worklog.author.name == person:
                        hours = Convert_Seconds_To_Hours(worklog.timeSpentSeconds)
                        person_with_hours[person] += hours

        except JIRAError as e:
            print("FUCK OFF: ", e.status_code, e.text)
            continue
    #print("epmployees_worklog_current_month: ", epmployees_worklog_current_month)
    return(person_with_hours)

def Get_Previous_Month_Logged_Work(person, projects):
    person_with_hours = {person: 0}
    for issue in get_issues_updated_jira_2.Get_Previous_Month_Updated_Issues(person, projects):
        try:
            for item in jira.worklogs(issue):
                worklog = jira.worklog(issue, item)
                if Worklog_Date(worklog.started) >= Start_Of_The_Previous_Month_Date() and Worklog_Date(worklog.started) < Start_Of_The_Month_Date():
                    if  worklog.author.name == person:
                        hours = Convert_Seconds_To_Hours(worklog.timeSpentSeconds)
                        person_with_hours[person] += hours

        except JIRAError as e:
            print("FUCK OFF: ", e.status_code, e.text)
            continue
    return(person_with_hours)


#Get_Today_Logged_Work()
#Get_Yesterday_Logged_Work()
#Get_Current_Month_Logged_Work()
#Get_Start_Of_The_Previous_Month_Date()
