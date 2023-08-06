__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

import pandas
import os
import numpy
from typing import Dict, List, Tuple, Any
from functools import reduce
from erlab_coat.meta import *
from datetime import date, timedelta
import us
import gc
import itertools


def state_abbreviator(x, string_for_bad: str = None):
    if x == 'District of Columbia':
        return 'DC'
    else:
        try:
            return us.states.lookup(x).abbr
        except Exception as e:
            if str is None:
                raise e
            else:
                return string_for_bad


def remove_county_word(x):
    if x.lower().endswith(' county') or x.lower().endswith(' parish'):
        return x[:-7]
    else:
        return x


def prepare_google_mobility_data(dataframe_path):
    google_mobility_df = pandas.read_csv(
        dataframe_path)
    google_mobility_df = google_mobility_df[google_mobility_df['country_region_code'] == 'US']
    google_mobility_df = google_mobility_df[google_mobility_df['sub_region_1'].isin(state_abbreviations.keys())]
    google_mobility_df.dropna(inplace=True)

    google_mobility_df['sub_region_1'] = google_mobility_df['sub_region_1'].apply(lambda x: state_abbreviator(x, 'bad'))
    google_mobility_df = google_mobility_df[~(google_mobility_df['sub_region_1'] == 'bad')]
    google_mobility_df['sub_region_2'] = google_mobility_df['sub_region_2'].apply(lambda x: remove_county_word(x))

    google_mobility_df.rename({
        'sub_region_1': 'state',
        'sub_region_2': 'county',
        'date': 'confirmed_date',
        'retail_and_recreation_percent_change_from_baseline': 'google_mobility_retail_and_recreation_percent_change_from_baseline',
        'grocery_and_pharmacy_percent_change_from_baseline': 'google_mobility_grocery_and_pharmacy_percent_change_from_baseline',
        'parks_percent_change_from_baseline': 'google_mobility_parks_percent_change_from_baseline',
        'transit_stations_percent_change_from_baseline': 'google_mobility_transit_stations_percent_change_from_baseline',
        'workplaces_percent_change_from_baseline': 'google_mobility_workplaces_percent_change_from_baseline',
        'residential_percent_change_from_baseline': 'google_mobility_residential_percent_change_from_baseline'
    }, axis=1, errors='raise', inplace=True)

    google_mobility_df = add_day_of_the_year_to_cases_table(google_mobility_df)
    google_mobility_df.drop(columns=['country_region_code', 'country_region', 'confirmed_date'], inplace=True)

    google_mobility_df['compliance'] = google_mobility_df[
                                           'google_mobility_retail_and_recreation_percent_change_from_baseline'].copy() + \
                                       google_mobility_df[
                                           'google_mobility_grocery_and_pharmacy_percent_change_from_baseline'].copy() + \
                                       google_mobility_df[
                                           'google_mobility_parks_percent_change_from_baseline'].copy() + \
                                       google_mobility_df[
                                           'google_mobility_transit_stations_percent_change_from_baseline'].copy() + \
                                       google_mobility_df[
                                           'google_mobility_workplaces_percent_change_from_baseline'].copy() + \
                                       google_mobility_df[
                                           'google_mobility_residential_percent_change_from_baseline'].copy()

    google_mobility_df['compliance'] *= (1. / 6.0)
    google_mobility_df['compliance'] = google_mobility_df['compliance'].apply(lambda x: -1 - (x - (100.0)) / 100.0)

    return google_mobility_df


