import logging

log = logging.getLogger('poetry_demo_cs151')

def enlarge_stuff(stuff):
    return stuff.upper()


def main():
    log.info("starting up")