import cairne.model.specification as spec
from cairne.model.character import Archetype

# spawn location


def trim(s: str) -> str:
	return '"' + s.replace("\n", " ").replace("\t", "") + '"'


WORLD = spec.EntitySpecification(
	entity_type=spec.EntityType.WORLD,
	children={
		"name": spec.ValueSpecification(
			parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
			editor=spec.EditorSpecification(editor_name=spec.EditorName.SHORT_STRING),
			generation=spec.GenerationSpecification(num_examples=3),
			validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
		),
		"factions": spec.ListSpecification(
			element_specification=spec.ValueSpecification(
				parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
				validators=[],
				editor=spec.EditorSpecification(editor_name=spec.EditorName.SHORT_STRING),
				generation=spec.GenerationSpecification(num_examples=3),
			),
		),
		spec.EntityType.REGION.get_field_name(): spec.EntityDictionarySpecification(
			entity_specification=spec.EntitySpecification(
				entity_type=spec.EntityType.REGION,
				children={
					"name": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.SHORT_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
							# example_json_values=["Daly City", "Fort Funston"],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
			 		),
					"description": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
							# example_json_values=[trim("""
							# 	A small town on the coast of California, inhabited since 2700 BC.
							#  	The Ohlone people lived here for thousands of years before the Spanish arrived in 1769.
							#   	The Spanish named the town after the nearby Mission Dolores, which was founded in 1776.
							#    	The town was incorporated in 1856 and has been growing ever since.
							# 	Today, it is home to over 100,000 people and is one of the most popular tourist destinations in the state.
							# 	"""),
				 			# ],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
					),
					"image_prompt": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
							# example_json_values=[
							# 	'"beach, ocean, cliffs, sand, waves, surfers, sun, fog, seagulls, pelicans, seals, sea lions, fog"',
							# ],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
					),
				},
			)
		),
		spec.EntityType.ITEM.get_field_name(): spec.EntityDictionarySpecification(
			entity_specification=spec.EntitySpecification(
				entity_type=spec.EntityType.ITEM,
				children={
					"name": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.SHORT_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
							# example_json_values=['"stick"', '"feather"', '"rock"', '"potion"'],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
			 		),
					"description": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
							# example_json_values=['"used for building a fire or arrow"'],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
			 		),
					"image_prompt": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
					),
				},
			)
		),
		spec.EntityType.RESOURCE_TYPE.get_field_name(): spec.EntityDictionarySpecification(
			entity_specification=spec.EntitySpecification(
				entity_type=spec.EntityType.RESOURCE_TYPE,
				children={
					"name": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.SHORT_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
			 		),
					"description": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
			 		),
					"image_prompt": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
					),
					"weight": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.FLOAT),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.NUMBER_INPUT),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
					)
				},
			)
		),
		spec.EntityType.CRAFTING_RECIPE.get_field_name(): spec.EntityDictionarySpecification(
			entity_specification=spec.EntitySpecification(
				entity_type=spec.EntityType.CRAFTING_RECIPE,
				children={
					"name": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.SHORT_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
			 		),
					"description": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
			 		),
					"image_prompt": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
					),
				},
			)
		),
		spec.EntityType.CHARACTER.get_field_name(): spec.EntityDictionarySpecification(
			entity_specification=spec.EntitySpecification(
				entity_type=spec.EntityType.CHARACTER,
				children={
					"name": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.SHORT_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
			 		),
					"age": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.FLOAT),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.NUMBER_INPUT),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
					),
					"archetype": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.ENUMERATED),
						validators=[
							spec.OneOfLiteralValidator(
								validator_name=spec.ValidatorName.ONE_OF_LITERAL,
								options=[
									(archetype, set([archetype.name, archetype.value]))
									for archetype in Archetype
								],
							)
						],
					),
					"description": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
					),
					"appearance": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
					),
					"history": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
					),
					"origin": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
					),
	 				# should update with the appearance...
					"image_prompt": spec.ValueSpecification(
						parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
						editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
						generation=spec.GenerationSpecification(
							instructions=[],
						),
						validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
					),  
					"strengths": spec.ListSpecification(
						generation=spec.GenerationSpecification(num_examples=2),
						element_specification=spec.ValueSpecification(
							parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
							editor=spec.EditorSpecification(editor_name=spec.EditorName.SHORT_STRING),
							validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
			 			),
		 			),
					"weaknesses": spec.ListSpecification(
						generation=spec.GenerationSpecification(num_examples=2),
						element_specification=spec.ValueSpecification(
							parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
							editor=spec.EditorSpecification(editor_name=spec.EditorName.SHORT_STRING),
							validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
			 			),
		 			),
					"fears": spec.ListSpecification(
						generation=spec.GenerationSpecification(num_examples=2),
						element_specification=spec.ValueSpecification(
							parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
							editor=spec.EditorSpecification(editor_name=spec.EditorName.SHORT_STRING),
							validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
			 			),
		 			),
					"secrets": spec.ListSpecification(
						generation=spec.GenerationSpecification(num_examples=2),
						element_specification=spec.ValueSpecification(
							parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
							editor=spec.EditorSpecification(editor_name=spec.EditorName.SHORT_STRING),
							validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
			 			),
		 			),
					"goals": spec.ListSpecification(
						generation=spec.GenerationSpecification(num_examples=2),
						element_specification=spec.ValueSpecification(
							parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
							editor=spec.EditorSpecification(editor_name=spec.EditorName.SHORT_STRING),
							validators=[spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)],
			 			),
		 			),
					# gender
					# marital status
					# occupuation
				},
			)
		),
	},
)
