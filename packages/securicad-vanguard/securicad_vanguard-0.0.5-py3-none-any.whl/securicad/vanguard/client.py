# Copyright 2020 Foreseeti AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import sys
import json
import time
import math
import base64

import requests
from requests.exceptions import HTTPError

import securicad.vanguard
from securicad.vanguard.model import Model
from securicad.vanguard.exceptions import (
    VanguardCredentialsError,
    AwsCredentialsError,
    RateLimitError,
)

import boto3
import botocore
from botocore.config import Config
from pycognito.aws_srp import AWSSRP


class Client:
    def __init__(self, username, password, url, region="eu-central-1"):
        self.base_url = url
        self.backend_url = f"{self.base_url}/backend"

        self.token = self.authenticate(username, password, region)
        self.headers = {
            "User-Agent": f"Vanguard SDK {securicad.vanguard.__version__}",
            "Authorization": self.token,
        }
        self.register()

    def simulate(self, model, profile, export_report=False):
        if not model.result_map:
            raise ValueError("Model must have at least one high value asset")
        simulation_tag = self.simulate_model(model.model, profile.value)
        results = self.wait_for_results(simulation_tag)
        parsed_results = self.parse_results(results["results"], model)
        if export_report:
            parsed_results["Report"] = results
        return parsed_results

    def get_model(self, **kwargs):
        if "data" in kwargs and kwargs["data"] is not None:
            model_tag = self.build_from_config(kwargs.get("data"), kwargs.get("vuln_data"))
        else:
            model_tag = self.build_from_role(
                kwargs.get("access_key"),
                kwargs.get("secret_key"),
                kwargs.get("region"),
                kwargs.get("vuln_data"),
            )
        try:
            model = self.wait_for_model(model_tag)

        except HTTPError as e:
            code = e.response.status_code
            error_message = e.response.json().get("error")
            if code == 400 and error_message == "Provided credentials were not accepted by AWS":
                raise AwsCredentialsError(error_message)

            msg1 = "You don't have permission to perform the required action"
            msg2 = "You don't have permission to perfom a required action"
            if code == 400 and (error_message.startswith(msg1) or error_message.startswith(msg2)):
                raise AwsCredentialsError(error_message)
            raise e

        return Model(model)

    def authenticate(self, username, password, region):
        client = boto3.client(
            "cognito-idp", region_name=region, config=Config(signature_version=botocore.UNSIGNED),
        )
        client_id, pool_id = self.cognito_params(region)
        aws = AWSSRP(
            username=username,
            password=password,
            pool_id=pool_id,
            client_id=client_id,
            client=client,
        )
        try:
            access_token = aws.authenticate_user()["AuthenticationResult"]["AccessToken"]
            jwt_token = f"JWT {access_token}"
            return jwt_token
        except:
            error_message = "Invalid password or username"
            raise VanguardCredentialsError(error_message)

    def register(self):
        res = requests.get(url=f"{self.backend_url}/whoami", headers=self.headers)
        res.raise_for_status()

    def encode_data(self, data):
        if isinstance(data, dict):
            content = json.dumps(data).encode("utf-8")
        elif isinstance(data, bytes):
            content = data
        else:
            raise ValueError(f"a bytes-like object or dict is required, not {type(data)}")
        return content

    def build_from_role(self, access_key, secret_key, region, vuln_data=None):
        url = f"{self.backend_url}/build_from_role"
        data = {
            "region": region,
            "access_key": access_key,
            "secret_key": secret_key,
            "include_inspector": False,
        }

        if vuln_data:
            vuln_content = self.encode_data(vuln_data)
            vuln_base64d = base64.b64encode(vuln_content).decode("utf-8")
            data["additionalFiles"] = [
                {"content": vuln_base64d, "filename": "vulnerabilities.json"}
            ]

        res = requests.put(url, headers=self.headers, json=data)
        res.raise_for_status()
        return res.json()["response"]["mtag"]

    def build_from_config(self, json_data, vuln_data=None):
        url = f"{self.backend_url}/build_from_config"

        model_content = self.encode_data(json_data)
        model_base64d = base64.b64encode(model_content).decode("utf-8")

        data = {"files": [{"content": model_base64d, "filename": "apimodel.json"}]}

        if vuln_data:
            vuln_content = self.encode_data(vuln_data)
            vuln_base64d = base64.b64encode(vuln_content).decode("utf-8")
            data["additionalFiles"] = [
                {"content": vuln_base64d, "filename": "vulnerabilities.json"}
            ]

        res = requests.put(url, headers=self.headers, json=data)
        res.raise_for_status()
        return res.json()["response"]["mtag"]

    def model_request(self, model_tag):
        url = f"{self.backend_url}/get_model"
        data = {"mtag": model_tag}
        res = requests.post(url, headers=self.headers, json=data)
        res.raise_for_status()
        if res.status_code == 204:
            return res.status_code, {}
        else:
            return res.status_code, res.json()["response"]

    def simulate_model(self, model, profile):
        url = f"{self.backend_url}/simulate"
        model["name"] = "vanguard_model"
        data = {"model": model, "profile": profile, "demo": False}
        res = requests.put(url, headers=self.headers, json=data)
        if res.status_code == 429:
            raise RateLimitError(
                "You are currently ratelimited, please wait for other simulations to complete"
            )
        res.raise_for_status()
        return res.json()["response"]["tag"]

    def get_results(self, simulation_tag):
        url = f"{self.backend_url}/results"
        data = {"tag": simulation_tag}
        res = requests.post(url, headers=self.headers, json=data)
        res.raise_for_status()
        if res.status_code == 204:
            return res.status_code, {}
        else:
            return res.status_code, res.json()["response"]

    def wait_for_results(self, simulation_tag):
        results = self.wait_for_response("get_results", simulation_tag)
        return results

    def wait_for_model(self, model_tag):
        return self.wait_for_response("model_request", model_tag)

    def parse_results(self, results, model):
        formatted_results = {}
        for key, data in results["data"].items():
            hv_asset = model.result_map[key]
            result = self.format_result(data)
            hv_asset.update(result)
            hv_asset["id"] = hv_asset["id"]["value"]
            if hv_asset["metaconcept"] not in formatted_results:
                formatted_results[hv_asset["metaconcept"]] = {}
            formatted_results[hv_asset["metaconcept"]][hv_asset["id"]] = hv_asset
        return formatted_results

    def format_result(self, data):
        ttc50 = float(data["ttc50"])
        if ttc50 == sys.float_info.max:
            ttc50 = math.inf
        else:
            ttc50 = int(ttc50)
        prob = int(float(data["probability"]) * 100)
        result = {
            "probability": float(data["probability"]),
            "ttc": ttc50,
            "name": data["object_name"],
        }
        return result

    def wait_for_response(self, function, *args):
        status = 204
        while status == 204:
            time.sleep(5)
            status, data = getattr(self, function)(*args)
            if status == 200:
                return data

    def cognito_params(self, region):
        url = f"{self.base_url}/bundle.js"
        pattern = fr"{{\s*UserPoolId:\s*['\"]({region}[^'\"]+)['\"],\s*ClientId:\s*['\"]([^'\"]+)['\"]\s*}}"
        res = requests.get(url)
        res.raise_for_status()
        data = res.text
        match = re.search(pattern, data)
        if match:
            userpool_id = str(match.group(1))
            client_id = str(match.group(2))
            return client_id, userpool_id
        raise EnvironmentError("Failed to get cognito parameters")
