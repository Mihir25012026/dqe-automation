*** Settings ***
Library    SeleniumLibrary
Library    helper.py

*** Variables ***
${REPORT_FILE}     file:///C:/PycharmProjects/dqe_automation-new/robot_framework_project/report.html
${PARQUET_FOLDER}  parquet_data/facility_type_avg_time_spent_per_visit_date
${FILTER_DATE}     2026-04-01


*** Test Cases ***
Compare HTML Table With Parquet Data
    Open Browser    ${REPORT_FILE}    chrome
    Maximize Browser Window

    Wait Until Element Is Visible    class:table

    ${html_df}=       Read Html Table

    ${parquet_df}=    Read Parquet Data    ${PARQUET_FOLDER}    ${FILTER_DATE}

    ${result}    ${diff}=    Compare Dataframes    ${html_df}    ${parquet_df}

    Run Keyword If    '${result}' == 'False'    Fail    Data mismatch found: ${diff}

    Close Browser