import json

class Queue:

    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Error: Cannot dequeue from an empty Queue.")
        return self._items.pop(0)

    def enqueue_emergency(self, item):
        item.status = "Emergency Pending"
        self._items.insert(0, item)

    def front(self):

        if self.is_empty():
            return None
        return self._items[0]

    def is_empty(self):
        return len(self._items) ==0

    def size(self):
        return len(self._items)

    def get_all(self):
         return list(self._items)


class Stack:

    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Error: Cannot pop from an empty Stack.")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)
    def get_all(self):
        return list(self.items)


class HashTable:

    def __init__(self, capacity=10):
        self.capacity = capacity
        self.buckets = [[] for i in range(self.capacity)]

    def hashing(self, key):
        return int(key) % self.capacity

    def put(self, key, value):
        index = self.hashing(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] =(key, value)
                return

        bucket.append((key, value))

    def get(self, key):
        index = self.hashing(key)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v
        return None



def bubble_sort(arr, key_func=lambda x: x):
    data = list(arr)
    n = len(data)
    comparisons =0
    swaps =0

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if key_func(data[j]) > key_func(data[j + 1]):
                data[j], data[j + 1] = data[j + 1], data[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return data,comparisons,swaps
def create_test_datasets(data):
    sorted_data, _, _ = bubble_sort(data, lambda r: r.request_id)

    reverse_data = list(reversed(sorted_data))

    nearly_data = list(sorted_data)
    if len(nearly_data) >= 2:
        nearly_data[0], nearly_data[1] = nearly_data[1], nearly_data[0]

    random_data = list(data)

    import random
    random.shuffle(random_data)

    return {
        "Already Sorted": sorted_data,
        "Reverse Sorted": reverse_data,
        "Nearly Sorted": nearly_data,
        "Random Order": random_data}

def selection_sort(arr, key_func=lambda x: x):

    data = list(arr)
    n = len(data)
    comparisons = 0
    swaps = 0

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if key_func(data[j]) < key_func(data[min_idx]):
                min_idx = j

        if min_idx != i:
            data[i], data[min_idx] = data[min_idx], data[i]
            swaps += 1
    return data, comparisons, swaps


def insertion_sort(arr, key_func=lambda x: x):

    data = list(arr)
    n = len(data)
    comparisons = 0
    shifts =0

    for i in range(1, n):
        key_item = data[i]
        key_value = key_func(key_item)
        j = i - 1

        while j >= 0:
            comparisons += 1
            if key_func(data[j]) > key_value:
                data[j + 1] = data[j]
                shifts += 1
                j -= 1
            else:
                break
        data[j + 1] = key_item

    return data, comparisons, shifts

def smart_sort(arr, key_func=lambda x: x):
    data = list(arr)
    n = len(data)
    if n <= 1:
        return insertion_sort(data, key_func)

    inversions = 0
    for i in range(n - 1):
        if key_func(data[i]) > key_func(data[i + 1]):
            inversions += 1

    if inversions == 0 or inversions <= n // 3:
        print("\n[Smart Sort Notice]: Data is nearly/already sorted. Choosing Insertion Sort.")
        return insertion_sort(data, key_func)
    else:
        print("\n[Smart Sort Notice]: Data is unsorted. Choosing Selection Sort.")
        return selection_sort(data, key_func)

def sequential_search(arr, target_id):

    comparisons =0
    for index, item in enumerate(arr):
        comparisons += 1
        if item.request_id == target_id:
            return item, comparisons, index
    return None, comparisons, -1


def binary_search(sorted_arr, target_id):

    low =0
    high = len(sorted_arr) -1
    comparisons =0

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1

        mid_id = sorted_arr[mid].request_id

        if mid_id == target_id:
            return sorted_arr[mid], comparisons, mid
        elif mid_id < target_id:
            low = mid + 1
        else:
            high = mid - 1

    return None, comparisons, low


class Request:
    def __init__(self, request_id, customer_name, priority, estimated_time, status="Pending"):
        self.request_id = int(request_id)
        self.customer_name = str(customer_name).strip()
        self.priority = int(priority)
        self.estimated_time = int(estimated_time)
        self.status = str(status).strip()

    def show_request(self):
        return f"Request(ID={self.request_id},Name='{self.customer_name}',Priority={self.priority},Time={self.estimated_time}m,Status='{self.status}')"

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "customer_name": self.customer_name,
            "priority": self.priority,
            "estimated_time": self.estimated_time,
            "status": self.status}



def validate_request_data(request_id, customer_name, priority, estimated_time, existing_ids):

    try:
        req_id = int(request_id)
        if req_id <= 0:
            return False, "Error: Request ID must be a positive integer."
        if req_id in existing_ids:
            return False, f"Error: Request ID {req_id} already exists."
    except ValueError:
        return False, "Error: Invalid Request ID format."

    if not str(customer_name).strip():
        return False, "Error: Customer name cannot be empty."


    try:
        prio = int(priority)
        if prio < 1 or prio > 5:
            return False, "Error: Priority must be between 1 and 5."
    except ValueError:
        return False, "Error: Priority must be an integer."


    try:
        est_time = int(estimated_time)
        if est_time <= 0:
            return False, "Error: Estimated time must be greater than 0."
    except ValueError:
        return False, "Error: Estimated time must be an integer."
    return True, "Valid"




