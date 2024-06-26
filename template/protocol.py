# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import base64
import typing

import bittensor as bt
import pydantic

from schemas.bit_ads import GetMinerUniqueIdResponse, Campaign


# This is the protocol for the dummy miner and validator.
# It is a simple request-response protocol where the validator sends a request
# to the miner, and the miner responds with a dummy response.

# ---- miner ----
# Example usage:
#   def dummy( synapse: Dummy ) -> Dummy:
#       synapse.dummy_output = synapse.dummy_input + 1
#       return synapse
#   axon = bt.axon().attach( dummy ).serve(netuid=...).start()

# ---- validator ---
# Example usage:
#   dendrite = bt.dendrite()
#   dummy_output = dendrite.query( Dummy( dummy_input = 1 ) )
#   assert dummy_output == 2


class Dummy(bt.Synapse):
    """
    A simple dummy protocol representation which uses bt.Synapse as its base.
    This protocol helps in handling dummy request and response communication between
    the miner and the validator.

    Attributes:
    - dummy_input: An integer value representing the input request sent by the validator.
    - dummy_output: An optional integer value which, when filled, represents the response from the miner.
    """

    # Required request input, filled by sending dendrite caller.
    dummy_input: int

    # Optional request output, filled by recieving axon.
    dummy_output: typing.Optional[int] = None

    def deserialize(self) -> int:
        """
        Deserialize the dummy output. This method retrieves the response from
        the miner in the form of dummy_output, deserializes it and returns it
        as the output of the dendrite.query() call.

        Returns:
        - int: The deserialized response, which in this case is the value of dummy_output.

        Example:
        Assuming a Dummy instance has a dummy_output value of 5:
        >>> dummy_instance = Dummy(dummy_input=4)
        >>> dummy_instance.dummy_output = 5
        >>> dummy_instance.deserialize()
        5
        """
        return self.dummy_output


class Task(bt.Synapse):
    dummy_input: Campaign
    dummy_output: typing.Optional[GetMinerUniqueIdResponse] = None

    def deserialize(self) -> typing.Optional[GetMinerUniqueIdResponse]:
        return self.dummy_output

    def to_headers(self) -> dict:
        result = super().to_headers()
        result["bt_header_input_obj_dummy_input"] = base64.b64encode(
            self.dummy_input.json().encode()
        ).decode("utf-8")
        return result


"""
Represents a software version with major, minor, and patch components.
"""


class Version(pydantic.BaseModel):
    major_version: typing.Optional[int] = None
    minor_version: typing.Optional[int] = None
    patch_version: typing.Optional[int] = None


class MapSynapse(bt.Synapse):
    version: typing.Optional[Version] = None


"""
A specialized Synapse representing the status of a miner, 
including its availability and memory resources.
"""


class MinerStatus(MapSynapse):
    free_memory: typing.Optional[int] = None
    available: typing.Optional[bool] = None


class SpeedTest(MapSynapse):
    result: typing.Optional[typing.Dict] = None


class Retrieve(bt.Synapse):
    pass


class TextToSpeech(bt.Synapse):
    pass


class MusicGeneration(bt.Synapse):
    pass


class VoiceClone(bt.Synapse):
    pass


"""
Defines the status of a validator, particularly whether it is available for processing requests.
"""


class ValidatorStatus(pydantic.BaseModel):
    available: typing.Optional[bool] = None
