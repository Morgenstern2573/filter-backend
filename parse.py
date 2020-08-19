import xlrd
import sqlite3
import json


def main(input_file=None):
    raw_data = xlrd.open_workbook(input_file)
    today = ""
    days = ["tuesday", "monday", "wednesday", "thursday", "friday"]
    time_map = None
    output = dict()

    sheet = raw_data.sheet_by_index(0)
    rows = []

    for row_index in range(sheet.nrows):
        rows.append(sheet.row(row_index))
    # create mapping of column indices to time intervals
    for index, row in enumerate(rows):
        b = row[0].value.lower().strip()
        if b in days:
            if time_map is None:
                time_map = dict()
                for i in range(2, len(rows[index + 1])):
                    time_map[i] = rows[index + 1][i].value
                break

  # actually process data
    for index, row in enumerate(rows):
        b = row[0].value.lower().strip()
        if b == "" or b == "venue":
            continue
        elif b in days:
            today = b
            continue
        else:
            for i in range(2, len(row)):
                content = row[i].value.strip()
                codes = content.split("/")
                if len(codes) == 1:
                    content = codes[0]
                    if content != "":
                        if not content in output:
                            output[content] = [[today,
                                                time_map[i], (row[0].value +
                                                              ", " + row[1].value)]]

                        else:
                            output[content].append([today, time_map[i],
                                                    (row[0].value + ", " + row[1].value)])
                else:
                    pre = codes[0].split(" ")[0]
                    codes[1] = pre + " " + codes[1]
                    for code in codes:
                        content = code
                        if content != "":
                            if not content in output:
                                output[content] = [[today,
                                                    time_map[i], (row[0].value +
                                                                  ", " + row[1].value)]]

                            else:
                                output[content].append([today, time_map[i],
                                                        (row[0].value + ", " + row[1].value)])

    con = sqlite3.connect('./db.sqlite')
    cur = con.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS timetable;

        CREATE TABLE timetable(
            'course_code' TEXT UNIQUE NOT NULL,
            'loctime' TEXT NOT NULL
        );
    """)

    con.commit()

    for k, v in output.items():
        cur.execute(
            'INSERT INTO timetable (course_code, loctime) VALUES (?, ?)', (k, json.dumps(v)))

    con.commit()
    con.close()


if __name__ == "__main__":
    main('./sample2.xls')
