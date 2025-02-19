class HeaderManager:
    @staticmethod
    def setup_headers(data):
        headers = data[0][1].strip().split('\n')[2].split('\t')
        headers.insert(0, 'File')  # Add 'File' column as the first column
        headers.append('Edit/Export')
        return headers