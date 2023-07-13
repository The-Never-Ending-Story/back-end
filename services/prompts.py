def gpt_prompt(params):
    return f"""
       Please describe a world in vivid detail with the following features:

       {params}

       Include descriptions of:
        -the world's landscapes, 
        -its major species, 
        -2 of their cities/settlements/colonies, and one other significant location,
        -a significant character for each location,
        -and a significant event each character participated in.
       Based on these, describe an overview of the world's historical lore in three epochs.
       
       Your response should follow this structure:
           {{
            "name": (a creative name based on its features. may be inspired by genre but not directly use genre names),
            "blurb": (a brief one-liner about the world),
            "description": (a one paragraph description),
            "geoDynamics": {{
                "size": (scope),
                "climate": (natural conditions)
            }}
            "magicTechnology": {{
                "magic": (Boolean),
                "technology": (Integer),
                "genres": [(eg fantasy, sci-fi, _-punk, vaporwave)]  
            }}
            "species": [{{
                "name": (name of species),
                "description": (description),
                "politics": (one sentence about their politics),
                "imagine": (image prompt; each imagine prompt should be a detailed standalone one-paragraph natural language description of appearance only, no names. include appropriate stylistic instructions)")
            }}]
            "locations": [{{
                "type": (eg city, settlement, landmark, monument),
                "climate": (local microclimate),
                "name": (name),
                "lore": (description),
                "imagine": (image prompt)
               }}]
            "characters": [{{
               "name": (name),
               "age": (Integer),
               "species": (name of species),
               "alignment": (DnD alignment),
               "lore": String,
               "imagine": (image prompt)
            }}]
            "events": [{{
                "name": (name),
                "type": (type of event)
                "age": (the epoch of the world),
                "time": (calendar year),
                "lore": (description),
                "imagine": (image prompt)
            }}]
            "history": [
                 eg, "The Age of Creation saw the birth of the world and the awakening of its first inhabitants.",
                 eg, "The Era of Darkness plunged Mythos into chaos, with monsters and dark forces threatening its existence.",
                 eg, "The Age of Heroes brought forth legendary figures who shaped the world's destiny."
               ],
            "imagine": (detailed one-paragraph prompt for a landscape view of the world. no names)
             }}
       """