from datetime import datetime, timedelta


def is_leap_year(year):
    if year % 4 == 0:
        return True
    else:
        return False


def find_future_date(n, day, month, year, dow):
    days_of_week = ["Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday"]
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    if is_leap_year(year):
        days_in_month[1] = 29

    for _ in range(n):
        day += 1
        if day > days_in_month[month - 1]:
            day = 1
            month += 1
            if month > 12:
                month = 1
                year += 1
                if is_leap_year(year):
                    days_in_month[1] = 29
                else:
                    days_in_month[1] = 28

    return day, month, year, days_of_week[(dow + n) % 7]


if __name__ == "__main__":
    day = int(input("Enter the starting day (1-31): "))
    month = int(input("Enter the starting month (1-12): "))
    year = int(input("Enter the starting year: "))
    dow = int(input("Enter the day of week: "))

    n = int(input("Enter the number of days: "))
    future_day = find_future_date(
        n, day, month, year, dow)
    print(future_day)