def prepare_cdc_data(path_to_cdc_repo: str, max_day: int) -> pandas.DataFrame:
    # - covid-19 hospitalization data ----------

    age_groups = {
        'ag0_4': '0-4 yr',
        'ag18_49': '18-49 yr',
        'ag5_17': '5-17 yr',
        'ag50_64': '50-64 yr',
        'ag65p': '65+ yr',
        'ag65_74': '65-74 yr',
        'ag75_84': '75-84 yr',
        'ag85p': '85+',
        'agoverall': 'Overall'
    }

    change_mmwr_to_date = lambda x: str(date(2020, 3, 7) + timedelta(days=7 * (x - 10)))
    covid_hospitalizations = {
        state_abbreviator(e.split('.')[0].split('_')[-2]): pandas.read_csv(
            os.path.join(path_to_cdc_repo, 'covid_hospitalizations', e), skiprows=2).iloc[:-15, :]
        for e in os.listdir(os.path.join(path_to_cdc_repo, 'covid_hospitalizations')) if
        ((not e.split('.')[0].split('_')[-2] == 'Entire Network') and e.endswith('.csv'))
    }

    covid_hospitalizations_df = pandas.concat(covid_hospitalizations.values())
    covid_hospitalizations_df.dropna(inplace=True)
    covid_hospitalizations_df['MMWR-WEEK'] = covid_hospitalizations_df['MMWR-WEEK'].apply(change_mmwr_to_date)
    covid_hospitalizations_df.rename({
        'CATCHMENT': 'state',
        'WEEKLY RATE ': 'state_weekly_covid_hospitalization_rate_per_100k',
        'CUMULATIVE RATE': 'state_cumulative_covid_hospitalization_rate_per_100k',
        'AGE CATEGORY': 'state_covid_hospitalization_age_category',
        'MMWR-YEAR': 'state_covid_hospitalization_year',
        'MMWR-WEEK': 'confirmed_date'
    }, axis=1, errors='raise', inplace=True)

    covid_hospitalizations_df['state'] = covid_hospitalizations_df['state'].apply(state_abbreviator)
    covid_hospitalizations_df.drop(columns=['NETWORK', 'state_covid_hospitalization_year', 'YEAR'], inplace=True)
    covid_hospitalizations_df = add_day_of_the_year_to_cases_table(covid_hospitalizations_df)
    covid_hospitalizations_df['location'] = covid_hospitalizations_df['state'].copy()

    dfs_to_be_merged = []
    for key in age_groups:
        val = age_groups[key]
        tmp = covid_hospitalizations_df[
            covid_hospitalizations_df['state_covid_hospitalization_age_category'] == val].copy()
        tmp.rename({
            'state_weekly_covid_hospitalization_rate_per_100k': 'state_weekly_covid_hospitalization_rate_per_100k_' + key,
            'state_cumulative_covid_hospitalization_rate_per_100k': 'state_cumulative_covid_hospitalization_rate_per_100k_' + key
        }, axis=1, errors='raise', inplace=True)
        tmp.drop(columns=['state_covid_hospitalization_age_category'], inplace=True)
        dfs_to_be_merged.append(tmp)

    covid_hospitalizations_df = reduce(
        lambda left, right: pandas.merge(left, right, on=['day_of_the_year', 'location', 'state', 'confirmed_date'],
                                         left_index=False, right_index=False, how='inner'), dfs_to_be_merged)
    del dfs_to_be_merged
    covid_hospitalizations_df = interpolate_by_location(covid_hospitalizations_df, max_day=max_day)
    assert covid_hospitalizations_df.isna().sum().sum() == 0, "nan values are sighted in cdc covid hospitalization data - issue"

    # -------------------------

    # - national influenza surveys --------
    influenza_activity_level_df = pandas.read_csv(
        os.path.join(path_to_cdc_repo, 'weekly_influenza_surveillance/influenza_survey.csv'))
    influenza_activity_level_df = influenza_activity_level_df.loc[:, ['STATENAME', 'ACTIVITY LEVEL', 'WEEK']]
    influenza_activity_level_df.rename({
        'STATENAME': 'state',
        'ACTIVITY LEVEL': 'state_infleunza_activity_level',
        'WEEK': 'confirmed_date'
    }, axis=1, errors='raise', inplace=True)

    influenza_activity_level_df['state'] = influenza_activity_level_df['state'].apply(
        lambda x: state_abbreviator(x, 'bad'))
    influenza_activity_level_df = influenza_activity_level_df[~(influenza_activity_level_df['state'] == 'bad')]

    def week_to_date_cdc(x: int):
        return str(date(2020, 1, 4) + timedelta(days=(x - 1)))

    influenza_activity_level_df['confirmed_date'] = influenza_activity_level_df['confirmed_date'].apply(
        week_to_date_cdc)
    influenza_activity_level_df = add_day_of_the_year_to_cases_table(influenza_activity_level_df)

    influenza_activity_level_df['state_infleunza_activity_level'] = influenza_activity_level_df[
        'state_infleunza_activity_level'].apply(lambda x: float(x.split(' ')[1]))

    influenza_activity_level_df['location'] = influenza_activity_level_df['state'].copy()
    influenza_activity_level_df = interpolate_by_location(influenza_activity_level_df, max_day=max_day)
    influenza_activity_level_df.drop(columns=['confirmed_date', 'location'], inplace=True)
    cdc_covid_df = pandas.merge(left=covid_hospitalizations_df, right=influenza_activity_level_df,
                                on=['state', 'day_of_the_year'], how='outer')

    return cdc_covid_df


