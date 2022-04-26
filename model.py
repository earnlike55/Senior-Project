import datetime
import os
from clean_data import clean_all, combine_matches, get_match_results_against, save_database_result, save_datbase_standing_table
from constants import CLEANED_DATA_FILE_PATH_CURRENT, CLF_FILE, CONFIDENCE_FILE, CURRENT_YEAR, DATA_PATH, FINAL_FILE, MERGE_CLEANED_DATA_FILE_PATH, MERGE_CLEANED_DATA_FILE_PATH_CURRENT, OVA_FILE_PATH, PL_FILE, PRED_RANKING_FILE, PRED_RANKING_ROUND_PATH, PRED_RANKING_ROUND_SUMMARY_FILE, PREDICTION_FILE, RAW_CLEANED_DATA_FILE_PATH, RAW_CLEANED_DATA_FILE_PATH_CURRENT, RAW_DATA_FILE_PATH, RAW_DATA_FILE_PATH_CURRENT, STANDINGS_PATH, STATISTICS_PATH, TRAIN_DATA_FILE_PATH
from current_status import add_current_details, add_current_details_all
from helpers import copy_csv, remove_directory
from match_history import get_current_fixtures, get_fixtures
from plcollect import scrape_premier_entire_season
from rankings import get_rankings, get_rankings_all
from sofifa_scraper import merge_ova_to_cleaned_all, scrape_team_ova_all
from predict import get_clf, predict_next_round


if __name__ == "__main__":
    scrape_team_ova_all(OVA_FILE_PATH, 2006, 2021)
    get_fixtures(RAW_DATA_FILE_PATH, 2006, CURRENT_YEAR)
    scrape_premier_entire_season(CURRENT_YEAR, CURRENT_YEAR, PL_FILE, RAW_DATA_FILE_PATH)
    clean_all(RAW_DATA_FILE_PATH, RAW_CLEANED_DATA_FILE_PATH, 2006, CURRENT_YEAR)
    get_rankings_all(2006, CURRENT_YEAR, RAW_CLEANED_DATA_FILE_PATH, STANDINGS_PATH)
    merge_ova_to_cleaned_all(OVA_FILE_PATH, RAW_CLEANED_DATA_FILE_PATH, MERGE_CLEANED_DATA_FILE_PATH, 2006, CURRENT_YEAR)
    copy_csv(MERGE_CLEANED_DATA_FILE_PATH, TRAIN_DATA_FILE_PATH)
    add_current_details_all(TRAIN_DATA_FILE_PATH, TRAIN_DATA_FILE_PATH, STANDINGS_PATH, 2006, CURRENT_YEAR, 2006)
    combine_matches(TRAIN_DATA_FILE_PATH, FINAL_FILE, 2006, CURRENT_YEAR)
    get_match_results_against(FINAL_FILE, TRAIN_DATA_FILE_PATH, FINAL_FILE, 2006, CURRENT_YEAR) 
    best_clf, _, best_clf_average = get_clf(FINAL_FILE, CONFIDENCE_FILE, CLF_FILE, recalculate=True )
    is_first = True
    
    remove_directory(STATISTICS_PATH)
    now = datetime.datetime.now().date().strftime('%Y-%m-%d')
    

    while True:
        is_next_round, date = predict_next_round(best_clf, FINAL_FILE, MERGE_CLEANED_DATA_FILE_PATH_CURRENT, statistics=True, stat_path=PREDICTION_FILE, first=is_first)
        if not is_next_round:
            break
        add_current_details(MERGE_CLEANED_DATA_FILE_PATH_CURRENT, CLEANED_DATA_FILE_PATH_CURRENT, STANDINGS_PATH, 2006)
        combine_matches(TRAIN_DATA_FILE_PATH, FINAL_FILE, 2006, CURRENT_YEAR)
        get_match_results_against(FINAL_FILE, TRAIN_DATA_FILE_PATH, DATA_PATH, 2006, CURRENT_YEAR)
        is_first = False

    winning_team = get_rankings(PREDICTION_FILE, PRED_RANKING_FILE, include_prediction=True)
    # save_database_result(PREDICTION_FILE)
    # save_datbase_standing_table(PRED_RANKING_FILE)