from pybot import robot
import sys
import getopt


@robot.hear(r"^badger$")
def badger(res):
    res.send("thangs")


@robot.respond("say hi")
def say_hi(res):
    res.reply("hello")


@robot.hear(r"open the (.*?) doors")
def open_pod_bay_doors(res):
    door_type = res.match.group(1)
    if door_type == 'pod bay':
        res.reply("I'm afraid I can't let you do that")
    else:
        res.reply("Opening {} doors".format(door_type))


@robot.on('connected')
def on_connected(data):
    robot.send('shell', "I am here world")


def usage():
    print("-a adapter")
    print("-h help")


if __name__ == '__main__':
    useful_args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(useful_args, "a:h", ["adapter=", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-a", "--adapter"):
            robot.load_adapter(arg)

    robot.run()
