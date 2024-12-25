from patient import Patient
from medical_test import MedicalTest
from datetime import datetime, timedelta
from statistics import mean
import csv


def display_menu():
    print()
    print("1. Add New Medical Test")
    print("2. Add New Medical Test Record")
    print("3. Update Patient Records")
    print("4. Update Medical Test")
    print("5. Filter Medical Tests")
    print("6. Generate Summary Reports")
    print("7. Export Medical Records")
    print("8. Import Medical Records")
    print("9. Print all Medical Tests")
    print("10. Print all Medical Records")
    print("11. Exit")


def read_medical_tests(file_path):
    tests = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split("; ")

            if len(parts) < 3:
                print(f"Error: Invalid format in line: {line}")
                continue

            name_abbr = parts[0].split(": ")[1]
            name = name_abbr.split(" (")[0].strip()
            abbr_name = name_abbr.split(" (")[1].split(")")[0].strip()

            range_part = parts[1].split(": ")[1]

            lower_range = None
            upper_range = None

            if ">" in range_part:
                lower_range = float(range_part.split("> ")[1].split(",")[0].strip())
            if "<" in range_part:
                upper_range = float(parts[1].split("< ")[1].strip())

            unit_part = parts[2].split(", ")[0]
            unit = unit_part.split(": ")[1].strip()

            turnaround_time = parts[2].split(", ")[1].strip()

            test = MedicalTest(name, abbr_name, lower_range, upper_range, unit, turnaround_time)
            tests[abbr_name] = test

    return tests


def read_medical_records(file_path, tests, patients):
    with open(file_path, 'r') as file:
        for line in file:
            try:
                patient_id, record_data = line.split(":", 1)
                patient_id = int(patient_id.strip())

                record_parts = record_data.strip().split(", ")

                abbr_name = record_parts[0].strip()
                test_date = datetime.strptime(record_parts[1].strip(), "%Y-%m-%d %H:%M")
                result_value = float(record_parts[2].strip())
                unit = record_parts[3].strip()
                status = record_parts[4].strip()
                result_date = None
                if len(record_parts) > 5:
                    result_date = datetime.strptime(record_parts[5].strip(), "%Y-%m-%d %H:%M")

                if abbr_name in tests:
                    test = tests[abbr_name]

                    record = {
                        "test": test,
                        "test_date": test_date.strftime("%Y-%m-%d %H:%M"),
                        "result_value": result_value,
                        "unit": unit,
                        "status": status,
                        "result_date": result_date.strftime("%Y-%m-%d %H:%M") if result_date else None
                    }

                    if patient_id not in patients:
                        patients[patient_id] = Patient(patient_id)

                    patients[patient_id].add_record(record)
                else:
                    print(f"Warning: Test '{abbr_name}' not found in the list of valid medical tests.")
            except Exception as e:
                print(f"Error processing line: {line}\nException: {e}")

    return patients


def print_all_medical_tests(tests):
    for test, test_items in tests.items():
        print(test_items)


def print_all_medical_records(patients):
    for patient_id, patient in patients.items():
        print(patient)


def is_valid_float(value):
    return value.replace('.', '', 1).isdigit()


def validate_turnaround_time(value):
    parts = value.split('-')
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        return False

    days, hours, minutes = map(int, parts)
    if not (0 <= hours < 24 and 0 <= minutes < 60):
        return False

    return True


