import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago':'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) user_filter - user selected filter to control which data is displayed
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please select one city to evaluate: Chicago, New York City, Washington: ').lower()
        if city not in CITY_DATA:
            print('Please enter your selection exactly.')
        else:
            print('Thank you for selecting: {}'.format(city))
            break

    # ask if user wants to select month, day or neither
    user_filters = ['month','day','neither']
    while True:
        user_filter = input('Would you like to filter by month, day or neither (will display results from full dataset)?').lower()
        if user_filter not in user_filters:
            print('Please select month, day or nothing')
        else:
            print('Thank you for filtering by {}'.format(user_filter))
            break

    # get user input for month (all, january, february, ... , june)
    if user_filter == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        while True:
            month = input('Please select one month between January through June or type all to see data for all months: ').lower()
            if month == 'all':
                print('Thank you for selecting all months.')
                break
            elif month not in months:
                print('Please enter one of these months: January, February, March, April, May, June or type All.')
            else:
                print('Thank you for selecting: {}'.format(month))
                break
    else:
        month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if user_filter == 'day':
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        while True:
            day = input('Please select a day of the week by name or type All to see data for all days of the week:').lower()
            if day == 'all':
                print('Thank you for selecting all days.')
                break
            elif day not in days:
                print('Please enter a day of the week or type All.')
            else:
                print('Thank you for selecting: {}'.format(day))
                break
    else:
        day = 'all'

    print('-'*40)
    return city, month, day, user_filter


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

def time_stats(df, user_filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if user_filter != 'month':
        df['month'] = df['Start Time'].dt.strftime('%B')
        print('Bikeshare users most often used this service in the month of {}.'.format(df['month'].mode()[0]))

    # display the most common day of week
    if user_filter != 'day':
        print('Bikeshare users most often used this service on {}.'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    print('Bikeshare users most often started their journey in hour {}.'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('The most commonly used start station was {}.'.format(popular_start))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('The most commonly used end station was {}.'.format(popular_end))

    # display most frequent combination of start station and end station trip
    df['trips'] = df['Start Station'] + ' to ' + df['End Station']
    popular_trip = df['trips'].mode()[0]
    print('The most frequent trip was from {}.'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total time traveled was {} hours.'.format(total_time/3600))

    # display mean travel time
    mean_trip = df['Trip Duration'].mean()
    print('The average trip length was {} minutes'.format(mean_trip/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The count of User Types are:\n', df['User Type'].value_counts())

    # Display counts of gender
    try:
        print('\nThe number of users by gender are:\n', df['Gender'].value_counts())
    except KeyError:
        print('\nNo gender data is available.')

    # Display earliest, most recent, and most common year of birth
    try:
        print('\nThe earliest birth year is', int(df['Birth Year'].min()))
        print('The most recent birth year is', int(df['Birth Year'].max()))
        print('The most common birth year is', int(df['Birth Year'].mode()))
    except KeyError:
        print('\nNo birth year data is available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    # allows user to view raw data after day/month filters
    raw_data = input('\nWould you like to view 5 rows of the raw data? Enter yes or no.\n')
    n = 0
    while raw_data.lower() == 'yes' and n <= len(df.index):
        print(df.iloc[n:n+5])
        n += 5
        raw_data = input('\nWould you like to view 5 more rows of the raw data? Enter yes or no.\n')

def main():
    while True:
        city, month, day, user_filter = get_filters()
        df = load_data(city, month, day)

        time_stats(df, user_filter)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        # asks user if they wish to restart
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
