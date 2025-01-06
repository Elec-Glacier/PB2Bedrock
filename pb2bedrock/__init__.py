import threading
import time


saving_in_progress = False
save_query_timer = None


def on_load(server, old):
    server.logger.info('PB2Bedrock')


def start_save_query_loop(server):
    global saving_in_progress, save_query_timer

    def save_query_task():
        while saving_in_progress:
            server.execute("save query")
            time.sleep(1)

    save_query_thread = threading.Thread(target=save_query_task)
    save_query_thread.daemon = True
    save_query_thread.start()


def stop_save_query_loop():
    global saving_in_progress
    saving_in_progress = False


def on_info(server, info):
    global saving_in_progress, save_query_timer

    if not info.is_user:
        if info.content == 'Saving...':
            if not saving_in_progress:
                saving_in_progress = True
                start_save_query_loop(server)
        elif saving_in_progress and 'Data saved. Files are now ready to be copied.' in info.content:
            stop_save_query_loop()