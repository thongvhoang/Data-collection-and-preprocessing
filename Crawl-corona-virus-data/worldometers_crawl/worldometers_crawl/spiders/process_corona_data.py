class process_data:
    def __init__(self,string_data):
        self.string_data = string_data

    def getTitle(self):
        return self.string_data[4:len(self.string_data)-5] 
        
    def getDate(self):
        Date_index_start = self.string_data.find('["')+2
        Date_index_end = self.string_data.find('"]')
        Date = self.string_data[Date_index_start:Date_index_end].split('","')
        return Date#self.string_data[Date_start:Date_end]
    
    def getNumberData(self):
        NumberData_index_start = self.string_data.find('data: [')+7
        NumberData_index_rstart = self.string_data.rfind('data: [')+7
        if (NumberData_index_start==NumberData_index_rstart or self.string_data.find('Total Cases')>0):
            NumberData_index_end = self.string_data.find('responsive')-23
        else:
            NumberData_index_end = self.string_data.rfind('color')-65
        NumberData = self.string_data[NumberData_index_start:NumberData_index_end].split(',')                
        return NumberData
