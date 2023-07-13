def gpt_prompt(params):
    return f"""
       Describe a world in vivid detail with the following features:

       {params}

       Include a description of the world's landscapes, its major species, their cities/settlements/colonies, 
        with a significant character.
       Based on these, describe an overview of the world's historical lore in three epochs.
       Your response should follow this structure:
           {{
            "name": (a creative name based on its features),
            "blurb": (a brief one-liner about the world),
            "description": (a one paragraph description),
            "geodynamics": {{
                "size": (eg, "large"),
                "climate": (eg, "lush rainforest")
            }}
            "magictechnology": {{
                "magic": true,
                "technology": 6,
                "genres": [(eg fantasy, sci-fi, _-punk, vaporwave, etc)]  
            }}
            "species": [{{
                "name": (name of species),
                "alignment": (DnD alignment),
                "politics": (one sentence about their politics)
            }}]
            "locations": [{{
                "type": (eg city, settlement, landmark, monument, etc),
                "name": (name),
                "description": (description)
               }}]
            "characters": [{{
               "name": (name),
               "description": (description)
            }}]
            "events": [{{
                "time": "2000",
                "description": "A rebellion"
            }}]
            "history": [
                 eg, "The Age of Creation saw the birth of the world and the awakening of its first inhabitants.",
                 eg, "The Era of Darkness plunged Mythos into chaos, with monsters and dark forces threatening its existence.",
                 eg, "The Age of Heroes brought forth legendary figures who shaped the world's destiny."
               ]
             }}
       """

