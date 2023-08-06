#!/usr/bin/env python3

from btcpy.structs.script import Script, ScriptBuilder, P2shScript, \
    IfElseScript, Hashlock256Script, RelativeTimelockScript
from btcpy.structs.transaction import Sequence
from binascii import unhexlify

from .utils import script_from_address, is_address
from ...utils.exceptions import AddressError
from ..config import bitcoin

import hashlib

# Bitcoin config
bitcoin = bitcoin()


# Hash Time Lock Contract
class HTLC:
    """
    Bitcoin Hash Time Lock Contract (HTLC) class.

    :param network: Bitcoin network, defaults to testnet.
    :type network: str
    :returns:  HTLC -- Bitcoin HTLC instance.

    .. note::
        Bitcoin has only two networks, ``mainnet`` and ``testnet``.
    """

    # Initialization
    def __init__(self, network="testnet"):
        # Bitcoin network
        self.mainnet = None
        self.network = network
        if self.network == "mainnet":
            self.mainnet = True
        elif self.network == "testnet":
            self.mainnet = False
        else:
            raise ValueError("invalid network, only mainnet or testnet")
        # HTLC script
        self.script = None

    # Initialize new HTLC Contract script
    def init(self, secret_hash, recipient_address, sender_address, sequence=bitcoin["sequence"]):
        """
        Initialize Bitcoin Hash Time Lock Contract (HTLC).

        :param secret_hash: secret sha-256 hash.
        :type secret_hash: str
        :param recipient_address: Bitcoin recipient address.
        :type recipient_address: str
        :param sender_address: Bitcoin sender address.
        :type sender_address: str
        :param sequence: Bitcoin sequence number of expiration block, defaults to 1000.
        :type sequence: int
        :returns: HTLC -- Bitcoin Hash Time Lock Contract (HTLC) instance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init(secret_hash="3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", recipient_address="muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", sender_address="mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", sequence=1000)
        <swap.providers.bitcoin.htlc.HTLC object at 0x0409DAF0>
        """

        # Checking parameter instances
        if not isinstance(secret_hash, str):
            raise TypeError("secret hash must be string format")
        if len(secret_hash) != 64:
            raise ValueError("invalid secret hash, length must be 64.")
        if not isinstance(recipient_address, str):
            raise TypeError("recipient address must be string format")
        if not is_address(recipient_address, self.network):
            raise AddressError("invalid %s recipient %s address" % (self.network, recipient_address))
        if not isinstance(sender_address, str):
            raise TypeError("sender address must be string format")
        if not is_address(sender_address, self.network):
            raise AddressError("invalid %s sender %s address" % (self.network, sender_address))
        if not isinstance(sequence, int):
            raise TypeError("sequence must be integer format")

        # HASH TIME LOCK CONTRACT SCRIPT
        self.script = IfElseScript(
            # If branch
            Hashlock256Script(  # Hash lock 250
                hashlib.sha256(unhexlify(secret_hash)).digest(),  # Secret double hash for (OP_HASH256)
                script_from_address(
                    address=recipient_address, network=self.network)  # Script hash of account two
            ),
            # Else branch
            RelativeTimelockScript(  # Relative time locked script
                Sequence(sequence),  # Expiration blocks
                script_from_address(
                    address=sender_address, network=self.network)  # Script hash of account one
            )
        )
        return self

    # Hash time lock contract form opcode script
    def from_opcode(self, opcode):
        """
        Initiate Bitcoin Hash Time Lock Contract (HTLC) from opcode script.

        :param opcode: Bitcoin opcode script.
        :type opcode: str
        :returns: HTLC -- Bitcoin Hash Time Lock Contract (HTLC) instance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc_opcode_script = "OP_IF OP_HASH256 821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158 OP_EQUALVERIFY OP_DUP OP_HASH160 98f879fb7f8b4951dee9bc8a0327b792fbe332b8 OP_EQUALVERIFY OP_CHECKSIG OP_ELSE e803 OP_CHECKSEQUENCEVERIFY OP_DROP OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF"        >>> htlc.from_opcode(opcode=htlc_opcode_script)
        <swap.providers.bitcoin.htlc.HTLC object at 0x0409DAF0>
        """

        if isinstance(opcode, str):
            bytecode = Script.compile(opcode)
            self.script = ScriptBuilder.identify(bytecode)
            return self
        raise TypeError("op_code must be string format")

    # Hash time lock contract form bytecode
    def from_bytecode(self, bytecode):
        """
        Initiate Bitcoin Hash Time Lock Contract (HTLC) from bytecode.

        :param bytecode: Bitcoin bytecode.
        :type bytecode: str
        :returns: HTLC -- Bitcoin Hash Time Lock Contract (HTLC) instance.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc_bytecode = "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68"
        >>> htlc.from_bytecode(bytecode=htlc_bytecode)
        <swap.providers.bitcoin.htlc.HTLC object at 0x0409DAF0>
        """

        if isinstance(bytecode, str):
            self.script = ScriptBuilder.identify(bytecode)
            return self
        raise TypeError("bytecode must be string format")

    # Bytecode HTLC script
    def bytecode(self):
        """
        Get Bitcoin htlc bytecode.

        :returns: str -- Bitcoin Hash Time Lock Contract (HTLC) bytecode.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init("3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> htlc.bytecode()
        "63aa20821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e01588876a91498f879fb7f8b4951dee9bc8a0327b792fbe332b888ac6702e803b27576a91464a8390b0b1685fcbf2d4b457118dc8da92d553488ac68"
        """

        if self.script is None:
            raise ValueError("htlc script is none, initialization htlc first")
        return self.script.hexlify()

    # Decompiled HTLC script
    def opcode(self):
        """
        Get Bitcoin htlc opcode.

        :returns: str -- Bitcoin Hash Time Lock Contract (HTLC) opcode.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init("3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> htlc.opcode()
        "OP_IF OP_HASH256 821124b554d13f247b1e5d10b84e44fb1296f18f38bbaa1bea34a12c843e0158 OP_EQUALVERIFY OP_DUP OP_HASH160 98f879fb7f8b4951dee9bc8a0327b792fbe332b8 OP_EQUALVERIFY OP_CHECKSIG OP_ELSE e803 OP_CHECKSEQUENCEVERIFY OP_DROP OP_DUP OP_HASH160 64a8390b0b1685fcbf2d4b457118dc8da92d5534 OP_EQUALVERIFY OP_CHECKSIG OP_ENDIF"
        """

        if self.script is None:
            raise ValueError("htlc script is none, initialization htlc first")
        return self.script.decompile()

    # HTLC script hash
    def hash(self):
        """
        Get Bitcoin Hash Time Lock Contract (HTLC) hash.

        :returns: str -- Bitcoin Hash Time Lock Contract (HTLC) hash.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init("3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> htlc.hash()
        "a9142bb013c3e4beb08421dedcf815cb65a5c388178b87"
        """

        if self.script is None:
            raise ValueError("htlc script is none, initialization htlc first")
        return str(P2shScript(self.script.p2sh_hash()).hexlify())

    # HTLC script address
    def address(self):
        """
        Get Bitcoin Hash Time Lock Contract (HTLC) address.

        :returns: str -- Bitcoin Hash Time Lock Contract (HTLC) address.

        >>> from swap.providers.bitcoin.htlc import HTLC
        >>> htlc = HTLC(network="testnet")
        >>> htlc.init("3a26da82ead15a80533a02696656b14b5dbfd84eb14790f2e1be5e9e45820eeb", "muTnffLDR5LtFeLR2i3WsKVfdyvzfyPnVB", "mphBPZf15cRFcL5tUq6mCbE84XobZ1vg7Q", 1000)
        >>> htlc.address()
        "2MwEDybGC34949zgzWX4M9FHmE3crDSUydP"
        """

        if self.script is None:
            raise ValueError("htlc script is none, initialization htlc first")
        return str(P2shScript(self.script.p2sh_hash()).address(mainnet=self.mainnet))
