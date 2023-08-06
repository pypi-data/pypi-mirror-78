# get_nested_value_by_path
Get a nested value of nested dict by path

    def get_nested_value_by_path(nested_dict, path, default=None, mode='mix'):
    """
    :param nested_dict: nested dict object
        {
          "club": [
            {
              "manager": {
                "last_name": "Lionel",
                "first_name": "Messi"
              }
            }
          ]
        }
    :param path: path to access the nested dict value
        "club/0/manager/first_name"
    :param default: default value
    :param mode: ['json', 'list', 'mix']
    :return: value of nested dict
        "Messi"
    """

#####Installation:
https://pypi.org/project/get-nested-value-by-path/

    pip install get-nested-value-by-path

#####Usage:

    nested_dict = {
      "key": [
        {
          "sub_key": {
            "sub_sub_key_1": "Value_1",
            "sub_sub_key_2": "Value_2"
          }
        }
      ]
    }
        

`before:`

    sub_sub_value_1 = nested_dict['key'][0]['sub_key']['sub_sub_key_1']

`after:`

    from get_nested_value_by_path import get_nested_value_by_path
    sub_sub_value_1 = get_nested_value_by_path(nested_dict, "key/0/sub_key/sub_sub_key_1")
        
#####Example:

    nested_dict = {
      "club": [
        {
          "manager": {
            "last_name": "Lionel",
            "first_name": "Messi"
          }
        }
      ]
    }
        

`before:`

    manager_last_name = nested_dict['club'][0]['manager']['last_name']

`after:`

    from get_nested_value_by_path import get_nested_value_by_path
    manager_last_name = get_nested_value_by_path(nested_dict, "club/0/manager/last_name")