def get_cdc_data(path_to_cdc_repo: str) -> pandas.DataFrame:
    # - covid-19 hospitalization data ----------

    age_groups = {
        'ag0_4': '0-4 yr',
        'ag18_49': '18-49 yr',
        'ag5_17': '5-17 yr',
        'ag50_64': '50-64 yr',
        'ag65p': '65+ yr',
        'ag65_74': '65-74 yr',
        'ag75_84': '75-84 yr',
        'ag85p': '85+',
        'agoverall': 'Overall'
    }

    change_mmwr_to_date = lambda x: str(date(2020, 3, 7) + timedelta(days=7 * (x - 10)))
    covid_hospitalizations = {
        state_abbreviator(e.split('.')[0].split('_')[-2]): pandas.read_csv(
            os.path.join(path_to_cdc_repo, 'covid_hospitalizations', e), skiprows=2).iloc[:-15, :]
        for e in os.listdir(os.path.join(path_to_cdc_repo, 'covid_hospitalizations')) if
        ((not e.split('.')[0].split('_')[-2] == 'Entire Network') and e.endswith('.csv'))
    }

    covid_hospitalizations_df = pandas.concat(covid_hospitalizations.values())
    covid_hospitalizations_df.dropna(inplace=True)
    covid_hospitalizations_df['MMWR-WEEK'] = covid_hospitalizations_df['MMWR-WEEK'].apply(change_mmwr_to_date)
    covid_hospitalizations_df.rename({
        'CATCHMENT': 'state',
        'WEEKLY RATE ': 'state_weekly_covid_hospitalization_rate_per_100k',
        'CUMULATIVE RATE': 'state_cumulative_covid_hospitalization_rate_per_100k',
        'AGE CATEGORY': 'state_covid_hospitalization_age_category',
        'MMWR-YEAR': 'state_covid_hospitalization_year',
        'MMWR-WEEK': 'confirmed_date'
    }, axis=1, errors='raise', inplace=True)

    covid_hospitalizations_df['state'] = covid_hospitalizations_df['state'].apply(state_abbreviator)
    covid_hospitalizations_df.drop(columns=['NETWORK', 'state_covid_hospitalization_year', 'YEAR'], inplace=True)
    covid_hospitalizations_df = add_day_of_the_year_to_cases_table(covid_hospitalizations_df)
    covid_hospitalizations_df['location'] = covid_hospitalizations_df['state'].copy()

    dfs_to_be_merged = []
    for key in age_groups:
        val = age_groups[key]
        tmp = covid_hospitalizations_df[
            covid_hospitalizations_df['state_covid_hospitalization_age_category'] == val].copy()
        tmp.rename({
            'state_weekly_covid_hospitalization_rate_per_100k': 'state_weekly_covid_hospitalization_rate_per_100k_' + key,
            'state_cumulative_covid_hospitalization_rate_per_100k': 'state_cumulative_covid_hospitalization_rate_per_100k_' + key
        }, axis=1, errors='raise', inplace=True)
        tmp.drop(columns=['state_covid_hospitalization_age_category'], inplace=True)
        dfs_to_be_merged.append(tmp)

    covid_hospitalizations_df = reduce(
        lambda left, right: pandas.merge(left, right, on=['day_of_the_year', 'location', 'state', 'confirmed_date'],
                                         left_index=False, right_index=False, how='inner'), dfs_to_be_merged)
    del dfs_to_be_merged
    assert covid_hospitalizations_df.isna().sum().sum() == 0, "nan values are sighted in cdc covid hospitalization data - issue"

    # -------------------------

    # - national influenza surveys --------
    influenza_activity_level_df = pandas.read_csv(
        os.path.join(path_to_cdc_repo, 'weekly_influenza_surveillance/influenza_survey.csv'))
    influenza_activity_level_df = influenza_activity_level_df.loc[:, ['STATENAME', 'ACTIVITY LEVEL', 'WEEK']]
    influenza_activity_level_df.rename({
        'STATENAME': 'state',
        'ACTIVITY LEVEL': 'state_infleunza_activity_level',
        'WEEK': 'confirmed_date'
    }, axis=1, errors='raise', inplace=True)

    influenza_activity_level_df['state'] = influenza_activity_level_df['state'].apply(
        lambda x: state_abbreviator(x, 'bad'))
    influenza_activity_level_df = influenza_activity_level_df[~(influenza_activity_level_df['state'] == 'bad')]

    def week_to_date_cdc(x: int):
        return str(date(2020, 1, 4) + timedelta(days=(x - 1)))

    influenza_activity_level_df['confirmed_date'] = influenza_activity_level_df['confirmed_date'].apply(
        week_to_date_cdc)
    influenza_activity_level_df = add_day_of_the_year_to_cases_table(influenza_activity_level_df)

    influenza_activity_level_df['state_infleunza_activity_level'] = influenza_activity_level_df[
        'state_infleunza_activity_level'].apply(lambda x: float(x.split(' ')[1]))

    influenza_activity_level_df['location'] = influenza_activity_level_df['state'].copy()

    return covid_hospitalizations_df, influenza_activity_level_df


def preprocess_dataset_further(
        df: pandas.DataFrame
) -> pandas.DataFrame:
    """
    The :func:`preprocess_dataset_further` takes care of further preprocessings such as normalizing election results.

    Parameters
    ----------
    df: `pandas.DataFrame`, required
        The input dataframe

    Returns
    ----------
    The now modified output dataframe which is an instance of `pandas.DataFrame`.
    """
    tmp = (df['democrat'] + df['republican'] + df['other']).copy()
    df.loc[~(tmp == 0), 'democrat_percentage'] = df.loc[~(tmp == 0), 'democrat'].copy() / tmp[~(tmp == 0)]
    df.loc[~(tmp == 0), 'republican_percentage'] = df.loc[~(tmp == 0), 'republican'].copy() / tmp[~(tmp == 0)]
    df.loc[~(tmp == 0), 'other_than_democrat_or_republican_percentage'] = df.loc[~(tmp == 0), 'other'].copy() / tmp[
        ~(tmp == 0)]
    df['democrat_percentage'] *= (~(tmp == 0))
    df['republican_percentage'] *= (~(tmp == 0))
    df['other_than_democrat_or_republican_percentage'] *= (~(tmp == 0))

    tmp = (df['number_of_men'] + df['number_of_women']).copy()
    df.loc[~(tmp == 0), 'men_percentage'] = df.loc[~(tmp == 0), 'number_of_men'].copy() / tmp[~(tmp == 0)]
    df.loc[~(tmp == 0), 'women_percentage'] = df.loc[~(tmp == 0), 'number_of_women'].copy() / tmp[~(tmp == 0)]
    df['men_percentage'] *= (~(tmp == 0))
    df['women_percentage'] *= (~(tmp == 0))

    df['normalized_voting_age_citizens'] = df['voting_age_citizens'].copy() / df['total_population'].copy()

    tmp = df['ALAND_SQMI'].copy()
    df['population_density'] = tmp.copy()
    df[(tmp > 0) & (~tmp.isna())]['population_density'] = df[(tmp > 0) & (~tmp.isna())]['total_population'] / tmp[
        (tmp > 0) & (~tmp.isna())]
    df['population_density'] *= (tmp > 0) & (~tmp.isna())
    df = make_state_county_composite_index(df)
    return df


