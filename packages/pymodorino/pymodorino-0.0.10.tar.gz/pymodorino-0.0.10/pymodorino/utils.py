def minutesToSeconds(minutes):
    return int(minutes * 60)

def getRemainingTime(seconds):
    minutes = seconds // 60
    return f"{minutes}m {seconds - minutes * 60}s"

def printMessage(message, terminal):
    t = terminal
    with t.location():
        print('\n\n')
        print(t.center("", fillchar="@"))
        print("@" + t.move_right(t.width) + "@")
        print(t.center(f"    {message}    ", fillchar="~"))
        print("@" + t.move_right(t.width) + "@")
        print(t.center("", fillchar="@"))