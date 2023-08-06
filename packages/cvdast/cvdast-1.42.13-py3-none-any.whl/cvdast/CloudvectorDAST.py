#!/usr/bin/python

# /***************************************************************\
# **                                                           **
# **  / ___| | ___  _   _  __| \ \   / /__  ___| |_ ___  _ __  **
# ** | |   | |/ _ \| | | |/ _` |\ \ / / _ \/ __| __/ _ \| '__| **
# ** | |___| | (_) | |_| | (_| | \ V /  __/ (__| || (_) | |    **
# **  \____|_|\___/ \__,_|\__,_|  \_/ \___|\___|\__\___/|_|    **
# **                                                           **
# **      (c) Copyright 2018 & onward, CloudVector             **
# **                                                           **
# **  For license terms, refer to distribution info            **
# \***************************************************************/

import json
import re
import collections
import os
import yaml
import shutil
from jinja2 import Template
from copy import deepcopy
import requests
from cvapianalyser import CommunityEdition
from openapispecdiff import OpenApiSpecDiff

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

root = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(root, 'templates')
fuzz_words_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wfuzz/wordlist')
fuzz_types = ["general", "injections", "vulns", "webservices", "stress", "others"]
ANOMOLY_THRESHOLD = 1.07142
RESERVED_PARAMETERS = ["$RESPONSE_ERROR","$CV_EVENT_ID"]

import collections
def update_nested_dict(dict, value):
    for k, v in value.items():
        if isinstance(dict, collections.Mapping):
            if isinstance(v, collections.Mapping):
                r = update_nested_dict(dict.get(k, {}), v)
                dict[k] = r
            else:
                dict[k] = value[k]
        else:
            dict = {k: value[k]}
    return dict

def keypaths(nested):
    for key, value in nested.items():
        if isinstance(value, collections.Mapping):
            for subkey, subvalue in keypaths(value):
                yield [key] + subkey, subvalue
        else:
            yield [key], value


def key_lookup(key, var):
    paths = []
    for k, v in keypaths(var):
        if key in k:
            if k:
                paths.append(".".join(k))
    return paths