def make_state_county_composite_index(
        df: pandas.DataFrame
) -> pandas.DataFrame:
    """
    The :func:`make_state_county_composite_index` takes care of creating and adding the composite index of
    state and county to the dataframe.

    Parameters
    ----------
    df: `pandas.DataFrame`, required
        The input dataframe

    Returns
    ----------
    The now modified output dataframe which is an instance of `pandas.DataFrame`.
    """
    df['location'] = df['county'] + "_" + df['state']
    return df


def merge_all_dfs_in_dict(in_dict: Dict[str, pandas.DataFrame]) -> pandas.DataFrame:
    """
    The :func:`merge_all_dfs_in_dict` is for merging all the dataframes in a dict by their indexes.

    Parameters
    ----------
    in_dict: `Dict[str, pandas.DataFrame])`, required
        The input dictionary of dataframes

    Returns
    ----------
    The output dataframe will be returned.
    """
    state_table = None
    for key in in_dict.keys():
        if state_table is None:
            state_table = in_dict[key].copy()
        else:
            tmp1 = state_table.copy()
            tmp2 = in_dict[key].copy()
            state_table = pandas.merge(right=tmp1, left=tmp2, how="outer", left_index=True, right_index=True).copy()
            tmp1 = None
            tmp2 = None
    return state_table


def interpolate_by_location(df: pandas.DataFrame, column_to_interpolate_on: str = 'day_of_the_year',
                            max_day: int = None) -> pandas.DataFrame:
    """
    The :func:`interpolate_by_location` helps with interpolating the values between the first and last
    day of events for our dataframes to have more consistent COVID-19 information.

    Parameters
    ----------
    df: `pandas.DataFrame`, required
        The main pandas dataframe that is loaded.

    column_to_interpolate_on: `str`, required
        In COVID-19 case it is usually the day of the year column

    max_day: `int`, optional (default=None)
        If set, everything will be interpolated by then

    Returns
    -----------
    This method returns the now modified dataframe
    """
    df_nans = df[df[column_to_interpolate_on].isna()].copy()
    df = df[~(df[column_to_interpolate_on].isna())].copy()

    if 'location' not in df.columns.tolist():
        df['location'] = (df['county'] + '_' + df['state']).copy()
        if df_nans.shape[0] > 0:
            df_nans['location'] = (df_nans['county'] + '_' + df_nans['state']).copy()
    # df.reset_index(inplace=True)
    df.sort_values(by=['location', 'day_of_the_year'], inplace=True)
    min_day = int(df['day_of_the_year'].min())
    if max_day is None:
        max_day = int(df['day_of_the_year'].max())
    unique_locations = df['location'].unique().tolist()
    rows_to_concat = []

    df.sort_values(by=['location', 'day_of_the_year'], inplace=True)
    good_columns = df.columns.tolist()
    df['locdoy_index'] = df['day_of_the_year'].apply(lambda x: str(int(x))).copy() + '_' + df['location'].copy()
    df.set_index('locdoy_index', inplace=True)

    for location in unique_locations:
        prev_row = None
        tmp = df[df['location'] == location].copy()
        days_that_we_have_data_for = set(tmp['day_of_the_year'].tolist())
        if tmp.shape[0] == 0:
            continue
        first_day_in_location = int(tmp.iloc[0, :]['day_of_the_year'])
        for day in range(first_day_in_location, max_day + 1):
            if day not in days_that_we_have_data_for:
                row_to_cat = prev_row.copy()
                row_to_cat['day_of_the_year'] = day
                for column in row_to_cat.keys():
                    if (column in ['confirmed_count', 'death_count']) or column.startswith(
                            'state_weekly_covid_hospitalization_rate_per'):
                        row_to_cat[column] = 0
                rows_to_concat.append(row_to_cat.copy())
            else:
                prev_row = tmp.loc[str(day) + '_' + location, good_columns].copy()
                if len(prev_row.shape) > 1:
                    prev_row = prev_row.iloc[0, :]

    df.reset_index(inplace=True, drop=True)

    df = pandas.concat([df.reset_index(drop=True).copy(), pandas.concat(rows_to_concat, axis=1, ignore_index=True).T],
                       ignore_index=True).reset_index(drop=True)

    if df_nans.shape[0] > 0:
        df = pandas.concat([df, df_nans])

    df.sort_values(by=['location', 'day_of_the_year'], inplace=True)

    return df


