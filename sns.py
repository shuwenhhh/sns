import queue
import threading
import time
import random

# prodcer, generate message
def producer(message_queue, num_messages):
    for i in range(num_messages):
        message = f"Emergency Alert {i}"
        message_queue.put(message)

# sender, send message
def sender(message_queue, failure_rate, mean_processing_time):
    while not message_queue.empty():
        message = message_queue.get()
        if random.random() > failure_rate:
            time.sleep(random.expovariate(1 / mean_processing_time))  # imitate the processing time
        else:
            print(f"Message failed to send: {message}")

# progress monitor, monitor the progress
def progress_monitor(message_queue, num_messages, start_time):
    while True:
        sent_messages = num_messages - message_queue.qsize()
        failed_messages = message_queue.unfinished_tasks - sent_messages
        average_time_per_message = (time.time() - start_time) / sent_messages if sent_messages > 0 else 0
        print(f"Messages sent: {sent_messages}, Messages failed: {failed_messages}, Average time per message: {average_time_per_message:.2f} seconds")
        time.sleep(5)  # update the progress every 5 seconds

if __name__ == "__main__":
    num_messages = 1000
    failure_rate = 0.1
    mean_processing_time = 5  # average processing time for each message

    message_queue = queue.Queue()
    start_time = time.time()

    producer_thread = threading.Thread(target=producer, args=(message_queue, num_messages))
    producer_thread.start()

    sender_threads = []
    for i in range(5):  
        sender_thread = threading.Thread(target=sender, args=(message_queue, failure_rate, mean_processing_time))
        sender_threads.append(sender_thread)
        sender_thread.start()

    progress_monitor_thread = threading.Thread(target=progress_monitor, args=(message_queue, num_messages, start_time))
    progress_monitor_thread.start()
