import time
import pandas as pd
import numpy as np
from datetime import timedelta


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). 
    print('Would you like to see data for Chicago, New York City, or Washington?')


    cities = ("chicago", "new york city", "washington")

    # Asks the user on which city to filter
    while True:
        city = input("City: ")
        city = city.lower()
        if city not in cities:
            print("Type Chicago, New York City or Washington: ")
            continue
        else:
            break

    print("Would you like to filter the data by month, day or not at all? Type 'none' for no time filter")

    while True:
        filter = input("Type month, day or none: ")
        if filter.lower() not in ("month","day","none"):
            print("Please try again: ")
            continue
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    if filter.lower() == "month":
        while True:
            months = ("january", "february", "march", "april", "may", "june")
            month = input("For which month would you like to filter? Choose between January, February, March, April, May or June: ")
            month = month.lower()
            if month not in months:
                print("Please try again")
                continue
            else:
                day = "all"
                break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if filter.lower() == "day":
        while True:
            days = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
            day = input("For which day would you like to filter? Choose Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday: ")
            day = day.lower()
            if day not in days:
                print("Please try again")
                continue
            else:
                month = "all"
                break

    if filter.lower() == "none":
            month = "all"
            day = "all"

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times Of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month_name()
    common_month = df['month'].mode()[0]
    print('Most common month: ', common_month)


    # TO DO: display the most common day of week
    df['dow'] = df['Start Time'].dt.weekday_name
    common_dow = df['dow'].mode()[0]
    print('Most common day of the week: ', common_dow)

    # TO DO: display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common start hour: ', common_hour, "o'clock")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: ', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: ', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Start and End Station'] = "'"+ df['Start Station'] + "'" + " and " + "'" + df['End Station'] + "'"
    common_startend = df['Start and End Station'].mode()[0]
    print('Most frequent combination of start and end station in a trip: ', common_startend)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df.loc[:,'Trip Duration'].sum(skipna = True)
    ttt_string = str(timedelta(seconds=int(total_travel_time)))
    print('The total travel time is: ', ttt_string, ' h:m:s')
    # TO DO: display mean travel time
    mean_travel_time = df.loc[:,'Trip Duration'].mean(skipna = True)
    mtt_string = str(timedelta(seconds=int(mean_travel_time)))
    print('The mean travel time is: ', mtt_string, ' h:m:s')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The counts of different user types:\n', user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df:
        df['Gender'].dropna(inplace=True)
        gender_counts = df['Gender'].value_counts()
        print('\nThe counts of different genders:\n', gender_counts)
    else:
        print('\nUnfortunately, there is no gender information available for Washington')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        df['Birth Year'].dropna(inplace=True)
        earliest_birth = df['Birth Year'].min()
        print('\nThe earliest birth year is: ', earliest_birth.astype(int))
        recent_birth = df['Birth Year'].max()
        print('The most recent birth year is: ', recent_birth.astype(int))
        common_birth = df['Birth Year'].mode()[0]
        print('The most common birth year is: ', common_birth.astype(int))
    else:
        print('\nUnfortunately, there is no birth year information available for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def rawdata(df):
    x = 0
    while True:
        inputraw = input("Would you like to view (extra) individual trip data? Type 'yes' or 'no': ")
        inputraw = inputraw.lower()
        if inputraw == "yes":
            print(df.iloc[x:(x+5)])
            x += 5
        if inputraw == "no":
            break
        if inputraw != "yes" or "no":
            print("Please try again")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        rawdata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