def combine_dynamic_and_static_datasets(
        path_to_erlab_glance: str,
        operation: str = 'static',  # options: dynamic
        interpolate_in_days: bool = False
) -> pandas.DataFrame:
    """
    The :func:`combine_dynamic_and_static_datasets` combines the static datasets including the state regions
    mentioned in our article with the dynamically changing datasets (commute and covid-19) to form the
    dataframes.

    Parameters
    ----------
    commute_dataset_filepath: `str`, required
        The filepath for the dataset

    cases_dataset_filepath: `str`, required
        The filepath for the dataset

    us_region_features_filepath: `str`, required
        The filepath for the dataset

    interpolate_in_days: `bool`, optional (default=False)
        If this is true, the values will be interpolated for days. Be cautious that in the cases
        of static plots this might lead to invalid interpretations (you do not want to add new cases
        to the dates with no new cases, but for animation, this helps smoothing the frames)

    Returns
    ----------
    The new dataframe will be returned.
    """
    assert operation in ['dynamic', 'static'], "unknown operation is requested"

    # - creating the paths ------
    createUSHighResCOVID19SpreadDB(path_to_erlab_glance)
    commute_dataset_filepath = os.path.join(path_to_erlab_glance, 'resolution/county/google_mobility.csv')
    cases_dataset_filepath = os.path.join(path_to_erlab_glance, 'resolution/county/cases.csv')
    us_region_features_filepath = os.path.join(path_to_erlab_glance,
                                               'resolution/county/USHighResCOVID19SpreadDB.csv')
    cdc_repo = os.path.join(path_to_erlab_glance, 'resolution/state/cdc_covid/')
    restaurant_business_filepath = os.path.join(path_to_erlab_glance, 'resolution/state/restaurant_business.csv')

    us_region_features = pandas.read_csv(us_region_features_filepath).drop(columns=['Unnamed: 0'])

    if operation == 'dynamic':
        us_region_features.set_index(['county', 'state'], inplace=True)
        cases = pandas.read_csv(cases_dataset_filepath)
        cases.rename({
            'state_name': 'state',
            'county_name': 'county'
        }, inplace=True, axis="columns", errors="raise")
        cases = add_cumsums_to_cases_table(cases)
        cases = add_day_of_the_year_to_cases_table(cases)
        cases.set_index(['county', 'state'], inplace=True)
        full = pandas.merge(right=cases, left=us_region_features, how="outer", left_index=True, right_index=True).copy()
        full['normalized_confirmed_count_cumsum'] = 1000.0 * full['confirmed_count_cumsum'] / full['total_population']
        full['normalized_death_count_cumsum'] = 1000.0 * full['death_count_cumsum'] / full['total_population']
        full['normalized_recovered_count_cumsum'] = 1000.0 * full['recovered_count_cumsum'] / full['total_population']
        full['confirmed_count_cumsum_per100k'] = 100000.0 * full['confirmed_count_cumsum'] / full['total_population']
        full['death_count_cumsum_per100k'] = 100000.0 * full['death_count_cumsum'] / full['total_population']
        full['recovered_count_cumsum_per100k'] = 100000.0 * full['recovered_count_cumsum'] / full['total_population']

        # cdc data on covid-19
        cdc_covid_df = prepare_cdc_data(cdc_repo, max_day=int(full.day_of_the_year.max()))
        cdc_covid_df.drop(columns=['location', 'confirmed_date'], inplace=True)

        full = pandas.merge(right=full.reset_index(), left=cdc_covid_df, how="right",
                            on=['state', 'day_of_the_year']).copy()
        full = pandas.merge(right=full, left=pandas.read_csv(restaurant_business_filepath), how='right',
                            on=['state']).copy()

        commute = prepare_google_mobility_data(commute_dataset_filepath)
        full = pandas.merge(right=full, left=commute, how='right',
                            on=['state', 'county', 'day_of_the_year']).copy()

    else:
        full = us_region_features.copy()

    full = full[full.state.isin(state_abbreviations.values())]
    full = add_location_to_df(full)

    # keeping the nans # full.fillna(0, inplace=True)
    if interpolate_in_days:
        full_interpolated = interpolate_by_location(full.copy())

        return full, full_interpolated
    else:
        return full


def add_prefix_to_df_columns(df: pandas.DataFrame, prefix: str) -> pandas.DataFrame:
    """
    Adding prefix to the columns using this method.

    Parameters
    ----------
    df: `pandas.DataFrame`, required
        The input dataframe

    Returns
    ----------
    The resulting dataframe will be returned.
    """
    for column in df.columns.tolist():
        df.rename({column: prefix + "_" + column}, inplace=True, axis="columns", errors="raise")
    return df


def parse_erlab_covid19_glance_collection(collection_path: str) -> Dict[str, Dict[str, pandas.DataFrame]]:
    """
    The :func:`parse_erlab_covid19_glance_collection` parses and loads ERLab's collection of US counties and
    COVID-19 outbreak.

    Parameters
    ----------
    collection_path: `str`, required
        The path to the directory of collection, which is produced by the extraction of the file you have downloaded.

    Returns
    ----------
    The output is of `Dict[str, Dict[str, pandas.DataFrame]]`, and is composed of information both for counties and states
    along with needed metadata.
    """
    collection_path = os.path.abspath(collection_path)
    output = {
        'state': dict(),
        'county': dict(),
        'meta': dict()
    }
    for key in output.keys():
        tmp_path = os.path.join(collection_path, 'resolution', key)
        files = [e for e in os.listdir(tmp_path) if (e.endswith('.csv')) and (not e.startswith('.'))]
        for file in files:
            try:
                output[key][file.split('.')[0]] = pandas.read_csv(os.path.join(tmp_path, file))
            except Exception as e:
                output[key][file.split('.')[0]] = pandas.read_csv(os.path.join(tmp_path, file), encoding="ISO-8859-1")
    return output


