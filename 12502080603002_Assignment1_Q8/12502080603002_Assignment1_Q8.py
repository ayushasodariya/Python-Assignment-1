import os
import re
import pickle
import zipfile


def normalize_words(line):
    """Return lowercase words from a log line."""
    return re.findall(r"[a-zA-Z0-9]+", line.lower())


def build_index(folder_path, zip_name):
    """Read log files, create the index and compress the files."""

    if not os.path.isdir(folder_path):
        print("Folder not found.")
        return

    index = {}
    total_files = 0
    total_lines = 0

    # Read every text file in the selected folder.
    for file_name in sorted(os.listdir(folder_path)):

        if not file_name.lower().endswith(".txt"):
            continue

        file_path = os.path.join(folder_path, file_name)
        total_files += 1

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    total_lines += 1

                    words = normalize_words(line)

                    for word in words:
                        # Avoid storing the same file/line twice
                        # when a word occurs multiple times in one line.
                        location = (file_name, line_number)

                        if word not in index:
                            index[word] = []

                        if location not in index[word]:
                            index[word].append(location)

        except OSError as error:
            print(f"Could not read {file_name}: {error}")

    if total_files == 0:
        print("No .txt log files found.")
        return

    # Save the inverted index using pickle.
    index_file = os.path.join(folder_path, "log_index.pkl")

    try:
        with open(index_file, "wb") as file:
            pickle.dump(index, file)
    except OSError as error:
        print("Could not save index:", error)
        return

    # Put all log files and the index into one ZIP archive.
    try:
        with zipfile.ZipFile(
            zip_name, "w", zipfile.ZIP_DEFLATED
        ) as archive:

            for file_name in sorted(os.listdir(folder_path)):
                file_path = os.path.join(folder_path, file_name)

                if file_name.endswith(".txt") or file_name == "log_index.pkl":
                    archive.write(file_path, arcname=file_name)

    except OSError as error:
        print("Could not create ZIP file:", error)
        return

    print("FILES", total_files)
    print("LINES", total_lines)
    print("TOKENS", len(index))


def search_index(index_path, queries):
    """Load the saved index and display locations of requested words."""

    if not os.path.isfile(index_path):
        print("Index file not found.")
        return

    try:
        with open(index_path, "rb") as file:
            index = pickle.load(file)
    except (OSError, pickle.PickleError):
        print("Could not load index.")
        return

    for query in queries:
        word = query.lower()

        if word in index:
            locations = sorted(index[word])

            print(word + ":")
            for file_name, line_number in locations:
                print(f"{file_name}:{line_number}")
        else:
            print(word + ": NOT FOUND")


def main():
    print("BUILD <folder> <zip_name>")
    print("SEARCH <pickle_path> <number_of_words> <words...>")
    print("Type quit to exit.")

    while True:
        try:
            command = input("> ").strip()

            if command.lower() == "quit":
                break

            parts = command.split()

            if not parts:
                print("Invalid input.")
                continue

            mode = parts[0].upper()

            if mode == "BUILD":

                if len(parts) != 3:
                    print("Usage: BUILD folder archive.zip")
                    continue

                folder = parts[1]
                zip_name = parts[2]

                build_index(folder, zip_name)

            elif mode == "SEARCH":

                if len(parts) < 3:
                    print(
                        "Usage: SEARCH pickle_path q word1 word2 ..."
                    )
                    continue

                index_path = parts[1]

                try:
                    q = int(parts[2])
                except ValueError:
                    print("Number of queries must be an integer.")
                    continue

                queries = parts[3:]

                if q <= 0 or len(queries) != q:
                    print("Invalid number of query words.")
                    continue

                search_index(index_path, queries)

            else:
                print("Unknown mode.")

        except KeyboardInterrupt:
            print("\nProgram stopped.")
            break


if __name__ == "__main__":
    main()