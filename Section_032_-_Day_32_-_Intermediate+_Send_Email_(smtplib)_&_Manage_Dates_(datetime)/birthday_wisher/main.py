from logic.birthday_selector import BirthdaySelector
from mail.builder import build_birthday_email
from mail.sender import MailSender


CSV_PATH = "data/birthdays.csv"

def main():
    selector = BirthdaySelector(CSV_PATH)
    sender = MailSender()

    birthdays = selector.get_birthdays()

    if birthdays.empty:
        print("No birthdays today")
        return

    for _, person in birthdays.iterrows():
        msg = build_birthday_email(
            name=person["name"],
            recipient=person["email"]
        )
        sender.send_email(msg)

    print("Birthday emails sent successfully")

if __name__ == "__main__":
    main()
