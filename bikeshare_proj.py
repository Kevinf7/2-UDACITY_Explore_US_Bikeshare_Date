import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
DAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

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
    city = ''
    while True:
        city = input('Please enter city: ').lower()
        if city not in CITY_DATA.keys():
            print('The city you entered is not valid. Please try again.')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    month = ''
    while True:
        month = input('Please enter month: ').lower()
        if (month not in MONTH_DATA) and (month != 'all'):
            print('The month you entered is not valid. Please try again.')
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while True:
        day = input('Please enter day: ').lower()
        if (day not in DAY_DATA) and (day != 'all'):
            print('The day you entered is not valid. Please try again.')
        else:
            break

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
    #df = pd.read_csv(CITY_DATA[city], nrows=2000)

    # convert the Start Time and End Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int

        month = MONTH_DATA.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    #filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'].str.lower() == day]

    return df

def display_details(df):
    """Display details of records returned"""
    print('\nDisplaying results...\n')

    sloc = 0
    eloc = 5
    while True:
        print(df.iloc[sloc:eloc])
        if eloc >= df.shape[0]:
            input('No more data. Press ENTER to continue...')
            break
        elif input('Display more? (y/n)').lower() == 'n':
            break
        sloc = eloc
        eloc = sloc+5
    print('-'*40)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month
    if(df['month'].isnull().all()):
        print('\nThere is no data for the month chosen. Cannot calculate most common month.')
    else:
        print('\nMost common month(s):')
        for mnth in df['month'].mode():
            print('  ' + MONTH_DATA[int(mnth)-1].title())
        print('Total of', df['month'].value_counts().max(), 'occurrence(s).')

    # display the most common day of week
    if(df['day_of_week'].isnull().all()):
        print('There is no data for the day chosen. Cannot calculate most common day of the week.')
    else:
        print('\nMost common day of the week(s):')
        for dayw in df['day_of_week'].mode():
            print('  ' + dayw)
        print('Total of', df['day_of_week'].value_counts().max(), 'occurrence(s).')

    # display the most common start hour
    if(df['Start Time'].isnull().all()):
        print('There is no data for the start time. Cannot calculate the most common start hour.')
    else:
        df['hour'] = df['Start Time'].dt.strftime('%I %p')
        print('\nMost common start hour(s):')
        for sthr in df['hour'].mode():
            print('  ' + str(sthr))
        print('Total of', df['hour'].value_counts().max(), 'occurrence(s).')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start station
    if(df['Start Station'].isnull().all()):
        print('\nThere is no data for the start station. Cannot calculate most commonly used start station.')
    else:
        print('\nMost commonly used start station(s):')
        for str_stn in df['Start Station'].mode():
            print('  ' + str_stn)
        print('Station(s) used', df['Start Station'].value_counts().max(), 'time(s).')

    # display most commonly used end station
    if(df['End Station'].isnull().all()):
        print('There is no data for the end station. Cannot calculate most commonly used end station.')
    else:
        print('\nMost commonly used end station(s):')
        for end_stn in df['End Station'].mode():
            print('  ' + end_stn)
        print('Station(s) used', df['End Station'].value_counts().max(), 'time(s).')

    # display most frequent combination of start station and end station trip
    if(df['Start Station'].isnull().all() or df['End Station'].isnull().all()):
        print('There is no data for the start and end station. Cannot calculate most commonly used start and end station.')
    else:
        print('\nMost frequent combination of start station and end station(s):')
        df['stations'] = df['Start Station'] + '**' + df['End Station'] #create new temp column with combined start end stations separated by **
        for stns in df['stations'].mode():
            stn = stns.split('**')
            print('  Start Station:', stn[0], '  End Station:', stn[1])
        print('Station(s) used', df['stations'].value_counts().max(), 'time(s).')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    if(df['Trip Duration'].isnull().all()):
        print('\nThere is no data for trip duration. Cannot calculate total travel time.')
    else:
        print('\nTotal travel time (in minutes):',round(df['Trip Duration'].sum()/60,2))

    # display mean travel time
    if(df['Trip Duration'].isnull().all()):
        print('There is no data for trip duration. Cannot calculate mean travel time.')
    else:
        print('Mean travel time (in minutes):',round(df['Trip Duration'].mean()/60,2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    if(df['Trip Duration'].isnull().all()):
        print('\nThere is no data for user type. Cannot calculate counts of user types.')
    else:
        print('\nCounts of user types:')
        print(df['User Type'].value_counts())

    # Display counts of gender

    if 'Gender' not in df.columns:
        print('The city chosen has no gender data.')
    else:
        if(df['Gender'].isnull().all()):
            print('There is no data for gender. Cannot calculate counts of gender.')
        else:
            print('\nCounts of gender:')
            print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print('The city chosen has no birth year data.')
    else:
        if(df['Birth Year'].isnull().all()):
            print('There is no data for birth year. Cannot calculate counts of birth year.')
        else:
            print('\nEarliest year of birth:',int(df['Birth Year'].min()))
            print('Most recent year of birth:',int(df['Birth Year'].max()))
            print('Most common year of birth:')
            for yob in df['Birth Year'].mode():
                print('  '+str(int(yob)))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_details(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
