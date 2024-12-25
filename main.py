import functions as f


def main():
    valid_tests = f.read_medical_tests("medicalTest.txt")
    patients = {}
    f.read_medical_records("medicalRecord.txt", valid_tests, patients)
    print("\nMedical Test Management System")
    while True:
        f.display_menu()
        choice = input("\nEnter your choice (1-11): ")

        if choice == '1':
            f.add_new_medical_test(valid_tests, "medicalTest.txt")
        elif choice == '2':
            f.add_new_medical_test_record(valid_tests, patients, "medicalRecord.txt")
        elif choice == '3':
            f.update_patient_records(patients, valid_tests, "medicalRecord.txt")
        elif choice == '4':
            f.update_medical_tests(valid_tests, "medicalTest.txt")
        elif choice == '5':
            filtered_patients = f.filter_medical_tests(patients)
            if filtered_patients:
                f.print_all_medical_records(filtered_patients)
            else:
                print("No matching data found.")
        elif choice == '6':
            filtered_records = f.filter_medical_tests(patients)
            report = f.calculate_summary_statistics(filtered_records)
            print(report)
        elif choice == '7':
            f.export_medical_records(patients)
        elif choice == '8':
            f.import_medical_records("medical_records.csv", valid_tests, patients)
        elif choice == '9':
            f.print_all_medical_tests(valid_tests)
        elif choice == '10':
            f.print_all_medical_records(patients)
        elif choice == '11':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
