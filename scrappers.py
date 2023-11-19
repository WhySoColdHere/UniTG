def get_institutes(element):
    raw_institutes = " ".join(element.split()[2:])
    indexes = []
    completed_institutes = []

    for letter in range(len(raw_institutes)):
        if raw_institutes[letter].isupper():
            indexes.append(letter)
    for i in range(len(indexes)):
        try:
            completed_institutes.append(raw_institutes[indexes[i]: indexes[i + 1]])
        except IndexError:
            completed_institutes.append(raw_institutes[indexes[i]:])

    return completed_institutes