def add_new_medical_test(tests, file_path):
    while True:
        name = input("Enter the full name of the test: ").strip()
        if name:
            break
        print("Test name cannot be empty. Please re-enter.")

    while True:
        abbr_name = input("Enter the abbreviated name of the test: ").strip()
        if abbr_name:
            if abbr_name not in tests:
                break
            else:
                print(f"Abbreviated name '{abbr_name}' already exists. Please enter a different abbreviation.")
        else:
            print("Abbreviated name cannot be empty. Please re-enter.")

    while True:
        lower_range = input("Enter the lower range value (or leave empty if not applicable): ").strip()
        upper_range = input("Enter the upper range value (or leave empty if not applicable): ").strip()
        if lower_range or upper_range:
            if (not lower_range or is_valid_float(lower_range)) and (not upper_range or is_valid_float(upper_range)):
                lower_range = float(lower_range) if lower_range else None
                upper_range = float(upper_range) if upper_range else None
                if lower_range is None or upper_range is None or lower_range < upper_range:
                    break
                else:
                    print("Lower range must be less than upper range. Please re-enter both values.")
            else:
                print("Invalid range values. Please ensure they are valid floats.")
        else:
            print("Invalid Input, Lower and Upper ranges can't be both null")

    while True:
        unit = input("Enter the unit of the test: ").strip()
        if unit:
            break
        print("Unit cannot be empty. Please re-enter.")

    while True:
        turnaround_time = input("Enter the turnaround time (format DD-hh-mm): ").strip()
        if validate_turnaround_time(turnaround_time):
            break
        print("Invalid turnaround time. It should be in the format DD-hh-mm with only numbers. Please re-enter.")

    test = MedicalTest(name, abbr_name, lower_range, upper_range, unit, turnaround_time)
    tests[abbr_name] = test

    with open(file_path, 'a') as file:
        file.write(test.to_file_string())

    print(f"Medical test '{name}' successfully added.")


def add_new_medical_test_record(tests, patients, file_path):
    while True:
        patient_id = input("Enter the Patient ID (7-digit number): ").strip()
        if patient_id.isdigit() and len(patient_id) == 7:
            patient_id = int(patient_id)
            break
        else:
            print("Invalid Patient ID. It must be a 7-digit number. Please re-enter.")

    while True:
        abbr_name = input("Enter the test abbreviation: ").strip()
        if abbr_name in tests:
            test = tests[abbr_name]
            break
        else:
            print(f"Invalid test abbreviation. Please enter a valid one from the following: {', '.join(tests.keys())}.")

    while True:
        try:
            test_date = input("Enter the test date (format YYYY-MM-DD HH:MM): ").strip()
            test_date_obj = datetime.strptime(test_date,
                                              "%Y-%m-%d %H:%M")  # used to parse the input string into a datetime object
            if datetime(2000, 1, 1) <= test_date_obj <= datetime.now():
                break
            else:
                print("Test date must be between 2000-01-01 and today. Please re-enter.")
        except ValueError:
            print("Invalid date format. Please re-enter in the format YYYY-MM-DD HH:MM.")

    unit = test.unit
    while True:
        result_value = input(f"Enter the result value (float) for the test {abbr_name}: ").strip()
        if is_valid_float(result_value):
            result_value = float(result_value)
            break
        else:
            print("Invalid result value. Please enter a valid float number.")

    valid_statuses = ["pending", "completed", "reviewed"]
    while True:
        status = input("Enter the status (Pending, Completed, Reviewed): ").strip().lower()
        if status in valid_statuses:
            break
        else:
            print("Invalid status. Please enter one of the following: Pending, Completed, Reviewed.")

    result_date_obj = None

    if status == "Completed":
        turnaround_days, turnaround_hours, turnaround_minutes = map(int, test.turnaround_time.split('-'))
        min_result_date = test_date_obj + timedelta(days=turnaround_days, hours=turnaround_hours,
                                                    minutes=turnaround_minutes)
        while True:
            try:
                result_date = input(
                    f"Enter the result date (format YYYY-MM-DD HH:MM, after {min_result_date}): ").strip()
                result_date_obj = datetime.strptime(result_date, "%Y-%m-%d %H:%M")
                if min_result_date <= result_date_obj <= datetime.now():
                    break
                else:
                    print(f"Result date must be after {min_result_date} and before now. Please re-enter.")
            except ValueError:
                print("Invalid date format. Please re-enter in the format YYYY-MM-DD HH:MM.")

    record = {
        "test": test,
        "test_date": test_date_obj.strftime("%Y-%m-%d %H:%M"),
        "result_value": result_value,
        "unit": unit,
        "status": status,
        "result_date": result_date_obj.strftime("%Y-%m-%d %H:%M") if result_date_obj else None
    }

    if patient_id not in patients:
        patients[patient_id] = Patient(patient_id)
    patients[patient_id].add_record(record)

    with open(file_path, 'a') as file:
        file.write(f"\n{patient_id}: {abbr_name}, {record['test_date']}, {result_value}, {unit}, {status}")
        if status == "Completed":
            file.write(f", {record['result_date']}")

    print("New medical test record successfully added.")


