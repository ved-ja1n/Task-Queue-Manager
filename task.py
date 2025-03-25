import json
import threading
import csv
from mail import send_gmail

class Queue():
    def __init__ (self, queue):
        self.queue = []
        self.load_tasks()
        if queue:
            self.queue.extend(queue)

    def add_task(self, task, *args, priority = False):
        if priority:
            self.queue.insert(0, (task, args))
        else:
            self.queue.append((task, args))

        self.save_tasks()

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        return None
    
    def tasks_remaining(self):
        return len(self.queue)
    
    def do_task(self):
        self.save_tasks()

        if not self.tasks_remaining():
            print("No tasks left to process.")
            return

        task, args = self.dequeue()
        if task == 'send-email':
            send_gmail(*args)
            print(f"Successful doing: {task} - {args}")
        else:
            print(f"Unknown task: {task}. Skipping.")

    def save_tasks(self, file_name = 'tasks.json'):
        with open(file_name, 'w') as file:
            json.dump(self.queue, file)

    def load_tasks(self, file_name = 'tasks.json'):
        try:
            with open(file_name, 'r') as file:
                self.queue = json.load(file)
        except FileNotFoundError:
            pass


if __name__ == '__main__':

    queue = Queue([])

    while True:
        print("\n--- Task Queue Manager ---")
        print("1. Add Send Email Task")
        print("2. Add Bulk Email Task")
        print("3. View Tasks Remaining")
        print("4. Process Tasks")
        print("5. Exit")

        choice = int(input("Enter choice (1-4) : "))

        if choice == 1:
            sender = input("Enter sender's email : ")
            password = input("Enter app password for gmail : ")

            i = 0
            receiver_list = []
            while True:
                i+=1
                receiver = input(f"Enter recipient {i} email / enter 'e' to exit : ")
                if receiver == 'e':
                    break
                else:
                    receiver_list.append(receiver)
            
            subject = input("Enter subject of email : ")
            print("Make a txt file in same directory as program and enter body there")
            body_file = input("Enter file name : ")

            with open(body_file, 'r') as file:
                body = file.read()

            priority_input = input("Mark as priority? (y/n) : ")
            if priority_input == 'y':
                priority = True
            else:
                priority = False
            
            queue.add_task('send-email', sender, password, receiver_list, subject, body, priority=priority)
            print("Task added successfully")

        elif choice == 2:
            sender = input("Enter sender's email : ")
            password = input("Enter app password for gmail : ")

            print("Make a csv file in same directory as program and enter all recipients there")
            csv_file = input("Enter file name: ")
            receiver_list = []
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    email = row['email']
                    receiver_list.append(email)

            subject = input("Enter subject of email : ")
            print("Make a txt file in same directory as program and enter body there")
            body_file = input("Enter file name : ")

            with open(body_file, 'r') as file:
                body = file.read()

            priority_input = input("Mark as priority? (y/n) : ")
            if priority_input == 'y':
                priority = True
            else:
                priority = False

            queue.add_task('send-email', sender, password, receiver_list, subject, body, priority=priority)
            print("Task added succesfully")

        elif choice == 3:
            print(f"Tasks remaining : {queue.tasks_remaining()}")
        elif choice == 4:
            threading.Thread(target=queue.do_task, daemon=True).start()
        elif choice == 5:
            break

        else:
            print("Invalid choice. Please select a valid option.")