JSON_FILE = "Service_Center_Data_Pack.json"

def create_request_from_dict(data):
    return Request(
        request_id=data.get("request_id") or data.get("Request ID"),
        customer_name=data.get("customer_name") or data.get("Customer Name"),
        priority=data.get("priority") or data.get("Priority"),
        estimated_time=data.get("estimated_time") or data.get("Estimated Time"),
        status=data.get("status") or data.get("Status", "Pending"))


def save_to_json(waiting_queue, processed_requests, search_stack):
    data = {
        "Requests Dataset": [req.to_dict() for req in waiting_queue.get_all()],
        "processed_requests": [req.to_dict() for req in processed_requests],
        "search_history": search_stack.get_all() }
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_from_json():
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

            raw_waiting = data.get("Requests Dataset") or data.get("waiting_queue", [])
            waiting = [create_request_from_dict(d) for d in raw_waiting]

            processed = [create_request_from_dict(d) for d in data.get("processed_requests", [])]
            history = data.get("search_history", [])

            return waiting, processed, history
    except FileNotFoundError:
        print(f"Notice: File '{JSON_FILE}' not found. Starting fresh.")
        return [], [], []
    except Exception as e:
        print(f"Error reading {JSON_FILE}: {e}")
        return [], [], []




def display_menu():
    print("\n" + "="*45)
    print("   SMART SERVICE CENTER ENGINE - MAIN MENU   ")
    print("="*45)
    print("1. Add Incoming Request")
    print("2. Process Next Request")
    print("3. Show Waiting Queue")
    print("4. Show Processed Requests")
    print("5. Sort Processed Requests")
    print("6. Search Requests")
    print("7. View / Remove Last Search")
    print("8. Show Algorithm Statistics")
    print("0. Exit")
    print("="*45)