def createUSHighResCOVID19SpreadDB(
        tables_root_directory: str
) -> None:
    """
    The :func:`createUSHighResCOVID19SpreadDB` takes care of merging and preprocessing
    the integration of all the data resources on the US regions.

    Parameters
    ----------
    tables_root_directory: `str`, required
        The root directory to the dataset tables folder

    """
    output_directory = os.path.join(tables_root_directory, 'resolution/county')

    collection_path = tables_root_directory  # '/Volumes/samsung/erlab_us_covid_spread/erlab_covid19_glance/'
    collection = parse_erlab_covid19_glance_collection(collection_path=collection_path)

    ## preprocessing
    for key in preprocessings.keys():
        for table_name in preprocessings[key].keys():
            table = collection[key][table_name].copy()
            lambdas = preprocessings[key][table_name]['lambdas']
            renames = preprocessings[key][table_name]['rename']
            remove = preprocessings[key][table_name]['remove']
            for column in lambdas.keys():
                table[column] = table[column].apply(lambdas[column])
            table.rename(renames, inplace=True, axis="columns", errors="raise")
            table.drop(columns=remove, inplace=True)
            collection[key][table_name] = table.copy()
            table = None

    ## further preprocessing

    # income
    def income_check1(x):
        try:
            output = x.split(',')[1]
        except:
            output = 'bad'
        return output

    collection['county']['diversityindex']['state'] = collection['county']['diversityindex']['Location'].apply(
        income_check1)
    collection['county']['diversityindex'] = collection['county']['diversityindex'][
        collection['county']['diversityindex']['state'] != 'bad']
    collection['county']['diversityindex']['county'] = collection['county']['diversityindex']['Location'].apply(
        lambda x: remove_county_word(x.split(', ')[0]))
    collection['county']['diversityindex'].drop(columns=['Location'], inplace=True)

    # diversity
    collection['county']['diversityindex']['state'] = collection['county']['diversityindex']['state'].apply(
        lambda x: x.strip())

    # mortality
    def mortality_check1(x):
        try:
            output = x.split(', ')[1]
        except:
            output = 'bad'
        return output

    collection['county']['mortality']['state'] = collection['county']['mortality']['county'].apply(
        mortality_check1).copy()
    collection['county']['mortality'] = collection['county']['mortality'][
        collection['county']['mortality']['state'] != 'bad']
    collection['county']['mortality']['county'] = collection['county']['mortality']['county'].apply(
        lambda x: remove_county_word(x.split(',')[0]))
    collection['county']['mortality']['state'] = collection['county']['mortality']['state'].apply(
        lambda x: state_abbreviations[x])

    # election
    collection['county']['election'].drop(columns=['state_po'], inplace=True)
    collection['county']['election'] = collection['county']['election'][
        collection['county']['election']['year'] == 2016]
    collection['county']['election']['state'] = collection['county']['election']['state'].apply(
        lambda x: state_abbreviations[x])
    output = {
        'state': [],
        'county': [],
        'democrat': [],
        'republican': [],
        'other': [],
    }

    for i in range(collection['county']['election'].shape[0]):
        row = collection['county']['election'].iloc[i, :]
        output['state'] += [row['state']]
        output['county'] += [row['county']]
        if row['party'] == 'democrat':
            output['democrat'] += [row['candidatevotes']]
            output['republican'] += [0]
            output['other'] += [0]
        elif row['party'] == 'republican':
            output['republican'] += [row['candidatevotes']]
            output['democrat'] += [0]
            output['other'] += [0]
        else:
            output['republican'] += [0]
            output['democrat'] += [0]
            output['other'] += [row['candidatevotes']]

    collection['county']['election'] = pandas.DataFrame(output)

    ## icu beds
    collection['county']['icu_beds']['state'] = collection['county']['icu_beds']['state'].apply(
        lambda x: state_abbreviations[x])

    ## income [removed]
    # collection['county']['income'] = collection['county']['income'].groupby(
    #     ['county', 'state']).mean().reset_index().copy()

    ## land and water
    collection['county']['land_and_water'] = collection['county']['land_and_water'].loc[:,
                                             ['state', 'county', 'ALAND', 'AWATER', 'ALAND_SQMI', 'AWATER_SQMI']]

    """
    Proceeding to merging and forming the final dataset
    """

    # todo: fix this and maybe remove? or do createushighres data in run_routine
    # cases
    cases = collection['county']['cases'].copy()
    # todo: rename aggregate_covid_by_country to country
    aggregate_covid_by_country = {
        'sum': cases.groupby(['county', 'state']).sum().copy(),
        'mean': cases.groupby(['county', 'state']).mean().copy(),
        'median': cases.groupby(['county', 'state']).median().copy(),
        'max': cases.groupby(['county', 'state']).max().copy().drop(columns=['confirmed_date']),
        'min': cases.groupby(['county', 'state']).min().copy().drop(columns=['confirmed_date'])
    }

    for key in aggregate_covid_by_country.keys():
        aggregate_covid_by_country[key] = add_prefix_to_df_columns(df=aggregate_covid_by_country[key], prefix=key)

    aggregate_covid_county_table = merge_all_dfs_in_dict(aggregate_covid_by_country)

    # # [removed income_table]
    # income_table = collection['county']['income'].copy()
    #
    # aggregate_income_by_county = {
    #     'sum': income_table.groupby(['county', 'state']).sum().copy(),
    #     'mean': income_table.groupby(['county', 'state']).mean().copy(),
    #     'median': income_table.groupby(['county', 'state']).median().copy(),
    #     'max': income_table.groupby(['county', 'state']).max().copy().drop(columns=[]),
    #     'min': income_table.groupby(['county', 'state']).min().copy().drop(columns=[])
    # }
    #
    # for key in aggregate_income_by_county.keys():
    #     aggregate_income_by_county[key] = add_prefix_to_df_columns(df=aggregate_income_by_county[key], prefix=key)
    # aggregate_income_by_county = merge_all_dfs_in_dict(aggregate_income_by_county)

    # mortality

    mortality = collection['county']['mortality'].copy().drop(columns=[
        'Mortality Rate, 1980*',
        'Mortality Rate, 1980* (Min)',
        'Mortality Rate, 1980* (Max)',
        'Mortality Rate, 1985*',
        'Mortality Rate, 1985* (Min)',
        'Mortality Rate, 1985* (Max)',
        'Mortality Rate, 1990*',
        'Mortality Rate, 1990* (Min)',
        'Mortality Rate, 1990* (Max)',
        'Mortality Rate, 1995*',
        'Mortality Rate, 1995* (Min)',
        'Mortality Rate, 1995* (Max)',
        'Mortality Rate, 2000*',
        'Mortality Rate, 2000* (Min)',
        'Mortality Rate, 2000* (Max)',
        'Mortality Rate, 2005*',
        'Mortality Rate, 2005* (Min)',
        'Mortality Rate, 2005* (Max)',
        'Mortality Rate, 2010*',
        'Mortality Rate, 2010* (Min)',
        'Mortality Rate, 2010* (Max)'
    ]).rename({
        'Mortality Rate, 2014*': 'mortality_rate',
        'Mortality Rate, 2014* (Min)': 'min_mortality_rate',
        'Mortality Rate, 2014* (Max)': 'max_mortality_rate',
        '% Change in Mortality Rate, 1980-2014': "change_in_mortality_rate",
        '% Change in Mortality Rate, 1980-2014 (Min)': "min_change_in_mortality_rate",
        '% Change in Mortality Rate, 1980-2014 (Max)': "max_change_in_mortality_rate"
    }, inplace=False, axis="columns", errors="raise")
    mortality = mortality.groupby(['county', 'state']).mean().copy()

    # todo: shady
    # census
    census_full = collection['county']['census_full'].copy()
    census_full = census_full.groupby(['county', 'state']).mean()

    land_and_water = collection['county']['land_and_water'].copy()
    land_and_water = land_and_water.groupby(['county', 'state']).sum()

    election = collection['county']['election'].copy()
    election = election.groupby(['county', 'state']).sum()

    icu_beds = collection['county']['icu_beds'].copy()
    icu_beds = icu_beds.groupby(['county', 'state']).sum()

    diversity = collection['county']['diversityindex'].copy()
    diversity = diversity.groupby(['county', 'state']).sum()

    # dataframes = [aggregate_covid_county_table, census_full, icu_beds, diversity, election, land_and_water,
    #               aggregate_income_by_county, mortality]

    dataframes = [aggregate_covid_county_table, census_full, icu_beds, diversity, election, land_and_water,
                  mortality]

    USHighResCOVID19SpreadDB = reduce(
        lambda left, right: pandas.merge(left, right, left_index=True, right_index=True, how='outer'), dataframes)

    USHighResCOVID19SpreadDB.reset_index().to_csv(os.path.join(output_directory, 'USHighResCOVID19SpreadDB.csv'))


