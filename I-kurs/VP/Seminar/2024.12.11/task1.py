# Description: This script creates a class `NumericList` that filters a list to keep only numeric values (integers and floats). It then provides methods to display the filtered list and calculate its average.  The script demonstrates its usage with sample data.
# Tags: List Filtering, Numeric Operations, Average Calculation

class NumericList:
    def __init__(self, input_list):
        self.numeric_list = [
            item for item in input_list if isinstance(item, (int, float))]

    def show_list(self):
        print(self.numeric_list)

    def calculate_average(self):
        if not self.numeric_list:
            return 0
        return sum(self.numeric_list) / len(self.numeric_list)


input_data = [1, 'a', 2, 3, 'b', 4]
numeric_list_obj = NumericList(input_data)
numeric_list_obj.show_list()
print(numeric_list_obj.calculate_average())