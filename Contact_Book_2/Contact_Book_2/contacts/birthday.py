import calendar
from datetime import date

def next_birthday(dob, today=None):
    """Return the next birthday date and days remaining. Feb 29 birthdays use Feb 28 in non-leap years."""
    today = today or date.today()
    year = today.year
    month, day = dob.month, dob.day

    def birthday_for(target_year):
        if month == 2 and day == 29 and not calendar.isleap(target_year):
            return date(target_year, 2, 28)
        return date(target_year, month, day)

    upcoming = birthday_for(year)
    if upcoming < today:
        upcoming = birthday_for(year + 1)
    return upcoming, (upcoming - today).days


def birthday_art(days_remaining):

    if days_remaining >= 100:
        return {
            "image": "images/birthdays/ben10.svg",
            "title": "Birthday is on the horizon!",
            "message": "A hero-sized countdown starts here.",
            "kind": "ben10",
        }

    elif days_remaining >= 31:
        return {
            "image": "images/birthdays/anime.svg",
            "title": "The birthday is getting closer!",
            "message": "A little anime excitement for the countdown.",
            "kind": "anime",
        }

    else:
        return {
            "image": "images/birthdays/celebration.svg",
            "title": "Celebration is almost here!",
            "message": "Get ready to celebrate this special day.",
            "kind": "celebration",
        }
