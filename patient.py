class Patient:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def __str__(self):
        record_str = "\n".join(
            f"{record['test'].abbr_name}, {record['test_date']}, {record['result_value']}, {record['unit']}, {record['test'].unit}"
            f"{', ' + record['result_date'] if record['status'] == 'completed' else ''}"
            for record in self.records
        )
        return f"Patient ID: {self.patient_id}\nRecords:\n{record_str}\n"
