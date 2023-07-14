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
            "earthly": Boolean,
            "geoDynamics": {{
                "size": (scope),
                "climate": (natural conditions)
            }}
            "magicTechnology": {{
                "magic": (Boolean),
                "technology": (Integer),
                "genres": [(eg fantasy, sci-fi, _-punk, vaporwave)]  
            }}
            "name": (a creative name based on its features. may be inspired by genre but not directly use genre names),
            "blurb": (a brief one-liner about the world),
            "description": (a one paragraph description),
            "species": [{{
                "name": (name of species),
                "description": (description),
                "politics": (one sentence about their politics),
                "imagine": (an image prompt: highly detailed, visually and stylistically descriptive, 
                one paragraph long. each such prompt should be a standalone natural language 
                description that doesn't refer to the names of the subjects)")
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
            "history": [(three strings, each a paragraph long, describing the evolution of the world in ages/epochs/etc, incorporating the above information)],
            "imagine": (highly detailed, visually and stylistically descriptive, one-paragraph prompt for a landscape view of the world. do not refer to the world or its features by name.)
             }}
       """