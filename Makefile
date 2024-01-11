

# pydantic2ts --module cairne.cairne.schema --output ashkavor/src/openrpg/schema/


schema:
	PYTHONPATH="cairne" python cairne/cairne/schema/base.py
	PATH="${PATH}:ashkavor/node_modules/.bin/" json2ts \
		-i ashkavor/src/openrpg/schema/schema.json \
		-o ashkavor/src/openrpg/schema/schema.tsx \
		--enableConstEnums --unreachableDefinitions