class CloudvectorDAST(object):
    """Library for creating pytest functional and fuzz test cases for a given Open API spec.

    Input:

    """
    def __init__(self, APISpecOne, APISpecTwo, ce_host, ce_username, ce_password, config_file, cover_only_diff="n",
                 input_params_file=None, do_fuzz=False):

        custom_validations = None
        self.static_headers_from_cfg = {}
        self.cv_config = None
        self.cvdast_to_auth_info = {}
        self.params_from_spec = {}
        self.respcodes_from_spec = {}
        self.params_details_from_spec = {}
        if config_file:
            if os.path.exists(config_file):
                self.cv_config = self._parse_cv_config(config_file)
                ce_host = self.cv_config["ce_setup"]["ce_host"]
                ce_username = self.cv_config["ce_setup"]["ce_username"]
                custom_validations = self.cv_config.get("custom_validations",{})
                self.static_headers_from_cfg = self.cv_config.get("static_headers")
                if self.cv_config.get("authentication"):
                  self.cvdast_to_auth_info = self.cv_config.get("authentication")
        if str(self.cv_config.get("generate_tests_for_response_codes","Y")).lower() == "y":
            self.generate_tests_for_respcodes = True
        else:
            self.generate_tests_for_respcodes = False
        if APISpecOne:
            self.apispec_one_path = APISpecOne
        else:
            self.apispec_one_path = None
        self.apispec_two_path = APISpecTwo
        if ".txt" not in self.apispec_two_path:
            self.openapispec_obj = OpenApiSpecDiff.OpenApiSpecDiff(self.apispec_one_path, self.apispec_two_path)
        self.ceobj = CommunityEdition.CommunityEdition(ce_host, ce_username, ce_password)
        print("\n\t\t\t\t\t\t\t\t\t----------------- DAST - For CloudVector APIShark events "
              "-----------------")
        # self.regenerate_traffic(self._get_changed_apis())
        self.input_json = {}
        if not os.path.exists("tests"):
            os.mkdir("tests")
        if do_fuzz:
            if not os.path.exists((os.path.join(os.getcwd(),"wfuzz"))):
                shutil.copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)),"wfuzz"), os.path.join(os.getcwd(),"wfuzz"))
        self.params_captured_in_traffic = {}
        self.prepped_spec = []
        if ".txt" not in self.apispec_two_path:
            changed_apis = self._get_changed_apis()
            apis_to_check = changed_apis["changed"]
            apis_to_check.update(changed_apis["new"])
            if self.apispec_one_path:
                self.prepped_spec = self._prepare_spec_for_test_generation(self.apispec_two_path, changed_apis)
            else:
                self.prepped_spec = self._prepare_spec_for_test_generation(self.apispec_two_path)
        else:
            with open(self.apispec_two_path) as fobj:
                apis_to_check = {str(_).replace("\n",""):"" for _ in fobj.readlines()}
        self.input_json = {}
        self.assertions_map = {}
        # for file in input_params_file.split(";"):
        #     print("loading variables from input file " + str(file) + " .....")
        #     input_json = {}
        #     if os.path.exists(file):
        #         if ".json" in file:
        #             with open(file) as fobj:
        #                 input_json = json.load(fobj)
        #         else:
        #             input_json = self._load_input_from_files(file)
        #     self.input_json.update(input_json)

        cv_events = []
        for _ in ["20"]:
            print("\n\t ---> Querying for Status code "+str(_)+"*")
            cv_events += self._process_event_data(apis_to_check, filters_to_query={"http_rsp_status_code":_})
        print("\n\t\t......done collecting events data from APIShark")

        # if not cv_events:
        #     cv_events = self.prepped_spec
        cv_events += self.prepped_spec
        #self._process_input_json()
        if cover_only_diff == "y":
            self._process_param_diff(apis_to_check, True)
        # else:
        #     self._process_param_diff(apis_to_check, False)

        # params_captured_in_traffic_new = deepcopy(self.params_captured_in_traffic)
        # for k,v in self.params_captured_in_traffic.items():
        #     if type(v) is list:
        #         for each in v:
        #             for i, j in self._recursive_items(each):
        #                 if i not in self.params_captured_in_traffic:
        #                     params_captured_in_traffic_new[i] = j
        #     else:
        #         for i, j in self._recursive_items(v):
        #             if i not in self.params_captured_in_traffic:
        #                 params_captured_in_traffic_new[i] = j
        #
        # print("\n\n\n\n")
        # print(params_captured_in_traffic_new)
        # print("\n\n\n\n")
        # print(self.params_captured_in_traffic)
        # print("\n\n\n\n")

        #self.params_captured_in_traffic = params_captured_in_traffic_new
        with open("tests/params_captured.json", "w+") as fobj:
            json.dump(self.params_captured_in_traffic, fobj, indent=4)
        self.create_pyfixtures()
        # self.create_fuzzfixtures()
        self.create_pytest_methods(cv_events, custom_validations)
        if do_fuzz:
            self.create_fuzz_test_methods(cv_events)
            # self.create_fuzzfixtures()
        self.create_assertions(fuzzing=do_fuzz)
        # if self.authentication_api_from_spec:
        #     self._update_params_captured_for_auth()

    def _load_input_from_files(self, input_file):
        input_vars = {}
        content = []
        if os.path.exists(input_file):
            with open(input_file) as fobj:
                content = fobj.readlines()
        for each in content:
            if "=" in each:
                key, value = each.split("=")
                if "[" in value and "]" in value:
                    value = eval(value)
                else:
                    value = [value]
                input_vars[str(key).strip()] = value
        return input_vars

    def _recursive_items(self, d):
        for key, value in d.items():
            if type(value) is dict:
                yield (key, value)
                yield from self._recursive_items(value)
            else:
                yield (key, value)
    # def _update_params_captured_for_auth(self, auth_info):
    #     with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests/authcreds.json"),"w+") as fobj:
    #         json.dumps(auth_info)

    def _prepare_spec_for_test_generation(self, input_spec, specific_apis=None):
        parsed_new_spec = self._get_spec_parsed(input_spec)
        #print(parsed_new_spec)
        apis_from_spec = []
        if "servers" in parsed_new_spec:
            from urllib.parse import urlparse
            baseurl = parsed_new_spec["servers"][0]["url"]
            host = urlparse(baseurl).netloc
            if host:
                baseurl = baseurl.split(host)[1:]

        else:
            baseurl = parsed_new_spec.get("host", "") + parsed_new_spec.get("basePath", "")
            host = parsed_new_spec.get("host")
        if type(baseurl) is list:
            baseurl = baseurl[0]
        for api, info in parsed_new_spec["paths"].items():
            if specific_apis:
                if api not in specific_apis:
                    continue
            if api not in self.respcodes_from_spec:
                self.respcodes_from_spec[api] = {}
            #print("----------")
            for method, minfo in info.items():
                #print(method, minfo)
                x = {}
                x["method"] = method.lower()
                x["host"] = host
                x["header"] = {}
                x["params"] = []
                x["detailed_params"] = {}
                x["body"] = {}
                x["rsp_body"] = {}
                x["url"] = ""
                x["http-req-url"] = baseurl+api
                if baseurl:
                    x["url"] = baseurl+api
                if host:
                    x["url"] = host + baseurl + api
                for _ in x["url"].split("/"):
                    if "{" in _ and "}" in _:
                        _ = str(_).replace("{", "").replace("}", "")
                        x["params"].append(_)
                #x["params"] += url_params
                if x["http-req-url"] not in self.respcodes_from_spec:
                    self.respcodes_from_spec[x["http-req-url"]] = {}
                self.respcodes_from_spec[x["http-req-url"]][method] = list(minfo.get("responses").keys())
                x["url"] = x["url"].replace("{", "{{").replace("}", "}}")
                for _ in minfo.get("parameters", []):
                    #print("\n\n"+str(_)+"\n\n")
                    if _.get("in") == "header":
                        x["header"][_.get("name")] = ""
                    elif _.get("in") == "query":
                        if "?" not in x["url"]:
                            x["url"] += "?" + _.get("name") + "={{" + _.get("name") + "}}"
                        else:
                            x["url"] += "&" + _.get("name") + "={{" + _.get("name") + "}}"
                        x["params"].append(_.get("name"))
                    else:
                        if _.get("name"):
                            x["params"].append(_.get("name"))
                            x["body"][_.get("name")] = ""
                    #print("this....."+str(_.get("value")), api, method)
                    if _.get("value"):
                        #if type(_.get("value")) is list:
                            #print("its a list....")
                        self.params_details_from_spec[str(_.get("name"))] = _.get("value")
                        # else:
                        #     print("not list...")
                        #     x["detailed_params"].update(_.get("value"))
                if api not in self.params_from_spec:
                    self.params_from_spec[api] = {}
                self.params_from_spec[api][method] = {_:[] for _ in x["params"]}
                #.update(x["detailed_params"])
                # if str(self.cv_config["authentication"]["api"]).lower() in str(x["url"]).lower():
                #     self.cvdast_to_auth_info = x
                #print("\n")
                #print(self.params_details_from_spec)
                #print("\n")
                #print(self.params_from_spec)
                apis_from_spec.append([x, None])
        return apis_from_spec

    def _parse_cv_config(self, path):
        with open(path) as fobj:
            config = yaml.load(fobj)
        return config

    def _scan_input_spec(self, input_path):
        input_spec = self._get_spec_parsed(input_path)
        if "servers" in input_spec:
            from urllib.parse import urlparse
            baseurl = input_spec["servers"][0]["url"]
            host = urlparse(baseurl).netloc
            if host:
                baseurl = baseurl.split(host)[1:]

        else:
            baseurl = input_spec.get("host", "") + input_spec.get("basePath", "")
            host = input_spec.get("host")
        if type(baseurl) is list:
            baseurl = baseurl[0]
        if baseurl == "/":
            baseurl = ""
        params_info = {}
        for api, info in input_spec["paths"].items():
            api = baseurl+api
            if api not in params_info:
                params_info[api] = {}
            for method, paraminfo in info.items():
                params = []
                if method not in params_info[api]:
                    params_info[api][method] = []
                for each in paraminfo.get("parameters", []):
                    if each.get("in") != "header":
                        params.append(each.get("name"))
                params_info[api][method] = params
        return params_info

    def _get_spec_parsed(self, input_path):
        return self.openapispec_obj.scan_input_spec(self.openapispec_obj.parse_spec(input_path))

    def _get_changed_apis(self):
        return self.openapispec_obj.diff

    # def _process_input_json(self):
    #     for key, value in self.input_json.items():
    #         if type(value) is list:
    #             if "others" not in self.params_captured_in_traffic:
    #                 self.params_captured_in_traffic["others"] = {}
    #             self.params_captured_in_traffic["others"].update({key: value})
    #         elif type(value) is dict:
    #             for name, values in value.items():
    #                 if "null" in values:
    #                     values.remove("null")
    #                 if key in self.params_captured_in_traffic:
    #                     self.params_captured_in_traffic[key].update({name: values})

    def _process_param_diff(self, changed_apis, only_diff):
        if only_diff:
            self.params_captured_in_traffic = {}

        for api, info in changed_apis.items():
            # if only_diff:
            #     self.params_captured_in_traffic[api] = {}
            # for method, params in info.items():
            #     for param in params:
            #         if api in self.params_captured_in_traffic:
            #             if param.get("name") not in self.params_captured_in_traffic[api]:
            #                 self.params_captured_in_traffic[api].update({param.get("name"): []})
            iflag = True
            for method, params in info.items():
                if only_diff and iflag:
                    self.params_captured_in_traffic = {api:{"200":{str(method).lower():[]}}}
                    iflag = False
                all_params = {}
                for param in params:
                    if api in self.params_captured_in_traffic:
                        if only_diff and iflag:
                            #self.params_captured_in_traffic[api]["200"][str(method).lower()] = []
                            all_params[param.get("name")] = ""
                self.params_captured_in_traffic[api]["200"][str(method).lower()].append(all_params)
        # for api, info in self.params_captured_in_traffic.items():
        #     for param, value in info.items():
        #         if param in self.input_json:
        #             self.params_captured_in_traffic[api][param] = self.input_json[param]
        #         if api in self.input_json:
        #             if param in self.input_json[api]:
        #                 self.params_captured_in_traffic[api][param] = self.input_json[api][param]

    def _get_fuzz_details(self, fuzz_type):
        fuzz_values = []
        # if os.path.isdir(os.path.join(fuzz_words_dir, fuzz_type)):
        #     for (root, dirs, files) in os.walk(os.path.join(fuzz_words_dir, fuzz_type), topdown=True):
        #         for _file in files:
        #             fuzz_values.append({"path": os.path.join("wfuzz/wordlist/", fuzz_type),
        #                                 "fuzz_type": fuzz_type})
                    # values = []
                    # with open(file) as _file:
                    #     values = _file.readlines()
                    # fuzz_values[file] = values
        fuzz_values.append({"path": os.path.join("wfuzz/wordlist/", fuzz_type),
                                        "fuzz_type": fuzz_type})
        return fuzz_values

    def _get_hosts_input(self, hosts):
        print("\n\n Select the host to create the tests for:\n")
        for _ in range(1, len(hosts) + 1):
            print("\t\t\t\t" + str(_) + " - " + str(hosts[_]) + "\n")
        pos = input("Select the host : ")
        return hosts[int(pos) - 1]

    def create_pyfixtures(self):
        print("\n\ncreating Pytest fixtures....\n")
        with open(os.path.join(templates_dir, 'conftest.j2')) as file_:
            template = Template(file_.read())
        #code = template.render(api_info=self.params_captured_in_traffic)
        #print(self.validate_pycode_for_syntax(code))
        if not os.path.exists("tests"):
            os.mkdir("tests")
        auth_api = None
        auth_api_headers = None
        auth_api_payload = None
        auth_api_response_key = None
        auth_inputs = ["host"]
        if self.cvdast_to_auth_info:
            auth_api = self.cvdast_to_auth_info.get("api_url")
            auth_api_headers = self.cvdast_to_auth_info.get("headers")
            auth_api_payload = self.cvdast_to_auth_info.get("payload")
            for k, v in auth_api_headers.items():
                template_found = re.search(r"\[\'([A-Za-z0-9_]+)\'\]", str(v))
                if template_found:
                    auth_inputs.append(template_found.group(1))
                    auth_api_headers[k] = auth_inputs[-1]
            for k, v in auth_api_payload.items():
                template_found = re.search(r"\[\'([A-Za-z0-9_]+)\'\]", str(v))
                if template_found:
                    auth_inputs.append(template_found.group(1))
                    auth_api_payload[k] = auth_inputs[-1]
            auth_api_response_key = self.cvdast_to_auth_info.get("response_key")
            auth_type = self.cvdast_to_auth_info.get("type", "basic").lower()
            if auth_type == "basic":
                auth_prefix = ""
            elif auth_type == "bearer":
                auth_prefix = "Bearer"
            else:
                auth_prefix = auth_type
        # for api,params_info in self.params_from_spec.items():
        #     for statuscode in self.params_captured_in_traffic:
        #         if int(statuscode) not in range(200,299):
        #             if not self.params_captured_in_traffic.get(statuscode):
        #                 continue
        #             if api not in self.params_captured_in_traffic[statuscode]:
        #                 self.params_captured_in_traffic[statuscode][api] = {}
        #             for k, v in params_info.items():
        #                 if k not in self.params_captured_in_traffic[statuscode].get(api,{}):
        #                     print(self.params_captured_in_traffic[statuscode][api])
        #                     self.params_captured_in_traffic[statuscode][api][k]=v
        nested_params={}
        more_params = []

        for param, info in self.params_details_from_spec.items():
            #tmp = []
            # if type(info) is list:
            #     info = info[0]
            # for k, v in self._recursive_items(info):
            #     if type(v) is not dict:
            #         tmp.append(k)
            _params = []
            if type(info) is dict:
                for k, v in keypaths(info):
                    more_params+=k
                    _params+=k
                    info = update_nested_dict(info, {k[-1]: k[-1]})
            elif type(info) is list:
                for each in info:
                    for k, v in keypaths(each):
                        more_params+=k
                        _params+=k
                        each = update_nested_dict(each, {k[-1]:k[-1]})
            nested_params[param] = _params
            #more_params+=info
            more_params = list(set(more_params))

        params_for_fixtures = []
        for api,info in self.params_captured_in_traffic.items():
            for rspcode, minfo in info.items():
                for method, plist in minfo.items():
                    for each in plist:
                        if type(each) is str:
                            if each not in params_for_fixtures and each not in RESERVED_PARAMETERS:
                                params_for_fixtures.append(each)
                        elif type(each) is dict:
                            for _ in each.keys():
                                if _ not in params_for_fixtures and _ not in RESERVED_PARAMETERS:
                                    params_for_fixtures.append(_)

        with open("tests/conftest.py", 'w+') as fh:
            fh.write(template.render(api_info=params_for_fixtures, api_detailed_info=self.params_details_from_spec,
                                     nested_params=nested_params, AUTH_API=auth_api, more_params=more_params,
                                     AUTH_API_HEADERS=auth_api_headers,AUTH_API_PAYLOAD=json.dumps(auth_api_payload),
                                     AUTH_RESP_KEY=auth_api_response_key, AUTH_INPUTS=auth_inputs, TOKEN_PREFIX=auth_prefix))
        print("\n\t\t......done creating pytest fixtures (conftest.py)")

    def create_fuzzfixtures(self):
        print("\n\ncreating fuzz-lightyear fixtures....\n")
        with open(os.path.join(templates_dir, 'fuzz_fixtures.j2')) as file_:
            template = Template(file_.read())
        code = template.render(api_info=self.params_captured_in_traffic)
        print(self.validate_pycode_for_syntax(code))
        if not os.path.exists("tests"):
            os.mkdir("tests")
        with open("tests/fuzz_fixtures.py", 'w+') as fh:
            fh.write(template.render(api_info=self.params_captured_in_traffic))
        print("\n\t\t......done creating fuzz-lightyear fixtures (fuzz_fixtures.py)")

    def create_assertions(self, fuzzing):
        print("\n\ncreating assertion methods....\n")
        with open(os.path.join(templates_dir, 'assertions.j2')) as file_:
            template = Template(file_.read())
        # code = template.render(api_info=self.params_captured_in_traffic)
        # print(self.validate_pycode_for_syntax(code))
        if not os.path.exists("tests"):
            os.mkdir("tests")
        if fuzzing:
            threshold = ANOMOLY_THRESHOLD
        else:
            threshold = 0
        with open("tests/assertions.py", 'w+') as fh:
            fh.write(template.render(assertions=self.assertions_map, ANOMALY_THRESHOLD=threshold))
        print("\n\t\t......done creating assertions (assertions.py)")

    def _create_assertions_map(self, url, params, req_payload, resp_payload):
        assertions_map = {}
        if url not in self.assertions_map:
            url = url.replace("//","/").replace("/", "_S_").replace("{", "").replace("}", "").replace(" ","").split("?")[0]
            if url.startswith("_S_"):
                url = "_"+url[3:]
            self.assertions_map[url] = {}
        if None in params:
            params.remove(None)

        for param in params:
            paths_in_req = key_lookup(param, req_payload)
            paths_in_rsp = key_lookup(param, resp_payload)

            paths_in_req = [_ for _ in paths_in_req if _ != ""]
            paths_in_rsp = [_ for _ in paths_in_rsp if _ != ""]

            if paths_in_req and paths_in_rsp:
                assertions_map.update({
                    param:
                        {
                            "req": paths_in_req,
                            "resp": paths_in_rsp
                        }
                })
        self.assertions_map[url].update(assertions_map)

    def _create_custom_validations(self, params_to_validate, info):
        validations = []
        for method, minfo in info.items():
            actual_params = minfo.get("params")
            for param in actual_params:
                if param in params_to_validate:
                    for condition, to_check in params_to_validate[param].items():
                        if condition == "missing":
                            validations.append([str(param) + "_missing", str(param) + "_arg = ''", to_check])
                        elif condition == "invalid":
                            validations.append([str(param) + "_invalid", str(param) + "_arg = 'iamdummy'", to_check])
        return validations

    def create_pytest_methods(self, cv_events, custom_validations):
        # print("\n\n\n"+str(custom_validations)+"\n\n\n")
        params_for_custom_validations = custom_validations.get("request_params")
        apis_to_be_tested = {}
        files_created = set()
        print("\n\ncreating Pytest test methods....\n")
        try:
            new_spec_info = self._scan_input_spec(self.apispec_two_path)
            hosts = new_spec_info.get("servers", {}).get("url", [])
        except AttributeError:
            new_spec_info = {}
            hosts = []
        #print(cv_events)
        for _ in cv_events:
            #print(_)
            event = _[0]
            rsp_codes_in_traffic = {}
            if _[1]:
                if int(_[1]["attributes"]["http_rsp_status_code"]) not in range(200, 299):
                    continue
            if event["url"]:
                # api = str(event["http-req-url"]).lstrip("/").rstrip("/").replace("/", "_").replace("-", "_").split("?")[
                #     0]
                api = str(event["http-req-url"]).lstrip("/").replace("/", "_S_").replace(" ","").split("?")[0]
                if api not in apis_to_be_tested:
                    apis_to_be_tested[api] = {}
                #apis_to_be_tested[api]["method"] = event["method"]
                method = event["method"].lower()
                if method not in apis_to_be_tested[api]:
                    apis_to_be_tested[api][method] = {}
                if self.static_headers_from_cfg:
                    for k, v in event["header"].items():
                        if k in self.static_headers_from_cfg:
                            event["header"][k] = str(self.static_headers_from_cfg[k])
                if "header" not in apis_to_be_tested[api][method]:
                    apis_to_be_tested[api][method]["header"] = {}
                apis_to_be_tested[api][method]["header"].update(event["header"])
                apis_to_be_tested[api][method]["url"] = event["url"]  # str(event["host"]).lower() + event["url"]
                if apis_to_be_tested[api][method].get("params"):
                    known_params = apis_to_be_tested[api][method].get("params")
                else:
                    known_params = []
                apis_to_be_tested[api][method]["params"] = new_spec_info.get(str(event["http-req-url"]).replace("//", "/"),{}).get(method,[])

                params_in_traffic = event.get("body",{}).keys()

                for _ in params_in_traffic:
                    if _ not in apis_to_be_tested[api][method]["params"]:
                        apis_to_be_tested[api][method]["params"].append(_)

                if apis_to_be_tested[api][method]["params"] is None:
                    apis_to_be_tested[api][method]["params"] = []

                apis_to_be_tested[api][method]["params"] = list(set(apis_to_be_tested[api][method]["params"]))
                apis_to_be_tested[api][method]["params"].append("host")
                apis_to_be_tested[api][method]["params"].append("url_prefix")
                apis_to_be_tested[api][method]["params"].append("access_token")

                host_url = str(event["host"]).lower()
                hosts.append(host_url)
                self._create_assertions_map(event["http-req-url"], apis_to_be_tested[api][method]["params"], event["body"],
                                            event["rsp_body"])
        with open(os.path.join(templates_dir, 'test_api.j2')) as file_:
            template = Template(file_.read())
        #host_url = [list(set([_ for _ in hosts if _ != '']))[-1]]
        # print(apis_to_be_tested)
        for k, v in apis_to_be_tested.items():
            # code = template.render(api_info=apis_to_be_tested[k], api_name=k, host_url=host_url)
            filename = str(k).replace("/", "_").replace("{", "").replace("}", "")
            if not os.path.exists("tests"):
                os.mkdir("tests")
            if params_for_custom_validations:
                extra_validations = self._create_custom_validations(params_for_custom_validations,
                                                                    apis_to_be_tested[k])
            else:
                extra_validations = []

            api_name = "/"+str(k.replace("_","/"))
            if self.generate_tests_for_respcodes:
                status_codes_for_api = self.respcodes_from_spec.get(api_name,{})
            else:
                status_codes_for_api = {}

            with open("tests/test_" + str(filename) + ".py", 'w+') as fh:
                fh.write(template.render(apis_metadata=apis_to_be_tested[k], api_name=k, host_url=host_url,
                                         custom_validations=extra_validations, STATUS_CODES=status_codes_for_api, TEST_MANAGEMENT=self.cv_config.get("upload_result_to")))
            files_created.add("test_" + str(filename))
        print("\n\t\t......done creating pytest methods: " + str(files_created))

    def create_fuzz_test_methods(self, cv_events):
        apis_to_be_tested = {}
        files_created = set()
        print("\n\ncreating Pytest test methods for fuzzing....\n")
        try:
            new_spec_info = self._scan_input_spec(self.apispec_two_path)
            hosts = new_spec_info.get("servers", {}).get("url", [])
        except AttributeError:
            new_spec_info = {}
            hosts = []
        # for _ in cv_events:
        #     event = _[0]
        #     if _[1]:
        #         if _[1]["attributes"]["http_rsp_status_code"] not in ["200", "201"]:
        #             continue
        #     if event["url"] not in apis_to_be_tested:
        #         api = str(event["http-req-url"]).lstrip("/").rstrip("/").replace("/", "_").replace("-", "_").split("?")[
        #             0]
        #         apis_to_be_tested[api] = {}
        #         apis_to_be_tested[api]["method"] = event["method"]
        #         if self.static_headers_from_cfg:
        #             for k, v in event["header"].items():
        #                 if k in self.static_headers_from_cfg:
        #                     event["header"][k] = str(self.static_headers_from_cfg[k])
        #
        #         # for k, v in event["header"].items():
        #         #     if k in self.static_headers_from_cfg:
        #         #         event["header"][k] = v
        #         apis_to_be_tested[api]["header"] = event["header"]
        #         apis_to_be_tested[api]["url"] = event["url"]
        #         apis_to_be_tested[api]["params"] = new_spec_info.get(str(event["http-req-url"]).replace("//", "/"))
        #         if apis_to_be_tested[api]["params"] is None:
        #             apis_to_be_tested[api]["params"] = []
        #         host_url = str(event["host"]).lower()
        #         hosts.append(host_url)
        #         self._create_assertions_map(event["http-req-url"], apis_to_be_tested[api]["params"], event["body"],
        #                                     event["rsp_body"])

        for _ in cv_events:
            #print(_)
            event = _[0]
            if _[1]:
                if int(_[1]["attributes"]["http_rsp_status_code"]) not in range(200, 299):
                    continue
            if event["url"]:
                # api = str(event["http-req-url"]).lstrip("/").rstrip("/").replace("/", "_").replace("-", "_").split("?")[
                #     0]
                api = str(event["http-req-url"]).lstrip("/").replace("/", "_S_").replace(" ","").split("?")[0]
                if api not in apis_to_be_tested:
                    apis_to_be_tested[api] = {}
                #apis_to_be_tested[api]["method"] = event["method"]
                method = event["method"].lower()
                if method not in apis_to_be_tested[api]:
                    apis_to_be_tested[api][method] = {}
                if self.static_headers_from_cfg:
                    for k, v in event["header"].items():
                        if k in self.static_headers_from_cfg:
                            event["header"][k] = str(self.static_headers_from_cfg[k])
                if "header" not in apis_to_be_tested[api][method]:
                    apis_to_be_tested[api][method]["header"] = {}
                apis_to_be_tested[api][method]["header"].update(event["header"])
                apis_to_be_tested[api][method]["url"] = event["url"]  # str(event["host"]).lower() + event["url"]
                if apis_to_be_tested[api][method].get("params"):
                    known_params = apis_to_be_tested[api][method].get("params")
                else:
                    known_params = []
                apis_to_be_tested[api][method]["params"] = new_spec_info.get(str(event["http-req-url"]).replace("//", "/"),{}).get(method,[])

                params_in_traffic = event.get("body",{}).keys()

                for _ in params_in_traffic:
                    if _ not in apis_to_be_tested[api][method]["params"]:
                        apis_to_be_tested[api][method]["params"].append(_)

                if apis_to_be_tested[api][method]["params"] is None:
                    apis_to_be_tested[api][method]["params"] = []

                apis_to_be_tested[api][method]["params"] = list(set(apis_to_be_tested[api][method]["params"]))
                apis_to_be_tested[api][method]["params"].append("host")
                apis_to_be_tested[api][method]["params"].append("url_prefix")
                apis_to_be_tested[api][method]["params"].append("access_token")

                host_url = str(event["host"]).lower()
                hosts.append(host_url)
                self._create_assertions_map(event["http-req-url"], apis_to_be_tested[api][method]["params"], event["body"],
                                            event["rsp_body"])


        for type in fuzz_types:
            fuzzing_details = self._get_fuzz_details(type)
            with open(os.path.join(templates_dir, 'fuzz_test.j2')) as file_:
                template = Template(file_.read())
            for k, v in apis_to_be_tested.items():
                #print(k, v)
                for method, info in v.items():
                    if not info["params"]:
                        continue
                # code = template.render(api_info=apis_to_be_tested[k], api_name=k, host_url=host_url)
                filename = str(k).replace("/", "_").replace("{", "").replace("}", "") + "_for_" + str(type) + "_fuzzing"
                if not os.path.exists("tests"):
                    os.mkdir("tests")

                with open("tests/test_" + str(filename) + ".py", 'w+') as fh:
                    fh.write(template.render(apis_metadata=apis_to_be_tested[k], api_name=k, host_url=host_url,
                                             fuzzing_details=fuzzing_details, fuzz_type=str(type)))
                files_created.add("test_" + str(filename))
        print("\n\t\t......done creating pytest methods for fuzzing: " + str(files_created))

    def get_captured_events(self):
        return self.ceobj.get_all_raw_events()  # last 3 weeks data

    # def _get_changed_apis(self):
    #     return OpenApiSpecDiff.OpenApiSpecDiff(self.apispec_one_path, self.apispec_two_path).diff

    def validate_pycode_for_syntax(self, code):
        code = str(code).replace(" ", "%20").replace("\n", "%0")
        headers = {
            'authority': 'extendsclass.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/81.0.4044.129 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://extendsclass.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://extendsclass.com/python-tester.html',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': '__gads=ID=da612839d6fc1303:T=1590622404:S=ALNI_MaEgA77keI5Spn5CckEF15zogbT6A; '
                      'PHPSESSID=123dabd5a795c756d1a5f45837f3217d; SERVERID100401=15211|Xs75G|Xs74y',
        }

        data = {
            '$source': code
        }
        #print(data)
        response = requests.post('https://extendsclass.com/python-tester-source', headers=headers, data=data)
        print(response.text)
        return response.json()

    def _process_event_data(self, apis_to_check=[], filters_to_query={}):
        print("\n\ncollecting events data from APIShark....")
        cv_requests = []
        events = self.ceobj.get_all_raw_events(apis_to_check, **filters_to_query)
        print("\n\nprocessing events data from APIShark....")
        processed_events = 0
        for event in events:
            if "http-req-header-Cv-Fuzzed-Event" in event["attributes"]["event_json"]:
                continue
            if int(str(event["attributes"]["http_rsp_status_code"]).split(" ")[0]) == 0:
                continue
            if apis_to_check:
                iflag = False
                # params_to_add = []
                for _ in apis_to_check:
                    if str(_).lower() in str(event["attributes"]["http_path"]).lower():
                        iflag = True
                        params_to_add = apis_to_check[_]
                    if iflag:
                        break

                if not iflag:
                    continue
            request = {"url": str(event["attributes"]["http_path"]), "method": str(event["attributes"]["http_method"]).lower()}
            header = {}
            body = {}
            req_params_found = {}
            for k, v in event["attributes"]["event_json"].items():
                if "http-req-header" in k:
                    if k == "http-req-headers-params":
                        continue
                    header[str(k).replace("http-req-header-", "")] = v
                if k in ["http-req-body-params", "http-req-query-params"]:
                    if v:
                        for param in v:
                            req_params_found[param] = {}

            for param in req_params_found:
                if "http-req-body-" + str(param) in event["attributes"]["event_json"]:
                    req_params_found[param] = event["attributes"]["event_json"]["http-req-body-" + str(param)]
                elif "http-req-query-" + str(param) in event["attributes"]["event_json"]:
                    req_params_found[param] = event["attributes"]["event_json"]["http-req-query-" + str(param)]

            rsp_params_found = {}
            for k, v in event["attributes"]["event_json"].items():
                if "http-rsp-header" in k:
                    if k == "http-rsp-headers-params":
                        continue
                    header[str(k).replace("http-rsp-header-", "")] = v
                if k in ["http-rsp-body-params", "http-rsp-query-params"]:
                    if v:
                        for param in v:
                            rsp_params_found[param] = {}

            for param in rsp_params_found:
                if "http-rsp-body-" + str(param) in event["attributes"]["event_json"]:
                    rsp_params_found[param] = event["attributes"]["event_json"]["http-rsp-body-" + str(param)]
                elif "http-rsp-query-" + str(param) in event["attributes"]["event_json"]:
                    rsp_params_found[param] = event["attributes"]["event_json"]["http-rsp-query-" + str(param)]

            request["host"] = event["attributes"]["event_json"]["http-req-host"]
            request["http-req-url"] = event["attributes"]["event_json"]["http-req-url"]
            request["header"] = header
            request["body"] = req_params_found
            request["rsp_body"] = rsp_params_found
            request["method"] = str(event["attributes"].get("http_method")).lower()
            #print(event["attributes"]["event_json"])
            request["rsp_code"] = str(event["attributes"]["http_rsp_status_code"]).split(" ")[0]
            if request["rsp_code"] not in [200, 201]:
                request["rsp_error"] = event["attributes"]["event_json"].get("http-rsp-body-error")
            # if str(request["rsp_code"]) not in self.params_captured_in_traffic:
            #     self.params_captured_in_traffic[request["rsp_code"]] = {}
            # if str(event["attributes"]["http_path"]) not in self.params_captured_in_traffic[request["rsp_code"]]:
            #     self.params_captured_in_traffic[request["rsp_code"]].update( { str(event["attributes"]["http_path"]) : {} } )
            #
            # for param, value in req_params_found.items():
            #     if param in self.params_captured_in_traffic[request["rsp_code"]][str(event["attributes"]["http_path"])]:
            #         # self.params_captured_in_traffic[str(event["attributes"]["http_path"]).lower()] = {}
            #         #if value not in self.params_captured_in_traffic[request["rsp_code"]][str(event["attributes"]["http_path"])][
            #         #    param]:
            #         self.params_captured_in_traffic[request["rsp_code"]][str(event["attributes"]["http_path"])][param].append(
            #                 value)
            #     else:
            #         self.params_captured_in_traffic[request["rsp_code"]][str(event["attributes"]["http_path"])][param] = [value]
            #     try:
            #         self.params_captured_in_traffic[request["rsp_code"]][str(event["attributes"]["http_path"])][param] = \
            #             list(set(self.params_captured_in_traffic[request["rsp_code"]][str(event["attributes"]["http_path"])][param]))
            #     except TypeError:
            #         pass

            # if str(request["rsp_code"]) not in self.params_captured_in_traffic:
            #     self.params_captured_in_traffic[request["rsp_code"]] = {}
            # if str(event["attributes"]["http_path"]) not in self.params_captured_in_traffic[request["rsp_code"]]:
            #     self.params_captured_in_traffic[request["rsp_code"]].update( { str(event["attributes"]["http_path"]) : [] } )
            url = event["attributes"]["http_path"]
            # if url.endswith("/"):
            #     url = url [:-1]
            if str(url) not in self.params_captured_in_traffic:
                self.params_captured_in_traffic[url] = {}
            if str(request["rsp_code"]) not in self.params_captured_in_traffic[url]:
                self.params_captured_in_traffic[url].update( { str(request["rsp_code"]) : {} } )
            if str(request["method"]) not in self.params_captured_in_traffic[url][request["rsp_code"]]:
                self.params_captured_in_traffic[url][request["rsp_code"]].update( { str(request["method"]) : [] } )
            params_found = {}
            for param, value in req_params_found.items():
                params_found[param] = value
            if params_found:
                if request["rsp_code"] not in [200, 201]:
                    params_found["$RESPONSE_ERROR"] = request.get("rsp_error")
                    params_found["$CV_EVENT_ID"] = "CV-EVENT-"+str(event["id"])
                self.params_captured_in_traffic[str(url)][request["rsp_code"]][request["method"]].append(params_found)
                # if param in self.params_captured_in_traffic[request["rsp_code"]][str(event["attributes"]["http_path"])]:
                #     # self.params_captured_in_traffic[str(event["attributes"]["http_path"]).lower()] = {}
                #     #if value not in self.params_captured_in_traffic[request["rsp_code"]][str(event["attributes"]["http_path"])][
                #     #    param]:
                #     self.params_captured_in_traffic[request["rsp_code"]][str(event["attributes"]["http_path"])][param].append(
                #             value)
                # else:
                #     self.params_captured_in_traffic[request["rsp_code"]][str(event["attributes"]["http_path"])][param] = [value]
                # try:
                #     self.params_captured_in_traffic[request["rsp_code"]][str(event["attributes"]["http_path"])][param] = \
                #         list(set(self.params_captured_in_traffic[request["rsp_code"]][str(event["attributes"]["http_path"])][param]))
                # except TypeError:
                #     pass
            #print(self.params_captured_in_traffic)
            cv_requests.append([request, event])
            processed_events+=1
        print("\nNo. of events processed from Cloudvector Enterprise Dashboard: " + str(processed_events))
        return cv_requests