def add_day_of_the_year_to_cases_table(
        cases_dataframe: pandas.DataFrame
) -> pandas.DataFrame:
    """
    To add the day of the year for cases table this will be used.

    Parameters
    ----------
    cases: `pandas.DataFrame`, required
        The cases dataframe

    Returns
    ----------
    Returns the dataframe with the day of the year field
    """

    def get_day_of_the_year(x: str):
        year, month, day = [int(e) for e in x.split('-')]
        the_date = date(year, month, day)
        first_date = date(2020, 1, 1)
        delta = the_date - first_date
        return delta.days

    cases_dataframe['day_of_the_year'] = cases_dataframe['confirmed_date'].copy().apply(get_day_of_the_year)
    return cases_dataframe


def add_cumsums_to_cases_table_slow(
        cases: pandas.DataFrame
) -> pandas.DataFrame:
    """
    To add the cumsum values for death count and confirmed count, this will be used.

    Parameters
    ----------
    cases: `pandas.DataFrame`, required
        The cases dataframe

    Returns
    ----------
    Returns the dataframe with the cumsum values for cases added to it.
    """
    if not 'day_of_the_year' in cases.columns.tolist():
        cases = add_day_of_the_year_to_cases_table(cases)

    cases.sort_values(by=['state', 'county', 'day_of_the_year'], inplace=True)

    cases.reset_index(inplace=True, drop=True)

    cases['death_count_cumsum'] = cases['death_count'].copy()
    cases['confirmed_count_cumsum'] = cases['confirmed_count'].copy()
    cases['recovered_count_cumsum'] = cases['recovered_count'].copy()

    val1 = 0
    val2 = 0
    val3 = 0
    prev_state = 'wrong'
    prev_county = 'wrong'
    for i in range(cases.shape[0]):
        row = cases.iloc[i, :].copy()
        state = row['state']
        county = row['county']
        death_count = int(row['death_count'])
        confirmed_count = int(row['confirmed_count'])
        recovered_count = int(row['recovered_count'])
        if not ((state == prev_state) and (county == prev_county)):
            prev_state = state
            prev_county = county
            val1 = death_count
            val2 = confirmed_count
            val3 = recovered_count
        else:
            val1 += death_count
            val2 += confirmed_count
            val3 += recovered_count
        cases['death_count_cumsum'].iloc[i] = val1
        cases['confirmed_count_cumsum'].iloc[i] = val2
        cases['recovered_count_cumsum'].iloc[i] = val3

    return cases