def update_patient_records(patients, tests, file_path):
    while True:
        patient_id = input("Enter the Patient ID to update records: ").strip()
        if patient_id.isdigit() and int(patient_id) in patients:
            patient_id = int(patient_id)
            patient = patients[patient_id]
            break
        else:
            print("Invalid Patient ID. Please enter a valid Patient ID.")

    print("\nPatient Records:")
    for i, record in enumerate(patient.records, 1):
        print(f"{i}. Test: {record['test'].abbr_name}, Date: {record['test_date']}, "
              f"Result: {record['result_value']} {record['unit']}, Status: {record['status']}, "
              f"Result Date: {record['result_date']}")

    while True:
        record_number = input("Enter the number of the record you want to update: ").strip()
        if record_number.isdigit() and 1 <= int(record_number) <= len(patient.records):
            record_number = int(record_number) - 1
            selected_record = patient.records[record_number]
            break
        else:
            print("Invalid selection. Please enter a valid record number.")

    if input("Do you want to edit the Test Abbreviation? (Y/n): ").strip().lower() == 'y':
        while True:
            abbr_name = input("Enter the new test abbreviation: ").strip()
            if abbr_name in tests:
                selected_record['test'].abbr_name = abbr_name
                selected_record['unit'] = tests[abbr_name].unit
                break
            else:
                print("Invalid test abbreviation. Please re-enter.")

    if input("Do you want to edit the Test Date? (Y/n): ").strip().lower() == 'y':
        while True:
            try:
                new_test_date = input("Enter the new test date (format YYYY-MM-DD HH:MM): ").strip()
                new_test_date_obj = datetime.strptime(new_test_date, "%Y-%m-%d %H:%M")
                if datetime(2000, 1, 1) <= new_test_date_obj <= datetime.now():
                    selected_record['test_date'] = new_test_date_obj.strftime("%Y-%m-%d %H:%M")
                    break
                else:
                    print("Test date must be between 2000-01-01 and today. Please re-enter.")
            except ValueError:
                print("Invalid date format. Please re-enter in the format YYYY-MM-DD HH:MM.")

    if input("Do you want to edit the Result Value? (Y/n): ").strip().lower() == 'y':
        while True:
            result_value = input(f"Enter the new result value (float) for the test {selected_record['test'].abbr_name}: ").strip()
            if is_valid_float(result_value):
                selected_record['result_value'] = float(result_value)
                break
            else:
                print("Invalid result value. Please enter a valid float number.")

    if input("Do you want to edit the Status? (Y/n): ").strip().lower() == 'y':
        valid_statuses = ["pending", "completed", "reviewed"]
        while True:
            status = input("Enter the new status (Pending, Completed, Reviewed): ").strip().lower()
            if status in valid_statuses:
                selected_record['status'] = status
                break
            else:
                print("Invalid status. Please enter one of the following: Pending, Completed, Reviewed.")

    if selected_record['status'].lower() == "completed":
        if input("Do you want to edit the Result Date? (Y/n): ").strip().lower() == 'y':
            while True:
                try:
                    result_date = input(f"Enter the new result date (format YYYY-MM-DD HH:MM): ").strip()
                    result_date_obj = datetime.strptime(result_date, "%Y-%m-%d %H:%M")
                    if result_date_obj >= datetime.strptime(selected_record['test_date'], "%Y-%m-%d %H:%M"):
                        selected_record['result_date'] = result_date_obj.strftime("%Y-%m-%d %H:%M")
                        break
                    else:
                        print("Result date must be after the test date. Please re-enter.")
                except ValueError:
                    print("Invalid date format. Please re-enter in the format YYYY-MM-DD HH:MM.")
    patient.records[record_number] = selected_record
    with open(file_path, 'w') as file:
        for pid, patient in patients.items():
            for record in patient.records:
                line = f"{pid}: {record['test'].abbr_name}, {record['test_date']}, {record['result_value']}, {record['unit']}, {record['status']}"
                if record['status'] == "completed":
                    line += f", {record['result_date']}"
                file.write(line + "\n")

    print("Record successfully updated.")


