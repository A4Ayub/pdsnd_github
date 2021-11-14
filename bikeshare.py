import time
import pandas as pd
import numpy as np
# Picked from the https://stackoverflow.com/questions/12332975/installing-python-module-within-code
import subprocess
import sys
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('inquirer')
import inquirer

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. A user is allowed to provide the city, month and day in order to filter the records.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! To select an option please use the keyboard arrow keys!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_question = [
      inquirer.List('city',
                    message="Which city would you like to see",
                    choices=['Chicago', 'New York City', 'Washington'],
                ),
    ]
    city_answer = inquirer.prompt(city_question)
    city = city_answer['city']

    # get user input for month (all, january, february, ... , june)
    month_question = [
      inquirer.List('month',
                    message="Which month would you like to see",
                    choices=['All', 'January', 'February', 'March', 'April', 'May', 'June'],
                ),
    ]
    month_answer = inquirer.prompt(month_question)
    month = month_answer['month']

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_of_week_question = [
      inquirer.List('day_of_week',
                    message="Which day would you like to see",
                    choices=['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                ),
    ]
    day_of_week_answer = inquirer.prompt(day_of_week_question)
    day = day_of_week_answer['day_of_week']

    # Confirm the options selected by the use
    confirm_question = [
      inquirer.List('confirmation',
                    message="You have selected to view {} records, and {} as the preferred month(s) with {} as the preferred day(s) of week. Is this correct?".format(city,month,day),
                    choices=['Yes', 'No'],
                ),
    ]
    confirm_answer = inquirer.prompt(confirm_question)
    user_confirmation = confirm_answer['confirmation']

    view_summary_question = [
      inquirer.List('view_confirmation',
                    message="Would you like to see the first five lines of raw data?",
                    choices=['Yes', 'No'],
                ),
    ]
    confirm_summary = inquirer.prompt(view_summary_question)
    user_summary_confirmation = confirm_summary['view_confirmation']

    #view_next_summary_question = [
    #  inquirer.List('view_next_confirmation',
    #                message="Would you like to see the next five lines of raw data?",
    #                choices=['Yes', 'No'],
    #            ),
    #]
    #confirm_next_summary = inquirer.prompt(view_next_summary_question)
    #user_next_summary_confirmation = confirm_next_summary['view_next_confirmation']


    print('-'*40)

    return city, month, day, user_confirmation, user_summary_confirmation

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable. THis will load the data as per the desired filters!

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the date field to datetime datatype so that we can extract the month
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month.lower() != 'all':
        months = ['january','february','march','april','may','june']
        month = months.index(month.lower()) + 1
        #print("The month is : ",month)
        df = df[df['month'] == month]

    if day.lower() != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    months = ['january','february','march','april','may','june']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    common_month = months[df["month"].mode()[0] - 1].title()

    # display the most common month
    print("{} is the most common month! ".format(common_month))

    # display the most common day of week
    print("{} is the most common day of week! ".format(df["day_of_week"].mode()[0]))


    # display the most common start hour
    print("{} is the most common start hour! ".format(df["hour"].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is {}!".format(df["Start Station"].mode()[0]))

    # display most commonly used end station
    print("The most commonly used end station is {}!".format(df["End Station"].mode()[0]))


    # display most frequent combination of start station and end station trip
    df["trip"] = df["Start Station"] +"_" + df["End Station"]
    common_trip = df["trip"].mode()[0]
    #print("The common trip is :: {}".format(common_trip))
    from_ = common_trip.split("_")[0]
    #print("The from address is {}".format(from_))
    to_ = common_trip.split("_")[1]
    #print("The to address is {}".format(to_))
    value_cnt = df[df["trip"] == common_trip].size
    #print(value_cnt)
    print("The most common trip is from {} to {} with a total of {} trips done!".format(from_,to_,value_cnt))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The trip duration time is {} seconds!".format(df["Trip Duration"].sum()))

    # display mean travel time
    print("The average trip duuration is {} seconds!".format(df["Trip Duration"].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    #print(df.info())

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nCount of users by User Type")
    print(df["User Type"].fillna("Unknown User Type").value_counts())

    # Display counts of gender
    if "Gender" in df:
        print("\nCount by Gender")
        print(df["Gender"].fillna("Unknown Gender").value_counts())


    if "Birth Year" in df:
        # Display earliest, most recent, and most common year of birth
        # Convert year of birth to integer
        print("The earliest year of birth is {}".format(df["Birth Year"].min().astype(str).split(".")[0]))

        print("The latest year of birth is {}".format(df["Birth Year"].max().astype(str).split(".")[0]))

        print("The common year of birth is {}".format(df["Birth Year"].mode()[0].astype(str).split(".")[0]))


    print("\Executing your code too %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    start_loc = 0
    while True:
        city, month, day, confirm, summary = get_filters()

        if confirm.lower() != 'yes':
            break

        df = load_data(city, month, day)

        if summary.lower() == 'yes':
            while start_loc < df.shape[0]:
                print(df.iloc[start_loc:start_loc+5])
                start_loc += 5
                view_next_summary_question = [
                  inquirer.List('view_next_confirmation',
                                message="Would you like to see the next five lines of raw data?",
                                choices=['Yes', 'No'],
                            ),
                ]
                confirm_next_summary = inquirer.prompt(view_next_summary_question)
                user_next_summary_confirmation = confirm_next_summary['view_next_confirmation']

                if user_next_summary_confirmation.lower() != 'yes':
                    break

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nThank you for using the tool, would you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
