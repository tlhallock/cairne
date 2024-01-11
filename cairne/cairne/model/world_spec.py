import cairne.model.specification as spec
from cairne.model.character import Archetype

# spawn location


WORLD = spec.EntitySpecification(
	entity_type=spec.EntityType.WORLD,
	children={
		"name": spec.ValueSpecification.create_string_value(required=True),
		"factions": spec.ListSpecification.create_list_of_strings(),
		spec.EntityType.REGION.get_field_name(): spec.EntityDictionarySpecification(
			entity_specification=spec.EntitySpecification(
				entity_type=spec.EntityType.REGION,
				children={
					"name": spec.ValueSpecification.create_string_value(required=True),
					"description": spec.ValueSpecification.create_string_value(
						required=True
					),
					"image_prompt": spec.ValueSpecification.create_string_value(
						required=True
					),
				},
			)
		),
		spec.EntityType.ITEM.get_field_name(): spec.EntityDictionarySpecification(
			entity_specification=spec.EntitySpecification(
				entity_type=spec.EntityType.ITEM,
				children={
					"name": spec.ValueSpecification.create_string_value(required=True),
					"description": spec.ValueSpecification.create_string_value(
						required=True
					),
					"image_prompt": spec.ValueSpecification.create_string_value(
						required=True
					),
				},
			)
		),
		spec.EntityType.RESOURCE_TYPE.get_field_name(): spec.EntityDictionarySpecification(
			entity_specification=spec.EntitySpecification(
				entity_type=spec.EntityType.RESOURCE_TYPE,
				children={
					"name": spec.ValueSpecification.create_string_value(required=True),
					"description": spec.ValueSpecification.create_string_value(
						required=True
					),
					"image_prompt": spec.ValueSpecification.create_string_value(
						required=True
					),
				},
			)
		),
		spec.EntityType.CRAFTING_OPTION.get_field_name(): spec.EntityDictionarySpecification(
			entity_specification=spec.EntitySpecification(
				entity_type=spec.EntityType.CRAFTING_OPTION,
				children={
					"name": spec.ValueSpecification.create_string_value(required=True),
					"description": spec.ValueSpecification.create_string_value(
						required=True
					),
					"image_prompt": spec.ValueSpecification.create_string_value(
						required=True
					),
				},
			)
		),
		spec.EntityType.CHARACTER.get_field_name(): spec.EntityDictionarySpecification(
			entity_specification=spec.EntitySpecification(
				entity_type=spec.EntityType.CHARACTER,
				children={
					"name": spec.ValueSpecification.create_string_value(required=True),
					"age": spec.ValueSpecification.create_spec(spec.ParserName.FLOAT),
					"archetype": spec.ValueSpecification(
						parser=spec.ParserSpecification(
							parser_name=spec.ParserName.STRING
						),
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
					"description": spec.ValueSpecification.create_string_value(
						required=True
					),
					"appearance": spec.ValueSpecification.create_string_value(
						required=True
					),
					"history": spec.ValueSpecification.create_string_value(
						required=True
					),
					"origin": spec.ValueSpecification.create_string_value(
						required=True
					),
					"image_prompt": spec.ValueSpecification.create_string_value(
						required=True
					),  # should update with the appearance...
					"strengths": spec.ListSpecification.create_list_of_strings(),
					"weaknesses": spec.ListSpecification.create_list_of_strings(),
					"fears": spec.ListSpecification.create_list_of_strings(),
					"secrets": spec.ListSpecification.create_list_of_strings(),
					"goals": spec.ListSpecification.create_list_of_strings(),
					# gender
					# marital status
					# occupuation
				},
			)
		),
	},
)
