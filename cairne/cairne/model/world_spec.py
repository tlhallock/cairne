import cairne.model.character as character_model
import cairne.model.specification as spec

# spawn location


def trim(s: str) -> str:
    return '"' + s.replace("\n", " ").replace("\t", "") + '"'


WORLD = spec.EntitySpecification(
    entity_type=spec.EntityType.WORLD,
    children={
        "name": spec.ValueSpecification(
            parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
            editor=spec.EditorSpecification(editor_name=spec.EditorName.SHORT_STRING),
            validators=[
                spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)
            ],
        ),
        "theme": spec.ValueSpecification(
            parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
            editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
            validators=[
                spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)
            ],
        ),
        "concept": spec.ValueSpecification(
            parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
            editor=spec.EditorSpecification(editor_name=spec.EditorName.LONG_STRING),
            validators=[
                spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)
            ],
        ),
        "game_speed": spec.ValueSpecification(
            parser=spec.ParserSpecification(parser_name=spec.ParserName.FLOAT),
            editor=spec.EditorSpecification(editor_name=spec.EditorName.FLOAT_INPUT),
            validators=[
                spec.ValidatorSpecification(validator_name=spec.ValidatorName.REQUIRED)
            ],
            # Default value of 1.0?
        ),
        "factions": spec.ListSpecification(
            element_specification=spec.ValueSpecification(
                parser=spec.ParserSpecification(parser_name=spec.ParserName.STRING),
                validators=[],
                editor=spec.EditorSpecification(
                    editor_name=spec.EditorName.SHORT_STRING
                ),
                generation=spec.GenerationSpecification(num_examples=3),
            ),
        ),
        spec.EntityType.REGION.get_field_name(): spec.EntityDictionarySpecification(
            entity_specification=spec.EntitySpecification(
                entity_type=spec.EntityType.REGION,
                children={
                    "name": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.SHORT_STRING
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                    "description": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.LONG_STRING
                        ),
                        generation=spec.GenerationSpecification(
                            # example_json_values=[trim("""
                            # 	A small town on the coast of California, inhabited since 2700 BC.
                            #  	The Ohlone people lived here for thousands of years before the Spanish arrived in 1769.
                            #   	The Spanish named the town after the nearby Mission Dolores, which was founded in 1776.
                            #    	The town was incorporated in 1856 and has been growing ever since.
                            # 	Today, it is home to over 100,000 people and is one of the most popular tourist destinations in the state.
                            # 	"""),
                            # ],
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                    "image_prompt": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.LONG_STRING
                        ),
                        generation=spec.GenerationSpecification(
                            # example_json_values=[
                            # 	'"beach, ocean, cliffs, sand, waves, surfers, sun, fog, seagulls, pelicans, seals, sea lions, fog"',
                            # ],
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                },
            )
        ),
        spec.EntityType.ITEM.get_field_name(): spec.EntityDictionarySpecification(
            entity_specification=spec.EntitySpecification(
                entity_type=spec.EntityType.ITEM,
                children={
                    "name": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.SHORT_STRING
                        ),
                        generation=spec.GenerationSpecification(
                            # example_json_values=['"stick"', '"feather"', '"rock"', '"potion"'],
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                    "description": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.LONG_STRING
                        ),
                        generation=spec.GenerationSpecification(
                            # example_json_values=['"used for building a fire or arrow"'],
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                    "image_prompt": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.LONG_STRING
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                },
            )
        ),
        spec.EntityType.RESOURCE_TYPE.get_field_name(): spec.EntityDictionarySpecification(
            entity_specification=spec.EntitySpecification(
                entity_type=spec.EntityType.RESOURCE_TYPE,
                children={
                    "name": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.SHORT_STRING
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                    "description": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.LONG_STRING
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                    "image_prompt": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.LONG_STRING
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                    "weight": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.FLOAT
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.FLOAT_INPUT
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                },
            )
        ),
        spec.EntityType.CRAFTING_RECIPE.get_field_name(): spec.EntityDictionarySpecification(
            entity_specification=spec.EntitySpecification(
                entity_type=spec.EntityType.CRAFTING_RECIPE,
                children={
                    "name": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.SHORT_STRING
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                    "description": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.LONG_STRING
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                    "image_prompt": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.LONG_STRING
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                },
            )
        ),
        spec.EntityType.CHARACTER.get_field_name(): spec.EntityDictionarySpecification(
            entity_specification=spec.EntitySpecification(
                generation=spec.GenerationSpecification(
                    instructions=[
                        spec.PredefinedInstruction(name="setting", template="Create characters for a game with setting: '{theme}'."),
                        spec.PredefinedInstruction(name="unique", template="Character names should be unique and memorable."),
                        spec.PredefinedInstruction(name="no-well-known", template="Character names should not be well-known historical figures."),
                        spec.PredefinedInstruction(name="match-setting", template="Character names should be appropriate for the setting."),
                        spec.PredefinedInstruction(name="faction-options", template="Possible factions: [{possible_factions}]."),
                        spec.PredefinedInstruction(name="gender-options", template="Possible genders: [{possible_genders}]."),
                        spec.PredefinedInstruction(name="archetype-options", template="Possible archetypes: [{possible_archetypes}]."),
                        spec.PredefinedInstruction(name="existing-characters", template="The existing characters are: {existing_characters}."),
                    ],
                ),
                entity_type=spec.EntityType.CHARACTER,
                children={
                    "name": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.SHORT_STRING
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                    "faction": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.ENUMERATED
                        ),
                        validators=[
                            spec.OneOfGeneratedValidator(
                                path=spec.GeneratablePath(
                                    path_elements=[
                                        spec.GeneratablePathElement(key="factions"),
                                    ]
                                )
                            ),
                        ],
                    ),
                    "age": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.FLOAT
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.FLOAT_INPUT
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                    "archetype": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.ENUMERATED
                        ),
                        validators=[
                            spec.OneOfLiteralValidator(
                                options=[
                                    (archetype, [archetype.value, archetype.name])
                                    for archetype in character_model.Archetype
                                ],
                            )
                        ],
                    ),
                    "gender": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.ENUMERATED
                        ),
                        validators=[
                            spec.OneOfLiteralValidator(
                                options=[
                                    (gender, [gender.value, gender.name])
                                    for gender in character_model.Gender
                                ],
                            )
                        ],
                    ),
                    "marital_status": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.ENUMERATED
                        ),
                        validators=[
                            spec.OneOfLiteralValidator(
                                options=[
                                    (
                                        marital_status,
                                        [marital_status.value, marital_status.name],
                                    )
                                    for marital_status in character_model.MaritalStatus
                                ],
                            )
                        ],
                    ),
                    "description": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.LONG_STRING
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                    "appearance": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.LONG_STRING
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                    "history": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.LONG_STRING
                        ),
                    ),
                    "origin": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.LONG_STRING
                        ),
                    ),
                    # should update with the appearance...
                    "image_prompt": spec.ValueSpecification(
                        parser=spec.ParserSpecification(
                            parser_name=spec.ParserName.STRING
                        ),
                        editor=spec.EditorSpecification(
                            editor_name=spec.EditorName.LONG_STRING
                        ),
                        validators=[
                            spec.ValidatorSpecification(
                                validator_name=spec.ValidatorName.REQUIRED
                            )
                        ],
                    ),
                    "strengths": spec.ListSpecification(
                        generation=spec.GenerationSpecification(num_examples=2),
                        element_specification=spec.ValueSpecification(
                            parser=spec.ParserSpecification(
                                parser_name=spec.ParserName.STRING
                            ),
                            editor=spec.EditorSpecification(
                                editor_name=spec.EditorName.SHORT_STRING
                            ),
                            validators=[
                                spec.ValidatorSpecification(
                                    validator_name=spec.ValidatorName.REQUIRED
                                )
                            ],
                        ),
                    ),
                    "weaknesses": spec.ListSpecification(
                        generation=spec.GenerationSpecification(num_examples=2),
                        element_specification=spec.ValueSpecification(
                            parser=spec.ParserSpecification(
                                parser_name=spec.ParserName.STRING
                            ),
                            editor=spec.EditorSpecification(
                                editor_name=spec.EditorName.SHORT_STRING
                            ),
                            validators=[
                                spec.ValidatorSpecification(
                                    validator_name=spec.ValidatorName.REQUIRED
                                )
                            ],
                        ),
                    ),
                    "fears": spec.ListSpecification(
                        generation=spec.GenerationSpecification(num_examples=2),
                        element_specification=spec.ValueSpecification(
                            parser=spec.ParserSpecification(
                                parser_name=spec.ParserName.STRING
                            ),
                            editor=spec.EditorSpecification(
                                editor_name=spec.EditorName.SHORT_STRING
                            ),
                            validators=[
                                spec.ValidatorSpecification(
                                    validator_name=spec.ValidatorName.REQUIRED
                                )
                            ],
                        ),
                    ),
                    "secrets": spec.ListSpecification(
                        generation=spec.GenerationSpecification(num_examples=2),
                        element_specification=spec.ValueSpecification(
                            parser=spec.ParserSpecification(
                                parser_name=spec.ParserName.STRING
                            ),
                            editor=spec.EditorSpecification(
                                editor_name=spec.EditorName.SHORT_STRING
                            ),
                            validators=[
                                spec.ValidatorSpecification(
                                    validator_name=spec.ValidatorName.REQUIRED
                                )
                            ],
                        ),
                    ),
                    "goals": spec.ListSpecification(
                        generation=spec.GenerationSpecification(num_examples=2),
                        element_specification=spec.ValueSpecification(
                            parser=spec.ParserSpecification(
                                parser_name=spec.ParserName.STRING
                            ),
                            editor=spec.EditorSpecification(
                                editor_name=spec.EditorName.SHORT_STRING
                            ),
                            validators=[
                                spec.ValidatorSpecification(
                                    validator_name=spec.ValidatorName.REQUIRED
                                )
                            ],
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
