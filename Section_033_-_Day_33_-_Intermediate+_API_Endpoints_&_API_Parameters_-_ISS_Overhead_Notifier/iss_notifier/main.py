from location import (
    get_current_location,
    reverse_geocode,
    summarize_location
)
from astronomy import (
    is_night,
    get_iss_position,
    is_iss_overhead
)
from email_service import send_email
from output import print_header, print_kv

def main():
    print_header("ISS VISIBILITY CHECK")

    my_location = get_current_location()
    iss_location = get_iss_position()

    my_place = reverse_geocode(
        my_location["latitude"],
        my_location["longitude"]
    )
    iss_place = reverse_geocode(
        iss_location["latitude"],
        iss_location["longitude"]
    )

    print_kv("Your location", summarize_location(my_place))
    print_kv("Your latitude", f"{my_location['latitude']:.4f}")
    print_kv("Your longitude", f"{my_location['longitude']:.4f}")

    print()
    print_kv("ISS location", summarize_location(iss_place))
    print_kv("ISS latitude", f"{iss_location['latitude']:.4f}")
    print_kv("ISS longitude", f"{iss_location['longitude']:.4f}")

    print("\n" + "─" * 60)

    try:
        if is_night(my_location):
            print("🌙 It is currently NIGHT.")
            if is_iss_overhead(my_location, iss_location):
                print("🚀 THE ISS IS OVERHEAD!")
                send_email(
                    "The ISS is overhead!",
                    "The International Space Station is currently passing overhead from your location.\n\n"
                    "This is a rare and beautiful moment when the sky is dark enough to spot it with the naked eye.\n\n"
                    "Step outside, find a clear view of the sky, and look up. You may see a steady, fast-moving point of light crossing above you."
                )
            else:
                print("ℹ ISS not overhead.")
                send_email(
                    "ISS Update",
                    "It is currently nighttime at your location, but the International Space Station is not overhead right now.\n\n"
                    "The ISS orbits the Earth rapidly, so visibility changes often.\n\n"
                    "Keep an eye out—another opportunity to see it may occur soon."
                )
        else:
            print("☀ DAYTIME – ISS not visible.")
            send_email(
                "ISS Update",
                "The International Space Station is not visible at the moment because it is currently daytime at your location.\n\n"
                "ISS sightings are best during nighttime or early dawn when the sky is darker.\n\n"
                "You will be notified again when viewing conditions improve."
            )

        print("Email sent successfully!")
    except Exception as e:
        print(f"Email error: {e}")


    print("─" * 60)

if __name__ == "__main__":
    main()
