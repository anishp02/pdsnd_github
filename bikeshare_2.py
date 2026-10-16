import time
import pandas as pd
import numpy as np

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?: ').lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('Invalid: Please input Chicago, New York City, or Washington.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('What month would you like to see data for (All, January, February, March, April, May, June)? ').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Invalid: Please input All, January, February, March, April, May or June.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('What day would you like to see data for (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)? ').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Invalid: Please input All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday.')

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

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['month'] == month.title()]

    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = df['month'].mode()[0]
    print('Most Common Month: ', month)

    # display the most common day of week
    day = df['day'].mode()[0]
    print('Most Common Day: ', day)

    # display the most common start hour
    hour = df['hour'].mode()[0]
    print('Most Common Hour: ', hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station: ', start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most Common End Station: ', end_station)

    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' -> ' + df['End Station']
    combo = df['trip'].mode()[0]
    print('Most Common Trip: ', combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_s = df['Trip Duration'].sum()
    days, rem = divmod(total_time_s, 24*3600)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    print('Total Travel Time: ' , days, 'days', hours, 'hrs', minutes, 'mins', seconds, 'secs')

    # display mean travel time
    avg_time_s = df['Trip Duration'].mean()
    minutes, seconds = divmod(avg_time_s, 60)
    print('Average Travel Time: ', minutes, 'min', round(seconds, 2), 'secs')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users = df['User Type'].value_counts().rename_axis(None)
    print('User Types:')
    print(users.to_string())

    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts().rename_axis(None)
        print('\nGender Count:')
        print(genders.to_string())
    else:
        print('No gender data.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])
        print('\nEarliest Birth Year: ', earliest)
        print('Most Recent Birth Year: ', recent)
        print('Most Common Birth Year: ', common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
