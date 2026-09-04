json = [
    [
        "00002_index_1",
        {
            "seg": {
                "0": 3,
                "1": -1,
                "2": -1,
                "3": -1,
                "4": 0,
                "5": 0,
                "6": 5
            },
            "inst": [
                [
                    1,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    1
                ]
            ],
            "bottom": {}
        }
    ]
]
import numpy as np

np.set_printoptions(threshold=np.inf, linewidth=np.inf)
print(np.array(json[0][1]["inst"]))