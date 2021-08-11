# will be handy if up-scaling
# free plan of atlas not allowing $lookup aggregation

event_venue_pipeline = [
    {
        "$lookup": {
            "from": "$venue",
            "localField": "venue_ref",
            "foreignField": "venue_ref",
            "as": "venue"
        }
    },
    {"$unwind": "venue"},
    {
        "$lookup": {
            "from": "$category",
            "localField": "category",
            "foreignField": "cat_code",
            "as": "category"
        }
    },
    {"$unwind": "category"},
]

