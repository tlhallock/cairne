import cairne.model.specification as spec
import cairne.model.generated as generated_model
from cairne.model.world_spec import WORLD





# class Examples:
#     @staticmethod
#     def get_example_character() -> generated_model.GeneratedEntity:
#         character_json = {
#             "name": "Selena Grey",
#             "gender": "female",
#             "backstory": "Selena is a mysterious bounty hunter with a troubled past, driven by vengeance against alien invaders.",
#             "personality": ["guarded, resilient, and fiercely determined"],
#             "goals": "to seek retribution for her family's tragic fate at the hands of the alien threat",
#             "weaknesses": ["struggles with trust after betrayal", "vulnerable to emotional triggers from her past"],
#             "strengths": ["master tracker",	"proficient in stealth tactics"],
#             "appearance":"athletic build, with striking green eyes and fiery red hair tied back in a braid",
#             "age": 29,
#             "occupation":"bounty hunter",
#             "marital_status":"widow",
#             "faction": "cowboys"
#         }
#     EXAMPLE_CHARACTER = generated_model.GeneratedEntity(
#         entity_type: spec.EntityType = Field()
#     )