from abc import ABC, abstractmethod

# 2.1 & 2.2: แก้ไข Class Task ให้มี priority และแสดงผลใน __str__
class Task:
    # เพิ่มรับค่า priority (กำหนดค่าเริ่มต้นเป็น "medium")
    def __init__(self, task_id, description, priority="medium", due_date=None, completed=False):
        self.id = task_id
        self.description = description
        self.priority = priority # เพิ่ม Attribute priority
        self.due_date = due_date
        self.completed = completed

    def mark_completed(self):
        self.completed = True
        print(f"Task {self.id} '{self.description}' marked as completed.")

    def __str__(self):
        status = "✔" if self.completed else " "
        due = f" (Due: {self.due_date})" if self.due_date else ""
        # เพิ่มการแสดงผล priority
        priority_str = f" [Priority: {self.priority.upper()}]"
        return f"[{status}] {self.id}. {self.description}{priority_str}{due}"

class TaskStorage(ABC):
    @abstractmethod 
    def load_tasks(self):
        pass
        
    @abstractmethod
    def save_tasks(self, tasks):
        pass

class FileTasksStorage(TaskStorage):
    def __init__(self, filename="tasks.txt"):
        self.filename = filename

    def load_tasks(self):
        loaded_tasks = []
        try:
            with open(self.filename, "r") as f:
                for line in f:
                    parts = line.strip().split(',')
                    # ปรับปรุงให้รองรับข้อมูลทั้งแบบเก่า (4 ส่วน) และแบบใหม่ที่รวม priority แล้ว (5 ส่วน)
                    if len(parts) >= 4:
                        task_id = int(parts[0])
                        description = parts[1]
                        
                        # เช็คว่าไฟล์มี priority หรือไม่ (ถ้าเป็นไฟล์ใหม่จะมี 5 ส่วน)
                        if len(parts) == 5:
                            priority = parts[2]
                            due_date = parts[3] if parts[3] != 'None' else None
                            completed = parts[4] == 'True'
                        else:
                            priority = "medium" # ข้อมูลเก่าให้เป็น medium
                            due_date = parts[2] if parts[2] != 'None' else None
                            completed = parts[3] == 'True'
                            
                        loaded_tasks.append(Task(task_id, description, priority, due_date, completed))
        except FileNotFoundError:
            print(f"No existing task file '{self.filename}' found. Starting fresh.")
        return loaded_tasks
        
    def save_tasks(self, tasks):
        with open(self.filename, "w") as f:
            for task in tasks:
                # เพิ่ม task.priority ลงไปตอนเซฟไฟล์ด้วย
                f.write(f"{task.id},{task.description},{task.priority},{task.due_date},{task.completed}\n")
        print(f"Tasks saved to {self.filename}")

class TaskManager:
    def __init__(self, storage: TaskStorage):
        self.storage = storage
        self.tasks = self.storage.load_tasks()
        
        self.next_id = max([t.id for t in self.tasks] + [0]) + 1 if self.tasks else 1
        print(f"Loaded {len(self.tasks)} tasks. Next ID: {self.next_id}")

    # 2.3: แก้ไข add_task ให้รับค่า priority
    def add_task(self, description, priority="medium", due_date=None):
        # ส่ง priority เข้าไปตอนสร้าง Task
        task = Task(self.next_id, description, priority, due_date)
        self.tasks.append(task)
        self.next_id += 1
        self.storage.save_tasks(self.tasks)
        print(f"Task '{description}' (Priority: {priority}) added.")
        return task

    def list_tasks(self):
        print("\n--- Current Tasks ---")
        if not self.tasks:
            print("No tasks available.")
            return
        for task in self.tasks:
            print(task)
        print("---------")

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def mark_task_completed(self, task_id):
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_completed()
            self.storage.save_tasks(self.tasks)
            return True
        print(f"Task {task_id} not found.")
        return False

# ทดสอบ Logic หลัก
if __name__ == "__main__":
    file_storage = FileTasksStorage("my_tasks.txt")
    manager = TaskManager(file_storage)
    
    # ทดลองสร้าง Task แบบกำหนด Priority
    manager.add_task("Review SOLID Principles", priority="high", due_date="2024-08-10")
    manager.add_task("Prepare for Final Exam", priority="medium", due_date="2024-08-15")
    manager.add_task("Buy groceries", priority="low") # ไม่ใส่ due_date
    manager.list_tasks()

    print("Finshed")