import re
from functools import lru_cache
from typing import Dict, Union

from eth_abi import decode, encode
from eth_utils.abi import (
    collapse_if_tuple,
    function_abi_to_4byte_selector,
    function_signature_to_4byte_selector,
)
from eth_utils.hexadecimal import decode_hex, encode_hex

class DecodeError(Exception):
    pass

@lru_cache(maxsize=4096)
def parse_signature(s):
    pattern = r'([a-zA-Z0-9_]+|\([a-zA-Z0-9,_]+\))'
    return re.findall(pattern, s)

@lru_cache(maxsize=1024)
def parse_arg_string(s):
    return s.strip("()").split(",")

class Signature:
    """
    Encode/Decode function text signature or ABI,
    eg:
        function text signature:
            balanceOf(address)(uint256)
    or ABI
        {
            "name": "balanceOf",
            "inputs": [{"name": "account", "type": "address"}],
            "outputs": [{"name": "", "type": "uint256"}],
        }

    """

    def __init__(self, signature: Union[str, Dict]):
        self.signature = signature
        if isinstance(signature, str):
            parts = parse_signature(signature.strip().replace(" ", ""))

            self.input_types = parse_arg_string(parts[1])
            self.output_types = parse_arg_string(parts[2])
            function = "".join(parts[:2])
            self.fourbyte = function_signature_to_4byte_selector(function)

        elif isinstance(signature, dict):
            self.fourbyte = function_abi_to_4byte_selector(signature)
            input_types = f'({",".join(collapse_if_tuple(abi) for abi in signature.get("inputs", []))})'
            output_types = f'({",".join(collapse_if_tuple(abi) for abi in signature.get("outputs", []))})'
            self.input_types = parse_arg_string(input_types)
            self.output_types = parse_arg_string(output_types)
            

    def encode_data(self, args=None):
        data = self.fourbyte
        if args:
            for i in range(len(self.input_types)):
                data += encode(self.input_types[i : i + 1], args[i:i+1])
        return encode_hex(data)

    def decode_data(self, data: Union[str, bytes], ignore_error: bool = False):
        if isinstance(data, str):
            data = decode_hex(data)
        try:
            decoded = decode(self.output_types, data)
        except Exception as ex:
            if ignore_error:
                return None
            msg = f"failed to decode data: {data} of signature: {self.signature}"
            raise DecodeError(msg) from ex

        return decoded if len(decoded) > 1 else decoded[0]
