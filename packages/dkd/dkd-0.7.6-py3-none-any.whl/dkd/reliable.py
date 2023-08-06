# -*- coding: utf-8 -*-
#
#   Dao-Ke-Dao: Universal Message Module
#
#                                Written in 2019 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2019 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

from typing import Optional

from .secure import SecureMessage


class ReliableMessage(SecureMessage):
    """This class is used to sign the SecureMessage
    It contains a 'signature' field which signed with sender's private key

        Instant Message signed by an asymmetric key
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        data format: {
            //-- envelope
            sender   : "moki@xxx",
            receiver : "hulk@yyy",
            time     : 123,
            //-- content data and key/keys
            data     : "...",  // base64_encode(symmetric)
            key      : "...",  // base64_encode(asymmetric)
            keys     : {
                "ID1": "key1", // base64_encode(asymmetric)
            },
            //-- signature
            signature: "..."   // base64_encode()
        }
    """

    def __new__(cls, msg: dict):
        """
        Create reliable secure message

        :param msg: message info
        :return: ReliableMessage object
        """
        if msg is None:
            return None
        elif cls is ReliableMessage:
            if isinstance(msg, ReliableMessage):
                # return ReliableMessage object directly
                return msg
        # new ReliableMessage(dict)
        return super().__new__(cls, msg)

    def __init__(self, msg: dict):
        if self is msg:
            # no need to init again
            return
        super().__init__(msg)
        # lazy
        self.__signature = None

    @property
    def signature(self) -> bytes:
        if self.__signature is None:
            base64 = self.get('signature')
            assert base64 is not None, 'signature of reliable message cannot be empty: %s' % self
            self.__signature = self.delegate.decode_signature(signature=base64, msg=self)
        return self.__signature

    """
        Sender's Meta
        ~~~~~~~~~~~~~
        Extends for the first message package of 'Handshake' protocol.
    """
    @property
    def meta(self) -> Optional[dict]:
        return self.get('meta')

    @meta.setter
    def meta(self, value: dict):
        if value is None:
            self.pop('meta', None)
        else:
            self['meta'] = value

    """
        Sender's Profile
        ~~~~~~~~~~~~~
        Extends for the first message package of 'Handshake' protocol.
    """
    @property
    def profile(self) -> Optional[dict]:
        return self.get('profile')

    @profile.setter
    def profile(self, value: dict):
        if value is None:
            self.pop('profile', None)
        else:
            self['profile'] = value

    """
        Verify the Reliable Message to Secure Message
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            +----------+      +----------+
            | sender   |      | sender   |
            | receiver |      | receiver |
            | time     |  ->  | time     |
            |          |      |          |
            | data     |      | data     |  1. verify(data, signature, sender.PK)
            | key/keys |      | key/keys |
            | signature|      +----------+
            +----------+
    """

    def verify(self) -> Optional[SecureMessage]:
        """
        Verify the message.data with signature

        :return: SecureMessage object if signature matched
        """
        data = self.data
        if data is None:
            raise ValueError('failed to decode content data: %s' % self)
        signature = self.signature
        if signature is None:
            raise ValueError('failed to decode message signature: %s' % self)
        # 1. verify data signature
        if self.delegate.verify_data_signature(data=data, signature=signature, sender=self.sender, msg=self):
            # 2. pack message
            msg = self.copy()
            msg.pop('signature')  # remove 'signature'
            return SecureMessage(msg)
        # else:
        #     raise ValueError('Signature error: %s' % self)
