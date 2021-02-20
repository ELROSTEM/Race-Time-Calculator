import pandas as pd
import streamlit as st


def method_1():
    """
    Method 1
    Algorithm to rank the schools based on brute force. Better the stats better the ranking.

    Personal opinion of accuracy based on the data shown - (8/10)
    *My personal opinion is based of the "rep" of the school.
    """ 
    # Basic Stats
    basic_stats = (
        schoolperformance["graduation_rate_2013"] + schoolperformance["graduation_rate_2014"] + schoolperformance["college_career_rate_2013"] +          schoolperformance["college_career_rate_2014"] + schoolperformance["pct_stu_enough_variety_2014"] + schoolperformance["pct_stu_safe_2014"]
    )

    # SAT
    sat_stats = (
        schoolperformance["SAT Critical Reading Avg. Score"].astype(int) + schoolperformance["SAT Math Avg. Score"].astype(int) +                        schoolperformance["SAT Writing Avg. Score"].astype(int)
    )

    #Regent
    regent_stats = (
        schoolperformance["Mean Score"]
    )

    schoolperformance["score"] = basic_stats + sat_stats + regent_stats

    return schoolperformance["score"]


def method_2():
    """
    Method 2
    Algorithm to rank the schools by average and personal opinion. This way the score doesn't solely rely on the SAT scores of students instead      it is split in a ratio. In this case the ratio is 33:33:33. The score can be considered as a numeric grade for each schools performance.

    Personal opinion of accuracy based of the data shown - (9/10)
    *My personal opinion is based of the "rep" of the school.
    """

    # Basic Stats
    basic_stats = (
            (schoolperformance["graduation_rate_2013"] + schoolperformance["graduation_rate_2014"] + schoolperformance["college_career_rate_2013"] + schoolperformance["college_career_rate_2014"] + schoolperformance["pct_stu_enough_variety_2014"] + schoolperformance["pct_stu_safe_2014"])/600
        )

    # SAT 
    sat_stats = (
        (schoolperformance["SAT Critical Reading Avg. Score"].astype(int) + schoolperformance["SAT Math Avg. Score"].astype(int) + schoolperformance["SAT Writing Avg. Score"].astype(int)) /2400
        )
    
    #Regent
    regent_stats = (
        schoolperformance["Mean Score"]/100
    )

    schoolperformance["score"] = (basic_stats + sat_stats + regent_stats)/3

    return schoolperformance["score"]



"""Preparing the data"""

# read the csv
schooldirectory = pd.read_csv("data/2016_DOE_High_School_Directory.csv")
schoolsat = pd.read_csv("data/2012_SAT_Results.csv")
schoolregent = pd.read_csv("data/2014_-_2017_Regents_modified.csv")
schoolperformance = pd.read_csv("data/2016_DOE_High_School_Performance__Directory.csv")

# Modify datasets before joining
schoolsat['Num of SAT Test Takers'] = pd.to_numeric(schoolsat['Num of SAT Test Takers'], errors='coerce')
schoolsat = schoolsat.dropna(subset=['Num of SAT Test Takers'])

schoolsat['SAT Critical Reading Avg. Score'] = pd.to_numeric(schoolsat['SAT Critical Reading Avg. Score'], errors='coerce')
schoolsat['SAT Math Avg. Score'] = pd.to_numeric(schoolsat['SAT Math Avg. Score'], errors='coerce')
schoolsat['SAT Writing Avg. Score'] = pd.to_numeric(schoolsat['SAT Writing Avg. Score'], errors='coerce')

# join data
schoolperformance = schoolperformance.join(schooldirectory.set_index('dbn'), on='dbn')
schoolperformance = schoolperformance.join(schoolsat.set_index('dbn'), on='dbn')
schoolperformance = schoolperformance.join(schoolregent.set_index('dbn'), on='dbn')
schoolperformance = schoolperformance.fillna(0)


"""Method 1"""
method_1()

# sorts the school by the score 
schoolperformance.sort_values(by=['score'], ascending=False, inplace=True)
# gets rid of the ones without data
schoolperformance_display = schoolperformance[["dbn", "school_name", "borough", "total_students", "score"]]
best_schools = schoolperformance_display.head(10)
print(best_schools)


"""Method 2"""
method_2()

# sorts the school by the score 
schoolperformance.sort_values(by=['score'], ascending=False, inplace=True)
# gets rid of the ones without data
schoolperformance_display = schoolperformance[["school_name", "borough", "total_students", "score"]]
best_schools = schoolperformance_display.head(10)
print(best_schools)
