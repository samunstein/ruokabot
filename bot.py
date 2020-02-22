import requests
from datetime import datetime, timedelta, date
from time import sleep

from bot_token import TOKEN

from statics import EXTRA_PER_WEEK, POLL_INTERVAL_SECONDS, STARTUP_NEWNESS_MINUTES, FOOD_COMMAND, FOOD_STORAGE


current_offset = 0


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
    messages = resp.json()["result"]
    if len(messages) > 0:
        last_update = max(map(lambda m: m["update_id"], messages))
        current_offset = last_update + 1
    current_time = datetime.now().timestamp()

    messages = filter(lambda m: "message" in m, messages)
    messages = map(lambda m: m["message"], messages)
    new_enough = filter(lambda m: m["date"] > current_time - 60 * STARTUP_NEWNESS_MINUTES, messages)
    return list(new_enough)


def get_food_requests(messages):
    return list(filter(lambda m: "text" in m and m["text"].startswith(FOOD_COMMAND), messages))


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
            ruoat = f.read().strip().split("\n")
            if extra:
                return ruoat[-EXTRA_PER_WEEK:]
            else:
                return ruoat[:-EXTRA_PER_WEEK]
    except:
        return None


def format_food(food_text):
    name, ingredients = food_text.split("\t")
    return "{}:\n{}".format(name, "".join(["* {}\n".format(i.strip()) for i in ingredients.split(",")]))


def handle_food_request(food_request):
    send_extra = False
    week_offset = 0
    parameters = food_request["text"].split()[1:]
    if "extra" in parameters:
        send_extra = True
    numberparam = list(filter(is_int, parameters))
    if len(numberparam) > 0:
        week_offset = int(numberparam[0])

    foods = read_foods(week_offset, send_extra)
    foods = list(map(format_food, foods))

    chat_id = food_request["chat"]["id"]

    for food in foods:
        make_post_req("sendMessage", {"chat_id": chat_id, "text": food})


def loop():
    messages = get_messages()
    food_requests = get_food_requests(messages)

    for food_message in food_requests:
        handle_food_request(food_message)


def main():
    while True:
        sleep(POLL_INTERVAL_SECONDS)
        loop()


if __name__ == "__main__":
    main()