def main():
    waiting_queue = Queue()
    search_history_stack = Stack()
    hash_table = HashTable(capacity=20)

    processed_requests = []
    existing_ids = set()
    loaded_waiting, loaded_processed, loaded_history = load_from_json()

    if loaded_waiting or loaded_processed:
        for req in loaded_waiting:
            waiting_queue.enqueue(req)
            existing_ids.add(req.request_id)

        for req in loaded_processed:
            processed_requests.append(req)
            hash_table.put(req.request_id, req)
            existing_ids.add(req.request_id)

        for h in loaded_history:
            search_history_stack.push(h)

        print(f"Loaded existing state from '{JSON_FILE}'.")


    while True:
        display_menu()
        choice = input("Enter choice (0-8): ").strip()

        if choice == "1":
            print("\n--- Add Request ---")
            is_emergency = input("Is this an Emergency Request? (y/n): ").strip().lower() == 'y'
            req_id = input("ID: ")
            name = input("Name: ")
            prio = input("Priority (1-5): ")
            time_est = input("Estimated Time (mins): ")

            is_valid, msg = validate_request_data(req_id, name, prio, time_est, existing_ids)
            if is_valid:
                req = Request(req_id, name, prio, time_est)
                if is_emergency:
                    waiting_queue.enqueue_emergency(req)
                    print("Emergency Request added at the front of the queue!")
                else:
                    waiting_queue.enqueue(req)
                    print("Request added successfully!")
                existing_ids.add(req.request_id)
                save_to_json(waiting_queue, processed_requests, search_history_stack)
            else:
                print(msg)


        elif choice == "2":
            if waiting_queue.is_empty():
                print("Queue is empty!")
            else:
                req = waiting_queue.dequeue()
                req.status = "Processed"
                processed_requests.append(req)
                hash_table.put(req.request_id, req)
                save_to_json(waiting_queue, processed_requests, search_history_stack)
                print(f"Processed: {req.show_request()} (State updated)")

        elif choice == "3":
            print("\n--- Waiting Queue ---")
            if waiting_queue.is_empty():
                print("Queue is empty.")
            else:
                for req in waiting_queue.get_all():
                    print(req.show_request())

        elif choice == "4":
            print("\n--- Processed Requests ---")
            if not processed_requests:
                print("No processed requests yet.")
            else:
                for req in processed_requests:
                    print(req.show_request())

        elif choice == "5":
            if not processed_requests:
                print("No processed requests to sort.")
                continue

            print("\nSort by: 1. ID | 2. Priority | 3. Time")
            f_choice = input("Field: ")
            key_f = lambda r: r.request_id
            field_name = "Request ID"

            if f_choice == "2":
                key_f = lambda r: r.priority
                field_name = "Priority"

            elif f_choice == "3":
                key_f = lambda r: r.estimated_time
                field_name = "Estimated Time"

            print("Algorithm: 1. Bubble | 2. Selection | 3. Insertion | 4. Smart Sort ")
            a_choice = input("Algo: ")
            print(f"Sorted By: {field_name}")

            if a_choice == "1":
                res, comps, swaps = bubble_sort(processed_requests, key_f)
                print(f"Bubble Sort - Comparisons: {comps}, Swaps: {swaps}")
            elif a_choice == "2":
                res, comps, swaps = selection_sort(processed_requests, key_f)
                print(f"Selection Sort - Comparisons: {comps}, Swaps: {swaps}")
            elif a_choice == "3":
                res, comps, shifts = insertion_sort(processed_requests, key_f)
                print(f"Insertion Sort - Comparisons: {comps}, Shifts: {shifts}")
            elif a_choice == "4":
                res, comps, ops = smart_sort(processed_requests, key_f)
                print(f"Smart Sort Completed - Comparisons: {comps}, Swaps/Shifts: {ops}")
            else:
                print("Invalid choice.")
                continue

            processed_requests = res
            save_to_json(waiting_queue, processed_requests, search_history_stack)

            print("\n--- Sorted Results ---")
            for r in processed_requests:
                print(r.show_request())


        elif choice == "6":

            if not processed_requests:
                print("No processed requests to search.")
                continue

            print("Search Method: 1. Sequential | 2. Binary | 3. Hash Table | 4. Hash Collision Demo")
            m_choice = input("Method: ")

            if m_choice == "4":
                print("\n---  Hash Collision Handling  ---")
                cap = hash_table.capacity
                demo_id1 = 10
                demo_id2 = 10 + cap
                idx1 = hash_table.hashing(demo_id1)
                idx2 = hash_table.hashing(demo_id2)
                print(f"Key {demo_id1} % {cap} = Index {idx1}")
                print(f"Key {demo_id2} % {cap} = Index {idx2}")
                print(f"Collision Demo: Both IDs map to index {idx1}. Handled via Bucket Chaining List.")
                continue
            try:
                target = int(input("Target ID: "))
            except ValueError:
                print("Invalid ID format.")
                continue

            if m_choice == "1":
                res, comps, idx = sequential_search(processed_requests, target)
                status = "Found" if res else "Not Found"
                print(f"Result: {status} | Comparisons: {comps} | Index: {idx}")
                search_history_stack.push({"target": target, "method": "Sequential", "result": status, "comps": comps})

            elif m_choice == "2":
                sorted_reqs, _, _ = bubble_sort(processed_requests, lambda r: r.request_id)
                res, comps, pos = binary_search(sorted_reqs, target)
                status = "Found" if res else "Not Found"
                print(f"Result: {status} | Comparisons: {comps} | Index/Insert Pos: {pos}")
                search_history_stack.push({"target": target, "method": "Binary", "result": status, "comps": comps})

            elif m_choice == "3":
                res = hash_table.get(target)
                status = "Found" if res else "Not Found"
                print(f"Result: {status} | Direct Hash Lookup")
                search_history_stack.push({"target": target, "method": "HashTable", "result": status, "comps": 1})

            if res:
                print(f"Request Details: {res.show_request()}")
            else:
                print(f"No request found with ID: {target}")
            save_to_json(waiting_queue, processed_requests, search_history_stack)

        elif choice == "7":
            print("\n1. View Last Search | 2. Remove Last Search")
            s_choice = input("Choice: ")
            if s_choice == "1":
                print(f"Last Search: {search_history_stack.peek()}")
            elif s_choice == "2":
                try:
                    removed = search_history_stack.pop()
                    save_to_json(waiting_queue, processed_requests, search_history_stack)
                    print(f"Removed: {removed}")
                except IndexError as e:
                    print(e)



        elif choice == "8":
            print("\n" + "=" * 40)
            print("      BENCHMARK & STATISTICS REPORT      ")
            print("=" * 40)
            print(f"Waiting Queue Size: {waiting_queue.size()}")
            print(f"Processed Requests: {len(processed_requests)}")
            print(f"Search History Stack Size: {search_history_stack.size()}")

            if processed_requests:
                datasets = create_test_datasets(processed_requests)
                for dataset_name, dataset in datasets.items():
                    print("\n" + "-" * 40)
                    print(f"Dataset: {dataset_name}")
                    print("-" * 40)
                    b, bc, bs = bubble_sort(dataset,lambda r: r.request_id)
                    s, sc, ss = selection_sort(dataset,lambda r: r.request_id)
                    i, ic, ish = insertion_sort(dataset,lambda r: r.request_id)
                    print(f"Bubble Sort    : {bc} Comparisons, {bs} Swaps")
                    print(f"Selection Sort : {sc} Comparisons, {ss} Swaps")
                    print(f"Insertion Sort : {ic} Comparisons, {ish} Shifts")

            print("=" * 40)

        elif choice == "0":
            save_to_json(waiting_queue, processed_requests, search_history_stack)
            print("All changes saved. Exiting... Goodbye!")
            break

main()