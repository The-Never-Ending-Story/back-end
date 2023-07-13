def gpt_prompt(params):
    return f"""
       Describe a world in vivid detail with the following features:

       {params}

       Include a description of the world's landscape, its inhabitants, one of its cities, and a significant character.
       Based on these, describe an overview of the world's historical lore in three epochs.
       Your response should follow this structure:
           {{
            "name": (a creative name based on its features),
            "blurb": (a brief one-liner about the world),
            "description": (a one paragraph description),
            "city": {{
                "name": (name),
                "description": (description)
               }}
            "species": {{
                "name": (name of species),
                "alignment": (DnD alignment),
                "politics": (one sentence about their politics)
               }}
            "character": {{
               "name": (name),
               "description": (description)
               }}
            "history": [
                 eg, "The Age of Creation saw the birth of the world and the awakening of its first inhabitants.",
                 eg, "The Era of Darkness plunged Mythos into chaos, with monsters and dark forces threatening its existence.",
                 eg, "The Age of Heroes brought forth legendary figures who shaped the world's destiny."
               ]
             }}
       """