
from decimal import Decimal
from multicall import Multicall, Call

mc = Multicall("https://mainnet.infura.io/v3/xyz")

result = mc.agg(
    [
        Call(
            target="0xdac17f958d2ee523a2206206994597c13d831ec7",
            function="balanceOf(address)(uint256)",
            args=("0xa929022c9107643515f5c777ce9a910f0d1e490c",),
            # returns=[],
        ),
        Call(
            target="0xdac17f958d2ee523a2206206994597c13d831ec7",
            function="balanceOf(address)(uint256)",
            args=("0x47ac0fb4f2d84898e4d9e7b4dab3c24507a6d503",),
            request_id="0x47ac0fb4f2d84898e4d9e7b4dab3c24507a6d503",
        ),
        Call(
            "0x35d1b3f3d7966a1dfe207aa4514c12a259a0492b",
            "ilks(bytes32)((uint256,uint256,uint256,uint256,uint256))",
            args=[b"ETH-A"],
            request_id="ETH-A",
        ),
    ]
)

print(result)