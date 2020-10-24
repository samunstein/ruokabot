import requests
from datetime import datetime, timedelta, date
from time import sleep
from generointi import reader, randomer
from generointi.ruoka import Ruoka

from bot_token import TOKEN

from statics import EXTRA_PER_WEEK, POLL_INTERVAL_SECONDS, STARTUP_NEWNESS_MINUTES, FOOD_COMMAND, FOOD_STORAGE, EXTRA_COMMAND, RELOAD_COMMAND, RERANDOMIZE_COMMAND


current_offset = 0
foodmap = dict()


def make_get_req(method, params=None):
    url = "https://api.telegram.org/bot{}/{}".format(TOKEN, method)
    return requests.get(url, params if params is not None else {})


def make_post_req(method, params=None):
    params = {} if params is None else params
    url = "https://api.telegram.org/bot{}/{}".format(TOKEN, method)
    return requests.post(url, params)


def get_messages():
    global current_offset
    resp = make_get_req("getUpdates", {"offset": current_offset})
    messages = resp.json()["result"] if "result" in resp.json() else []
    if len(messages) > 0:
        last_update = max(map(lambda m: m["update_id"], messages))
        current_offset = last_update + 1
    current_time = datetime.now().timestamp()

    messages = filter(lambda m: "message" in m, messages)
    messages = map(lambda m: m["message"], messages)
    new_enough = filter(lambda m: m["date"] > current_time - 60 * STARTUP_NEWNESS_MINUTES, messages)
    return list(new_enough)


def get_requests(messages, commands):
    return list(filter(lambda m: "text" in m and m["text"].lower().split()[0] in commands, messages))


def get_unknown_requests(messages, known_commands):
    return list(filter(lambda m: "text" in m and m["text"].lower().split()[0] not in known_commands, messages))


def is_int(text):
    try:
        int(text)
        return True
    except ValueError:
        return False


def read_foods(offset, extra):
    now = date.today()
    wanted = now + timedelta(weeks=offset)
    try:
        with open("{}/{}_{}".format(FOOD_STORAGE, wanted.year, wanted.isocalendar()[1]), encoding="UTF-8") as f:
            names = [a.strip() for a in f.readlines()]
            if extra:
                names = names[-EXTRA_PER_WEEK:]
            else:
                names = names[:-EXTRA_PER_WEEK]
            ruoat = list(map(lambda name: foodmap[name] if name in foodmap else Ruoka.ei_loydy(name), names))
            return ruoat
    except:
        return []


def format_food(food):
    base = "{}: {} annosta.\n{}".format(food.nimi, food.annokset, "".join(["* {}\n".format(i.strip()) for i in food.ainekset.split(",")]))
    return base + "\n{}".format(food.linkki) if food.linkki is not None else base


def handle_food_request(food_request):
    week_offset = 0
    send_extra = food_request["text"].lower().startswith(EXTRA_COMMAND)
    offsettxt = " ".join(food_request["text"].split()[1:])
    if is_int(offsettxt):
        week_offset = int(offsettxt)

    foods = read_foods(week_offset, send_extra)
    foods = list(map(format_food, foods))

    chat_id = food_request["chat"]["id"]

    for food in foods:
        make_post_req("sendMessage", {"chat_id": chat_id, "text": food})


def handle_reload(message):
    global foodmap
    foodmap = reader.read()
    make_post_req("sendMessage", {"chat_id": message["chat"]["id"], "text": "Pling!"})


def handle_generate(message):
    week_offset = 0
    offsettxt = " ".join(message["text"].split()[1:])
    if is_int(offsettxt):
        week_offset = int(offsettxt)

    global foodmap
    foodmap = randomer.generate(week_offset)
    make_post_req("sendMessage", {"chat_id": message["chat"]["id"], "text": "Pling!"})


def handle_help(message):
    apu = "Ruoka: {} [offset]\nExtra: {} [offset]\nPäivitä sheetsistä: {}\nGeneroi uudelleen: {} [offset]".format(
        FOOD_COMMAND, EXTRA_COMMAND, RELOAD_COMMAND, RERANDOMIZE_COMMAND
    )
    make_post_req("sendMessage", {"chat_id": message["chat"]["id"], "text": apu})


def loop():
    try:
        messages = get_messages()
    except requests.exceptions.ConnectionError as e:
        print(e)
        messages = []

    for food_message in get_requests(messages, [FOOD_COMMAND, EXTRA_COMMAND]):
        handle_food_request(food_message)
    for reload_message in get_requests(messages, [RELOAD_COMMAND]):
        handle_reload(reload_message)
    for regenerate_message in get_requests(messages, [RERANDOMIZE_COMMAND]):
        handle_generate(regenerate_message)
    for unknown_message in get_unknown_requests(messages, [FOOD_COMMAND, EXTRA_COMMAND, RERANDOMIZE_COMMAND, RELOAD_COMMAND]):
        handle_help(unknown_message)


def main():
    global foodmap
    foodmap = reader.read()
    while True:
        sleep(POLL_INTERVAL_SECONDS)
        loop()


if __name__ == "__main__":
    main()
