

def get_url_params(url):
    '''
    This function will return the url parameters as a dictionary
    '''
    url_params = {}
    params_string = url.split("?")
    if len(params_string) > 1:
        url_param_string = params_string[1]
        url_param_list = url_param_string.split("&")
        for url_param in url_param_list:
            param_split = url_param.split("=")
            url_params[param_split[0]] = param_split[1]
    return url_params

def append_url_params(url, url_params,override=True):
    '''
    This function will append the url parameters to the url
    '''
    url_param_string = ""
    base_url = url.split("?")[0]

    old_params = get_url_params(url)
    if override == True:
        url_params={**old_params,**url_params}
    else:
        url_params={**url_params,**old_params}

    for key, value in url_params.items():
        if url_param_string == "":
            url_param_string += f"{key}={value}"
        else:
            url_param_string += f"&{key}={value}"
    new_url = f"{base_url}?{url_param_string}"
    print(new_url)
    return new_url

def remove_url_params(params_to_delete,url):
    '''
    This function will remove the url parameters from the url
    '''
    base_url = url.split("?")[0]
    url_params = get_url_params(url)
    for param in params_to_delete:
        if param in url_params:
            del url_params[param]
            
    return append_url_params(base_url,url_params,override=True)