def add_cumsums_to_cases_table(
        cases: pandas.DataFrame
) -> pandas.DataFrame:
    """
    To add the cumsum values for death count and confirmed count, this will be used.

    Parameters
    ----------
    cases: `pandas.DataFrame`, required
        The cases dataframe

    Returns
    ----------
    Returns the dataframe with the cumsum values for cases added to it.
    """
    if not 'day_of_the_year' in cases.columns.tolist():
        cases = add_day_of_the_year_to_cases_table(cases)

    cases.sort_values(by=['state', 'county', 'day_of_the_year'], inplace=True)

    cases.reset_index(inplace=True, drop=True)

    cases['death_count_cumsum'] = cases['death_count'].copy()
    cases['confirmed_count_cumsum'] = cases['confirmed_count'].copy()
    cases['recovered_count_cumsum'] = cases['recovered_count'].copy()

    cases = add_location_to_df(cases)

    for location in cases.location.unique():
        tmp = cases[cases.location == location].copy()
        tmp.death_count_cumsum = tmp.death_count_cumsum.cumsum()
        tmp.confirmed_count_cumsum = tmp.confirmed_count_cumsum.cumsum()
        tmp.recovered_count_cumsum = tmp.recovered_count_cumsum.cumsum()
        cases[cases.location == location] = tmp
        tmp = None

    cases.drop(columns=['location', 'day_of_the_year'], inplace=True)

    return cases


def add_location_to_df(
        df: pandas.DataFrame
) -> pandas.DataFrame:
    """
    To add the location for cases table this will be used.

    Parameters
    ----------
    cases: `pandas.DataFrame`, required
        The cases dataframe

    Returns
    ----------
    Returns the dataframe with the location field
    """
    if 'county' in df.columns.tolist():
        df['location'] = df['county'] + '_' + df['state']
    else:
        df['location'] = df['state']
    return df


def fill_nans_by_propagation_through_time(df):
    # if df.isna().sum().sum() == 0:
    #     return df
    # else:
    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)

    df = df.copy().groupby(['location', 'state', 'county']).apply(lambda x: x.drop(columns=['county', 'state', 'location']).sort_values(by=['day_of_the_year']).fillna(method='ffill')).reset_index()

    df.dropna(inplace=True)
    return df


def olivia_interpolation(df: pandas.DataFrame) -> pandas.DataFrame:
    """
    The :func:`olivia_interpolation` helps with interpolating the values between the first and last
    day of events for our dataframes to have more consistent COVID-19 information.

    Parameters
    ----------
    df: `pandas.DataFrame`, required
        The main pandas dataframe that is loaded.

    Returns
    -----------
    This method returns the now modified dataframe
    """


    df = add_location_to_df(df)
    df = add_day_of_the_year_to_cases_table(df)
    df.sort_values(by=['location', 'day_of_the_year'], inplace=True)
    min_day = int(df['day_of_the_year'].min())
    max_day = int(df['day_of_the_year'].max())
    unique_locations = df['location'].unique().tolist()

    all_possible_days = list(range(min_day, max_day + 1))

    placeholder_columns = itertools.product(unique_locations, all_possible_days)
    placeholder_columns = list(zip(*placeholder_columns))

    placeholder_df = pandas.DataFrame({
        'location': placeholder_columns[0],
        'day_of_the_year': placeholder_columns[1]
    })
    df = pandas.merge(left=df, right=placeholder_df, on=['location', 'day_of_the_year'], how='outer').reset_index(drop=True)
    df.loc[df.county.isna(), 'county'] = df.loc[df.county.isna(), 'location'].apply(lambda x: x.split('_')[0])
    df.loc[df.state.isna(), 'state'] = df.loc[df.state.isna(), 'location'].apply(lambda x: x.split('_')[1])

    df = df[df.location.isin(unique_locations)]
    df = fill_nans_by_propagation_through_time(df)

    if 'level_3' in df.columns:
        df.drop(columns=['level_3'], inplace=True)

    return df


def doty_to_date(day_of_the_year, use_slash: bool = True):
    days = day_of_the_year
    out = str(date(2020, 1, 1) + timedelta(days=int(days)))
    if use_slash:
        out = out.replace('-', '/')
    return out
