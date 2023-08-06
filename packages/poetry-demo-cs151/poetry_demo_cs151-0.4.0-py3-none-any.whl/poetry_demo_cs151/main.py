import logging

log = logging.getLogger('poetry_demo_cs151')

def enlarge_stuff(stuff):
    return stuff.upper()

def decrease_things(things):
    return things.lower()

def main():
    log.info("starting up!")