def update_medical_tests(tests, file_path):
    while True:
        abbr_name = input("Enter the Test Abbreviation to update: ").strip()
        if abbr_name in tests:
            selected_test = tests[abbr_name]
            break
        else:
            print("Invalid Test Abbreviation. Please enter a valid one.")

    print(f"\nSelected Test: {selected_test.name}")
    print(f"Abbreviation: {selected_test.abbr_name}")
    print(f"Normal Range: {selected_test.lower_range} - {selected_test.upper_range} {selected_test.unit}")
    print(f"Turnaround Time: {selected_test.turnaround_time}")

    if input("Do you want to edit the Test Name? (Y/n): ").strip().lower() == 'y':
        new_name = input("Enter the new test name: ").strip()
        selected_test.name = new_name

    if input("Do you want to edit the Lower Range? (Y/n): ").strip().lower() == 'y':
        while True:
            lower_range = input("Enter the new lower range (float): ").strip()
            if is_valid_float(lower_range):
                selected_test.lower_range = float(lower_range)
                break
            else:
                print("Invalid lower range. Please enter a valid float number.")

    if input("Do you want to edit the Upper Range? (Y/n): ").strip().lower() == 'y':
        while True:
            upper_range = input("Enter the new upper range (float): ").strip()
            if is_valid_float(upper_range) and float(upper_range) > selected_test.lower_range:
                selected_test.upper_range = float(upper_range)
                break
            else:
                print("Invalid upper range. Please ensure it is a valid float number and higher than the lower range.")

    if input("Do you want to edit the Unit? (Y/n): ").strip().lower() == 'y':
        new_unit = input("Enter the new unit: ").strip()
        selected_test.unit = new_unit

    if input("Do you want to edit the Turnaround Time? (Y/n): ").strip().lower() == 'y':
        while True:
            try:
                turnaround_time = input("Enter the new turnaround time (format DD-hh-mm): ").strip()
                days, hours, minutes = map(int, turnaround_time.split('-'))
                selected_test.turnaround_time = f"{days:02d}-{hours:02d}-{minutes:02d}"
                break
            except ValueError:
                print("Invalid format. Please enter the turnaround time in the format DD-hh-mm.")

    with open(file_path, 'w') as file:
        for test in tests.values():
            file.write(test.to_file_string())
    print("Medical test successfully updated.")


def filter_by_patient_id(patients, patient_id):
    return {pid: patient for pid, patient in patients.items() if pid == patient_id}


def filter_by_test_name(patients, test_name):
    filtered_patients = {}
    for pid, patient in patients.items():
        filtered_records = [record for record in patient.records if record['test'].abbr_name == test_name]
        if filtered_records:
            filtered_patients[pid] = Patient(pid)
            filtered_patients[pid].records = filtered_records
    return filtered_patients


def filter_by_abnormal_tests(patients):
    filtered_patients = {}
    for pid, patient in patients.items():
        filtered_records = [record for record in patient.records if
                            not record['test'].is_result_normal(record['result_value'])]
        if filtered_records:
            filtered_patients[pid] = Patient(pid)
            filtered_patients[pid].records = filtered_records
    return filtered_patients


def filter_by_date_range(patients, start_date, end_date):
    filtered_patients = {}
    for pid, patient in patients.items():
        filtered_records = [record for record in patient.records if
                            start_date <= datetime.strptime(record['test_date'], "%Y-%m-%d %H:%M") <= end_date]
        if filtered_records:
            filtered_patients[pid] = Patient(pid)
            filtered_patients[pid].records = filtered_records
    return filtered_patients


