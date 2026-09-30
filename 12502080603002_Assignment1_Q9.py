import heapq
import threading


class Job:
    def __init__(self, arrival, job_id, priority, duration, resources, order):
        self.arrival = arrival
        self.job_id = job_id
        self.priority = priority
        self.duration = duration
        self.resources = resources
        self.order = order


def read_jobs(n):
    """Read and validate all job information."""
    jobs = []

    for i in range(n):
        parts = input().split()

        if len(parts) != 5:
            raise ValueError("Each job needs 5 values")

        try:
            arrival = int(parts[0])
            job_id = parts[1]
            priority = int(parts[2])
            duration = int(parts[3])
            resources = int(parts[4])
        except ValueError:
            raise ValueError("Invalid numeric value in job")

        if arrival < 0:
            raise ValueError("Arrival time cannot be negative")

        if not job_id:
            raise ValueError("Job ID cannot be empty")

        if duration <= 0:
            raise ValueError("Duration must be positive")

        if resources <= 0:
            raise ValueError("Resources must be positive")

        jobs.append(
            Job(
                arrival,
                job_id,
                priority,
                duration,
                resources,
                i
            )
        )

    return jobs


def worker_function(worker_id, assigned_jobs, report, lock):
    """
    Simulate a worker processing its assigned jobs.

    The actual duration is represented by simulated start/finish
    times, so the program does not need to sleep for real time.
    """
    for job, start_time in assigned_jobs:
        finish_time = start_time + job.duration
        waiting_time = start_time - job.arrival

        result = (
            job.job_id,
            worker_id,
            start_time,
            finish_time,
            waiting_time
        )

        # Several worker threads may update the report at once.
        with lock:
            report.append(result)


def schedule_jobs(workers, jobs):
    """Create the worker schedule using priority-based simulation."""

    jobs.sort(key=lambda job: (job.arrival, job.order))

    # Jobs waiting to be assigned.
    # Higher priority is represented by negative priority.
    waiting = []

    # Workers currently busy: (finish_time, worker_number)
    busy_workers = []

    # Workers that are free.
    free_workers = list(range(1, workers + 1))
    heapq.heapify(free_workers)

    assigned = {i: [] for i in range(1, workers + 1)}

    job_index = 0
    current_time = 0

    while job_index < len(jobs) or waiting or busy_workers:

        # Add newly arrived jobs to the priority queue.
        if job_index < len(jobs):
            next_arrival = jobs[job_index].arrival

            if not waiting and not free_workers:
                current_time = max(
                    current_time,
                    min(next_arrival, busy_workers[0][0])
                )
            elif not waiting:
                current_time = max(current_time, next_arrival)

        # Move finished workers back to the free list.
        while busy_workers and busy_workers[0][0] <= current_time:
            finish_time, worker_id = heapq.heappop(busy_workers)
            heapq.heappush(free_workers, worker_id)

        # Add every job that has arrived by current time.
        while (
            job_index < len(jobs)
            and jobs[job_index].arrival <= current_time
        ):
            job = jobs[job_index]

            heapq.heappush(
                waiting,
                (-job.priority, job.arrival, job.order, job)
            )

            job_index += 1

        # If no worker is free, move time to the next worker completion.
        if not free_workers and waiting:
            current_time = busy_workers[0][0]
            continue

        # If nothing is waiting, jump to the next job arrival.
        if not waiting:
            if job_index < len(jobs):
                current_time = max(
                    current_time,
                    jobs[job_index].arrival
                )
                continue
            break

        # Assign jobs to available workers.
        while free_workers and waiting:
            worker_id = heapq.heappop(free_workers)

            _, _, _, job = heapq.heappop(waiting)

            start_time = max(current_time, job.arrival)
            finish_time = start_time + job.duration

            assigned[worker_id].append(
                (job, start_time)
            )

            heapq.heappush(
                busy_workers,
                (finish_time, worker_id)
            )

    return assigned


def run_workers(assigned):
    """Start worker threads and collect their execution reports."""

    report = []
    lock = threading.Lock()
    threads = []

    for worker_id in sorted(assigned):
        thread = threading.Thread(
            target=worker_function,
            args=(
                worker_id,
                assigned[worker_id],
                report,
                lock
            )
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return report


def main():
    try:
        first_line = input().split()

        if len(first_line) != 2:
            raise ValueError("First line must contain w and n")

        workers = int(first_line[0])
        n = int(first_line[1])

        if workers < 1 or workers > 64:
            raise ValueError("Workers must be between 1 and 64")

        if n < 1 or n > 200000:
            raise ValueError("Number of jobs is invalid")

        jobs = read_jobs(n)

        assigned = schedule_jobs(workers, jobs)

        report = run_workers(assigned)

        # Display jobs in their original input order.
        report.sort(
            key=lambda item: next(
                job.order for job in jobs
                if job.job_id == item[0]
            )
        )

        total_wait = 0

        for job_id, worker_id, start, finish, wait in report:
            print(
                job_id,
                f"W{worker_id}",
                start,
                finish
            )
            total_wait += wait

        average_wait = total_wait / len(report)

        print(f"AVG_WAIT {average_wait:.2f}")

    except ValueError as error:
        print("INPUT ERROR:", error)


if __name__ == "__main__":
    main()