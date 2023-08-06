import ujson as json


async def get_rules():
    pass


{
    "name": "这是一条联动",
    "positionId": "real1.xxxxxxxxx",
    "conditionRelation": "0",
    "conditions": [
        {
            "trigger": "TD.lumi.sensor_motion.motion",
            "did": "lumi.xxxxxx",
            "model": "lumi.sensor_motion.aq1",
            "params": []
        }
    ],
    "actions": [
        {
            "did": "lumi.xxxxx",
            "action": "AD.lumi.gateway.open_corridor_light",
            "model": "lumi.gateway.aq1",
            "params": []
        }
    ]
}

# property value == xxx
# (If (eq property_value xxx)
# )
