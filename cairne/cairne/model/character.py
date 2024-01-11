from enum import Enum
from typing import Any, Dict, List, Optional, Union

import cairne.model.generated as gen
from pydantic import BaseModel, Field


class Archetype(str, Enum):
	LOVER = "lover"
	HERO = "hero"
	MAGICIAN = "magician"
	EXPLORER = "explorer"
	SAGE = "sage"
	INNOCENT = "innocent"
	CREATOR = "creator"
	RULER = "ruler"
	CAREGIVER = "caregiver"
	EVERYMAN = "everyman"
	JESTER = "jester"
	REBEL = "rebel"

	def describe(self) -> str:
		if self == Archetype.INNOCENT:
			return "Exhibits happiness, goodness, optimism, safety, romance, and youth"
		elif self == Archetype.EVERYMAN:
			return "Seeks connections and belonging; is recognized as supportive, faithful and down-to-earth, reliable"
		elif self == Archetype.HERO:
			return "On a mission to make the world a better place, the Hero is courageous, bold, inspirational"
		elif self == Archetype.REBEL:
			return "Questions authority and breaks the rules; the Rebel craves rebellion and revolution"
		elif self == Archetype.EXPLORER:
			return "Finds inspiration in travel, risk, discovery, and the thrill of new experiences"
		elif self == Archetype.CREATOR:
			return "Imaginative, inventive and driven to build things of enduring meaning and value"
		elif self == Archetype.RULER:
			return "Creates order from the chaos, the Ruler is typically controlling and stern, yet responsible and organized"
		elif self == Archetype.MAGICIAN:
			return "Wishes to create something special and make dreams a reality, the Magician is seen as visionary and spiritual"
		elif self == Archetype.LOVER:
			return "Creates intimate moments, inspires love, passion, romance, sensuality, and commitment"
		elif self == Archetype.CAREGIVER:
			return "Protects and cares for others, is compassionate, nurturing and generous"
		elif self == Archetype.JESTER:
			return "Brings joy to the world through humor, fun, irreverence and often likes to make some mischief"
		elif self == Archetype.SAGE:
			return "Committed to helping the world gain deeper insight and wisdom, the Sage serves as the thoughtful mentor or advisor"
		else:
			raise Exception(f"Unknown archetype {self}")


# class NameParser(gen.Generatable):
#     # first_name: Optional[str] = Field(None, description="The character's first name")
#     # last_name: Optional[str] = Field(None, description="The character's last name")
#     # nickname: Optional[str] = Field(None, description="The character's nickname")

#     def parse(self, context: gen.ParseContext) -> None:
#         print("TODO: parse name")


# class AgeParser(gen.Generatable):
#     def parse(self, context: gen.ParseContext) -> None:
#         if self.raw_input is None:
#             context.add_error(
#                 gen.ValidationError(
#                     path=context.create_path(),
#                     message=f"age is a required field"
#                 )
#             )
#             return
#         if isinstance(self.raw_input, float):
#             self.parsed = self.raw_input
#         elif isinstance(self.raw_input, int):
#             self.parsed = float(self.raw_input)
#         else:
#             try:
#                 self.parsed = float(self.raw_input)
#             except ValueError:
#                 context.add_error(
#                     gen.ValidationError(
#                         path=context.create_path(),
#                         message=f"age must be a number"
#                     )
#                 )


# class Specifications:


# Need to create examples for openai
# Need to list the examples that are already generated (like the names should be unique)
# should there be regenerate options: if the appearance is updated, should the image_prompt be updated?
# should this really just be a yaml file?
# Shouhld have a generation schema for jsonformer
# GENERATABLE = gen.GeneratableComposite(
#     fields=[

#     ]
# )
