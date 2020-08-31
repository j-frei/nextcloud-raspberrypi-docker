import time, os, sys, ssl, urllib.request

if __name__ == "__main__":
    wait_sec = int(os.environ.get("SLEEP_SEC", 60))
    url = os.environ.get("CRON_URL")

    # execute first cron task as soon as possible
    first_cron = False
    while not first_cron:
        try:
            urllib.request.urlopen(url, context=ssl.SSLContext())
            first_cron=True
        except:
            time.sleep(1)

    # enter default cron loop
    try:
        while True:
            try:
                urllib.request.urlopen(url, context=ssl.SSLContext())
            except:
                print("Could not connect to {}.".format(url), file=sys.stderr)

            time.sleep(wait_sec)
    except:
        print("Container was stopped... Exiting...")
