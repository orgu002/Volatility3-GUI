class DataParser:
    @staticmethod
    def parse_data(data):
        all_rows_with_color = []
        for entry in data:
            color, rows_str = entry
            rows = [row.split('\t') for row in rows_str.strip().split('\n')[3:]]
            all_rows_with_color.extend([(row, color) for row in rows])
        return all_rows_with_color