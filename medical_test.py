class MedicalTest:
    def __init__(self, name, abbr_name, lower_range, upper_range, unit, turnaround_time):
        self.name = name
        self.abbr_name = abbr_name
        self.lower_range = lower_range
        self.upper_range = upper_range
        self.unit = unit
        self.turnaround_time = turnaround_time

    def is_result_normal(self, result_value):
        if self.lower_range is not None and result_value < self.lower_range:
            return False
        if self.upper_range is not None and result_value > self.upper_range:
            return False
        return True

    def __str__(self):
        return f"{self.name} ({self.abbr_name}): Range: > {self.lower_range}, < {self.upper_range}; Unit: {self.unit}; Turnaround Time: {self.turnaround_time}"

    def to_file_string(self):
        return f"\nName: {self.name} ({self.abbr_name}); Range: {('> ' + str(self.lower_range)) if self.lower_range is not None else ''}, {('< ' + str(self.upper_range)) if self.upper_range is not None else ''}; Unit: {self.unit}, {self.turnaround_time}"