def filter_by_status(patients, status):
    filtered_patients = {}
    for pid, patient in patients.items():
        filtered_records = [record for record in patient.records if record['status'].lower() == status.lower()]
        if filtered_records:
            filtered_patients[pid] = Patient(pid)
            filtered_patients[pid].records = filtered_records
    return filtered_patients


def convert_to_timedelta(turnaround_time_str):
    days, hours, minutes = map(int, turnaround_time_str.split('-'))
    return timedelta(days=days, hours=hours, minutes=minutes)


def filter_by_turnaround_time(patients, min_turnaround, max_turnaround):
    min_turnaround_delta = convert_to_timedelta(min_turnaround)
    max_turnaround_delta = convert_to_timedelta(max_turnaround)

    filtered_patients = {}
    for pid, patient in patients.items():
        filtered_records = []
        for record in patient.records:
            test = record['test']
            turnaround_delta = convert_to_timedelta(test.turnaround_time)
            if min_turnaround_delta <= turnaround_delta <= max_turnaround_delta:
                filtered_records.append(record)
        if filtered_records:
            filtered_patients[pid] = Patient(pid)
            filtered_patients[pid].records = filtered_records
    return filtered_patients


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False


def filter_medical_tests(patients):
    print("\nSelect the criteria you want to filter by:")
    print("1. Patient ID")
    print("2. Test Name")
    print("3. Abnormal Tests")
    print("4. Test added within a specific period (start and end dates)")
    print("5. Test Status")
    print("6. Test Turnaround Time within a period (min and max)")

    while True:
        num_criteria = input("How many criteria do you need? (1-6): ").strip()
        if num_criteria.isdigit() and 1 <= int(num_criteria) <= 6:
            num_criteria = int(num_criteria)
            break
        else:
            print("Invalid input. Please enter a number between 1 and 6.")

    selected_criteria = []
    for i in range(num_criteria):
        while True:
            criterion = input(f"Enter the number of criterion {i + 1} (1-6): ").strip()
            if criterion.isdigit() and 1 <= int(criterion) <= 6:
                selected_criteria.append(int(criterion))
                break
            else:
                print("Invalid input. Please enter a number between 1 and 6.")

    filtered_patients = patients

    for criterion in selected_criteria:
        if criterion == 1:
            while True:
                patient_id = input("Enter the Patient ID to filter by: ").strip()
                if patient_id.isdigit():
                    filtered_patients = filter_by_patient_id(filtered_patients, int(patient_id))
                    break
                else:
                    print("Invalid input. Please enter a valid Patient ID.")

        elif criterion == 2:
            test_name = input("Enter the Test Name (abbreviation) to filter by: ").strip()
            filtered_patients = filter_by_test_name(filtered_patients, test_name)

        elif criterion == 3:
            filtered_patients = filter_by_abnormal_tests(filtered_patients)

        elif criterion == 4:
            while True:
                start_date_str = input("Enter the start date (YYYY-MM-DD HH:MM): ").strip()
                end_date_str = input("Enter the end date (YYYY-MM-DD HH:MM): ").strip()
                if is_valid_date(start_date_str) and is_valid_date(end_date_str):
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M")
                    end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M")
                    filtered_patients = filter_by_date_range(filtered_patients, start_date, end_date)
                    break
                else:
                    print("Invalid date format. Please enter dates in the format YYYY-MM-DD HH:MM.")

        elif criterion == 5:
            status = input("Enter the Test Status to filter by (Pending, Completed, Reviewed): ").strip().lower()
            filtered_patients = filter_by_status(filtered_patients, status)

        elif criterion == 6:
            while True:
                min_turnaround = input("Enter the minimum turnaround time (DD-hh-mm): ").strip()
                max_turnaround = input("Enter the maximum turnaround time (DD-hh-mm): ").strip()
                if validate_turnaround_time(min_turnaround) and validate_turnaround_time(max_turnaround):
                    filtered_patients = filter_by_turnaround_time(filtered_patients, min_turnaround, max_turnaround)
                    break
                else:
                    print("Invalid input. Please enter turnaround time in the format DD-hh-mm.")

    '''
    if filtered_patients:
        print("\nFiltered Medical Records:")
        print_all_medical_records(filtered_patients)
    else:
        print("No records found matching the selected criteria.")
    '''
    return filtered_patients


