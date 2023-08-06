import os
import chardet
import warnings

import pandas as pd 

def read_content(dir_file):
    """ 
    Read the file as bite
    and return the content
    
    Arguments:
        dir_file {[str]} -- [description]
    
    Returns:
        [str] -- [description]
    """

    with open(dir_file, "rb") as r:
        content = r.read()
    try:
        content = content.decode("utf-8")
    except Exception:
        content = content.decode("CP932")
    except Exception:
        content = content.decode("SHIFT_JIS")
    except Exception:
        encoder_code = chardet.detect(content)["encoding"]
        content = content.decode(encoder_code)
    except Exception:
        message = "This file code {} is error, and ignored".format(dir_file)
        warnings.warn(message)
        content = content.decode(encoder_code, "ignore")
    return content


def write_content(dir_file, content):
    """ 
    Write the file as bite
    and return the content
    
    Arguments:
        dir_file {[str]} -- [description]
        content {[str]}
    
    Returns:
        [str] -- [description]
    """
    with open(dir_file, "w", encoding="utf-8") as w: 
        w.write("{}".format(content))

    return True


def read_excel(file):
    """
    Argument
        # file {str}
    
    Return 

    """
    data = pd.read_excel(file)
    return data

def read_folder_content(dir_folder):
    """[summary]
    
    Arguments:
        dir_folder {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    total_content = []
    list_files = os.listdir(dir_folder)
    for dir_file in list_files:
        content = read_content(dir_file=dir_folder+dir_file)
        total_content.append(content)
    return total_content


def write_to_excel(columns:list, data:list, file_name:str):
    """
    # Arguments
        - columns {list}: ["a","b"]
        - data {list}:[["a-v","b-v"]["a-v1","a-v2"]]
    """
    df = pd.DataFrame(columns=columns,data=data)
    writer = pd.ExcelWriter(file_name +'.xlsx')
    df.to_excel(writer,'Sheet1')
    writer.close()
    print("Write in {}, done.".format(file_name))
