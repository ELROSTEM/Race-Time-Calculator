import os

import pandas as pd
import streamlit as st


def prep_data():
    """Preparing the data"""

    # Gets working directory
    script_path = os.path.abspath(__file__)
    script_dir = os.path.split(script_path)[0]

    # read the csv
    schooldirectory = pd.read_csv(os.path.join(script_dir, "data/2016_DOE_High_School_Directory.csv"))
    schoolsat = pd.read_csv(os.path.join(script_dir, "data/2012_SAT_Results.csv"))
    schoolregent = pd.read_csv(os.path.join(script_dir, "data/2014_-_2017_Regents_modified.csv"))
    schoolperformance = pd.read_csv(os.path.join(script_dir, "data/2016_DOE_High_School_Performance__Directory.csv"))

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

    return schoolperformance

def method_1(schoolperformance):

    # Basic Stats
    basic_stats = (
        schoolperformance["graduation_rate_2013"] + schoolperformance["graduation_rate_2014"] + schoolperformance["college_career_rate_2013"] + 
        schoolperformance["college_career_rate_2014"] + schoolperformance["pct_stu_enough_variety_2014"] + schoolperformance["pct_stu_safe_2014"]
    )

    # SAT
    sat_stats = (
        schoolperformance["SAT Critical Reading Avg. Score"].astype(int) + schoolperformance["SAT Math Avg. Score"].astype(int) + 
        schoolperformance["SAT Writing Avg. Score"].astype(int)
    )

    #Regent
    regent_stats = (
        schoolperformance["Regent Mean Score"]
    )

    schoolperformance["score"] = basic_stats + sat_stats + regent_stats

    return schoolperformance["score"]

def method_2(schoolperformance):

    # Basic Stats
    basic_stats = (
            (schoolperformance["graduation_rate_2013"] + schoolperformance["graduation_rate_2014"] + schoolperformance["college_career_rate_2013"]
            + schoolperformance["college_career_rate_2014"] + schoolperformance["pct_stu_enough_variety_2014"] + 
            schoolperformance["pct_stu_safe_2014"])/600
        )

    # SAT 
    sat_stats = (
        (schoolperformance["SAT Critical Reading Avg. Score"].astype(int) + schoolperformance["SAT Math Avg. Score"].astype(int) + 
        schoolperformance["SAT Writing Avg. Score"].astype(int)) /2400
        )
    
    #Regent
    regent_stats = (
        schoolperformance["Regent Mean Score"]/100
    )

    schoolperformance["score"] = (basic_stats + sat_stats + regent_stats)/3

    return schoolperformance["score"]

def sort_data(schoolperformance, amount):
    # sorts the school by the score 
    schoolperformance.sort_values(by=['score'], ascending=False, inplace=True)
    # gets rid of the ones without data
    schoolperformance_display = schoolperformance[["dbn", "school_name", "borough", "total_students", "score"]]
    best_schools = schoolperformance_display.head(amount)
    return best_schools

schoolperformance = prep_data()

st.title("NYC Highschool Ranker")

st.markdown("### <- Please use the side bar to choose your options and click generate to generate the graph.") 

st.sidebar.title('Options')

amount = st.sidebar.slider("Select how many school to rank", 10, 100)

method = st.sidebar.selectbox("Method: ", ['Please Select','Method 1', 'Method 2'])

if(st.sidebar.button('Detail')):
    
    st.header("How everything is ranked") 

    st.text("""
        In New York City highschool applications are veiwed almost just as importantly as college
        applications. I created this app to rank the New York City highschools based off the 
        stats provided by NYC. You can find these stats here: https://opendata.cityofnewyork.us/

        The algorithms that ranks these Highschools are extremely simple however, I beleive that
        these stats acually provide an relatively accurate representation of how the schools are
        veiwed by the student body applying for highschool. 
        
        Please share this website with your friends

    """) 

    st.subheader("Cleaning The Date")

    st.text("""
        My thought process for cleaning the data was very unscientific becuase I actually don't
        know Datascience. Heres what I did, If a school had missing data anywhere the school
        was removed. This is because I thought that if the school does not have data then it was
        not valuable enough to be evaluate by the DOE.
    """)

    st.subheader("Basic") 

    st.text("""
        The basic stat is the combination of 2013 & 2014's graduation rating, 
        college carreer readiness rating, saftey rating, and variety rating.
    """)

    st.subheader("SAT")

    st.text("""
        The SAT stat is the combinaton of 2012's writing, reading, and math scores.
    """)

    st.subheader("Regent") 

    st.text("""
        The regent stat is the average of the total of every single regents a school's
        student body took between 2014 - 2017.
    """)

if(st.sidebar.button('Generate')):
    try:
        if (method == 'Method 1'):
            method_1(schoolperformance)
            st.title('Generated Table')
            st.write(sort_data(schoolperformance, amount))
            
            st.sidebar.success("Success")

            """
            Method 1
            Ranks the schools based on brute force. Better the stats better the ranking.

            Personal opinion of accuracy based on the data shown - (8/10)
            *My personal opinion is based of the "rep" of the school.
            """ 
        elif (method == 'Method 2'):
            method_2(schoolperformance)
            st.title('Generated Table')
            st.write(sort_data(schoolperformance, amount))

            st.sidebar.success("Success")

            """
            Method 2
            Ranks the schools in a ratio of 33:33:33 (SAT: Regent: Basic).
            The score can be considered as a numeric grade for each schools performance.
            This is because SAT can represent the capability of the students, regent 
            can represent the strenghth of the teachers, and basic can represent 
            the aptitude of the faculty. This means 100 percent would be a "perfect"
            school

            Personal opinion of accuracy based of the data shown - (9/10)
            *My personal opinion is based of the "rep" of the school.
            """
        
        else:
            st.sidebar.error("Incomplete")

    except:
        st.sidebar.error("Error") 

st.sidebar.subheader("Author:")

st.sidebar.write("""
    Ryan Zhang\n
    ryanzhangofficial@gmail.com
    rzhang2024@erhsnyc.net
""") 
