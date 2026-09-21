# Studionet lifecycle evidence

Network verified by the `gltest` configuration and Studio session:

- Alias: `studionet`
- Chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- Direct Mode dependency: `genlayer-test==0.29.2`

The lifecycle below was run with:

```text
gltest tests/integration/test_studionet_lifecycle.py -v -s --network studionet
```

Result: **1 passed**. The final run produced the following finalized contracts and transactions.

| Item | Evidence |
|---|---|
| ConditionLatch address | `0x84166D3950c6C655f9D70ce992597177CD0fff1c` |
| ConditionLatch deployment transaction | `0xca0ea424947c6db8519cfe2227c8798bc2166224149d7165df59f85efc0ac61d` |
| ConditionGate address | `0x805Db02F414833D2aF4008016280706163ff8057` |
| ConditionGate deployment transaction | `0xf3991d73b82c6ae8d490edbb13414fae96d4ada139547616b26fb30fc1120c3b` |
| Condition creation transaction | `0x2abc8fea61bd7580da5975619a66655f17e837a3688be6a7d0e4cd985a4adb73` |
| HTTPS source registration transaction | `0x46571d1d87ef4a520212e25fb5bfb9405de01dec72cb64f82c1d4d1cc2d80695` |
| Seal transaction | `0xc352f13a4fb31cdbad13050ecc01a52ee0bc5cdc77c4d55febe296b76a516f20` |
| Definition hash | `74c778ae17114e83b402efcefd8d0850d9db8bb4ae0b48582076c054cb875161` |
| Generation | `1` |
| Observation round 1 transaction (TRUE, remains ACTIVE) | `0xa24876ecf1fa983aee4b6461b1370d93dee14b6432721d8912ac7130a4e7f18f` |
| Observation round 2 transaction (TRUE, remains ACTIVE) | `0x24a9bee4d9326e6774af71079041aec1b5880ff67cd938dcc473c2c42b8f15f6` |
| Observation round 3 transaction (TRUE, latches) | `0x8b723bbc682c7a0235a1c8fc281ee8628cb4acb0970aafacd4dd3d8b9f6d17eb` |
| Final snapshot hash | `5afd3d0cb6637cbdd8bd991dc80c1d2495c9a69451b710cbe2526ff5edf7dff9` |
| Final round hash | `62d02ec76c24d35af03274556ea92f1a48796cdb3d7f0fdc1afd7bed82256555` |
| Successful ConditionGate action transaction | `0xac2e7de2b95c163922721f506b4ab8bf67b903c151628095da0e3e178fbfa435` |
| Replay rejection | Finalized transaction `0x38f1751ebef7d77b88e07f0a4671439d2711e32b8afe3708af366022cd04e233`; execution `ERROR`, rollback: `action hash already consumed` |
| Wrong-definition rejection | Finalized transaction `0x78310e7b94dbc165ed04e1ad9b3e0260bb6ca10d12d55e6311d6ee022fb71b5a`; execution `ERROR`, rollback: `ConditionLatch does not establish the pinned latch state` |
| Wrong-generation rejection | Finalized transaction `0xafc22ac9f18bfb55ac9c9e45fc8b81619a9d75a484c6f9a6b2027353a29530cf`; execution `ERROR`, rollback: `ConditionLatch does not establish the pinned latch state` |

An earlier Gate deployment attempt finalized with a contract error because the lifecycle passed the latch address as a plain string. The failed transaction was `0x7ba13c8966c53f8cb69297b08d8368960ccfe4c5310c826baf901732abfaaa4e`; its error was `AttributeError: 'str' object has no attribute 'as_bytes'`. The lifecycle now passes a typed `CalldataAddress`; the corrected Gate deployment and lifecycle above succeeded.

Immutable TRUE fixture commit: `a820417c7b4fd6c74f20d621fcc4801cbeec222b`.
