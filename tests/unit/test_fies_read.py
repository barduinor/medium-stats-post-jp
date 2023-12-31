from files import FileTypes, files_list, file_load

def test_files_list():
    """ Should return at least one file """
    file_list = files_list('tests')
    assert len(file_list) >= 1


def test_file_load():
    """ Should load the json file and retunr an object"""
    files = files_list('tests/data')
    for file_name in files:
        data = file_load('tests/data/'+file_name)
        # file_type_index = file.find('-')
        # file_name_type = file[file_type_index+1:len(file)-5:]

        if FileTypes.POST_STATS.value in file_name:
            file_type = FileTypes.POST_STATS
        elif FileTypes.DAILY_STATS.value in file_name:
            file_type = FileTypes.DAILY_STATS
        else:
            file_type = None

        if 'totalStats' in data[0]['data']['post']:
            json_type = FileTypes.POST_STATS
        elif 'dailyStats' in data[0]['data']['post']:
            json_type = FileTypes.DAILY_STATS
        else:
            json_type = None
            
        print(f'{file_name} : {file_type} : {json_type}')
        assert data is not None
        assert data[0]['data']['post']['id'] is not None
        
        assert file_type is not None
        assert json_type is not None

        assert file_type == json_type