def main():
    import sys
    import getpass
    import yaml
    if os.path.exists(os.path.join(os.getcwd(), "my_cesetup.yaml")):
        with open(os.path.join(os.getcwd(), "my_cesetup.yaml")) as fobj:
            ce_details = yaml.load(fobj, Loader=yaml.FullLoader)
    else:
        ce_details = {}
    print("\n\n")
    print("\t" * 7 + "# /***************************************************************\\")
    print("\t" * 7 + "# **                                                           **")
    print("\t" * 7 + "# **  / ___| | ___  _   _  __| \ \   / /__  ___| |_ ___  _ __  **")
    print("\t" * 7 + "# ** | |   | |/ _ \| | | |/ _` |\ \ / / _ \/ __| __/ _ \| '__| **")
    print("\t" * 7 + "# ** | |___| | (_) | |_| | (_| | \ V /  __/ (__| || (_) | |    **")
    print("\t" * 7 + "# **  \____|_|\___/ \__,_|\__,_|  \_/ \___|\___|\__\___/|_|    **")
    print("\t" * 7 + "# **                                                           **")
    print("\t" * 7 + "# **      (c) Copyright 2018 & onward, CloudVector             **")
    print("\t" * 7 + "# **                                                           **")
    print("\t" * 7 + "# **  For license terms, refer to distribution info            **")
    print("\t" * 7 + "# \***************************************************************/\n\n")

    print("\n\n" + "\t" * 4 + "*****" * 20)
    print ("\t" * 8 + "CloudVector - Dynamic Application Security Testing")
    print("\t" * 4 + "*****" * 20)
    # if ce_details:
    #     print("\nAPIShark details from my_cesetup.yaml:\n\t" + str(ce_details) + "\n")
    config = input("\n\nEnter the CloudVector config file path: ")
    if os.path.exists(config):
        with open(config) as fobj:
            ce_details = yaml.load(fobj, Loader=yaml.FullLoader)
    print("\nAPIShark details from my_cesetup.yaml:\n\t" + str(ce_details["ce_setup"]) + "\n")
    ce_host = ce_details["ce_setup"]["ce_host"]
    ce_username = ce_details["ce_setup"]["ce_username"]
    if not config:
        if ce_details.get("ce_host"):
            ce_host = ce_details["ce_host"]
        else:
            ce_host = input("Enter APIShark host in format <host>:<port> : ")
        if ce_details.get("ce_username"):
            ce_username = ce_details["ce_username"]
        else:
            ce_username = input("Enter your APIShark username : ")
    ce_password = getpass.getpass(prompt="APIShark password:")
    option = input("what do you want to do? (1: Compare SPECs for diff or 2: Use new SPEC):")
    if int(option) == 1:
        input_spec_one = input("Enter absolute path to Old API SPEC(Version A): ")
        input_spec_two = input("Enter absolute path to New API SPEC(Version B) : ")
        cover_only_diff = input("Do you want to process only the missing parameters? (Y/N) : ")
    else:
        input_spec_one = ""
        input_spec_two = input("Enter absolute path to Open API SPEC: ")
        cover_only_diff = "n"
    input_params_file = input("Enter absolute path to input parameters file(press Enter for None):")
    if not os.path.exists(os.path.join(os.getcwd(), "my_cesetup.yaml")):
        with open(os.path.join(os.getcwd(), "my_cesetup.yaml"), "w+") as fobj:
            yaml.dump({"ce_host": str(ce_host), "ce_username": str(ce_username)}, fobj)
    enable_fuzzing = False

    if sys.argv[1:]:
        if sys.argv[1:][0] == "--fuzz":
            print("\nFuzzing enabled!\n")
            enable_fuzzing = True
    CloudvectorDAST(str(input_spec_one).strip(), str(input_spec_two).strip(), ce_host, ce_username, ce_password, config,
                    str(cover_only_diff).lower(), input_params_file, enable_fuzzing)
    print("\n Test generation complete! Making the pycode PEP complaint ( https://www.python.org/dev/peps/pep-0008/ ).....\n")
    os.system("autopep8 --in-place --aggressive --aggressive tests/*.py")
    print("\n\t\t..........done")


if __name__ == "__main__":
    main()
    # print(key_lookup("amount",{'amount': 33, 'description': '', 'user_id': '2', 'account_id': 1}))

    # print(key_lookup("amount",{'deposit': {'account_id': 1, "abcd":"34", 'amount': '33.0', 'deposit_date': {'amount':34, 'date':'2020-05-26T10:44:19.095Z'}, 'deposit_file_url': None, 'id': 4709}}))