def calculate_summary_statistics(filtered_patients):
    if not filtered_patients:
        return "No records found for the selected criteria."

    test_values = []
    turnaround_times = []

    for patient in filtered_patients.values():
        for record in patient.records:
            test_values.append(record['result_value'])

            test = record['test']
            turnaround_delta = convert_to_timedelta(test.turnaround_time)
            turnaround_times.append(turnaround_delta)

    min_test_value = min(test_values)
    max_test_value = max(test_values)
    avg_test_value = mean(test_values)

    min_turnaround_time = min(turnaround_times)
    max_turnaround_time = max(turnaround_times)
    avg_turnaround_time = sum(turnaround_times, timedelta()) / len(turnaround_times)

    min_turnaround_time_str = f"{min_turnaround_time.days}-{min_turnaround_time.seconds // 3600}-{(min_turnaround_time.seconds // 60) % 60}"
    max_turnaround_time_str = f"{max_turnaround_time.days}-{max_turnaround_time.seconds // 3600}-{(max_turnaround_time.seconds // 60) % 60}"
    avg_turnaround_time_str = f"{avg_turnaround_time.days}-{avg_turnaround_time.seconds // 3600}-{(avg_turnaround_time.seconds // 60) % 60}"

    summary = f"Summary Report for Filtered Records:\n" \
              f"-----------------------------------\n" \
              f"Test Values:\n" \
              f" - Minimum Test Value: {min_test_value}\n" \
              f" - Maximum Test Value: {max_test_value}\n" \
              f" - Average Test Value: {avg_test_value:.2f}\n\n" \
              f"Turnaround Times:\n" \
              f" - Minimum Turnaround Time: {min_turnaround_time_str}\n" \
              f" - Maximum Turnaround Time: {max_turnaround_time_str}\n" \
              f" - Average Turnaround Time: {avg_turnaround_time_str}\n"

    return summary


def export_medical_records(patients, filename="medical_records.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["Patient ID", "Abbreviation", "Test Date", "Result Value", "Unit", "Status", "Result Date"])
        for patient in patients.values():
            for record in patient.records:
                writer.writerow([
                    patient.patient_id,
                    record['test'].abbr_name,
                    record['test_date'],
                    record['result_value'],
                    record['unit'],
                    record['status'],
                    record['result_date'] if 'result_date' in record else ''
                ])

    print(f"Medical records exported successfully to {filename}")


def import_medical_records(file_path, tests, patients):
    with open(file_path, 'r') as file:
        next(file)

        for line in file:
            try:
                record_parts = line.strip().split(",")

                patient_id = int(record_parts[0].strip())
                abbr_name = record_parts[1].strip()
                test_date = datetime.strptime(record_parts[2].strip(), "%Y-%m-%d %H:%M")
                result_value = float(record_parts[3].strip())
                unit = record_parts[4].strip()
                status = record_parts[5].strip()
                result_date = None
                if len(record_parts) > 6 and record_parts[6].strip():
                    result_date = datetime.strptime(record_parts[6].strip(), "%Y-%m-%d %H:%M")

                if abbr_name in tests:
                    test = tests[abbr_name]

                    record = {
                        "test": test,
                        "test_date": test_date.strftime("%Y-%m-%d %H:%M"),
                        "result_value": result_value,
                        "unit": unit,
                        "status": status,
                        "result_date": result_date.strftime("%Y-%m-%d %H:%M") if result_date else None
                    }

                    if patient_id not in patients:
                        patients[patient_id] = Patient(patient_id)

                    patients[patient_id].add_record(record)
                else:
                    print(f"Warning: Test '{abbr_name}' not found in the list of valid medical tests.")
            except Exception as e:
                print(f"Error processing line: {line}\nException: {e}")

    return patients
