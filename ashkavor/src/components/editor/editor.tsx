import classNames from 'classnames';
import styles from './entity-editor.module.scss';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import { replaceValue } from '../../openrpg/client';
import { StructuredGenerationSettings } from '../structured-generation-settings/structured-generation-settings';

import * as generation from '../../openrpg/generation';
import { StructuredGenerationField } from '../structured-generation-field/structured-generation-field';
import { GenerateStatus } from '../generate-status/generate-status';
import { ValueEditorProps } from './value-editors';

import { FIELD_STYLES, HEADER_STYLES } from './base';
import { FieldProps, UpdaterProps } from './base';
import {
    StringFieldEditor,
    BooleanValueEditor,
    FloatValueEditor,
    IntegerValueEditor,
    TextFieldEditor,
    ChoicesEditor,
} from './value-editors';

import { ListAdder } from './list-editor';

// const getGeneratedField = (
//     generationState: generation.GenerationState,
//     field: openrpg.GeneratedField
//     // TODO: Add the generation result field...
// ): generation.StructuredGenerationField => {
//     const existing = generationState.generationFields[field.edit_path_key];
//     if (existing) {
//         return existing;
//     }
//     return {
//         unique_path_key: field.edit_path_key,
//         path: field.edit_path,
//         generate: false,
//         generated: null,
//     };
// };

interface ValidationsProps {
    validationErrors?: openrpg.ValidationErrors;
}

const Validations = ({ validationErrors }: ValidationsProps) => {
    return (
        <ol>
            {validationErrors?.map((error, index) => (
                <li key={index + error} style={{ background: 'red' }}>
                    {error}
                    <input type="checkbox" />
                </li>
            ))}
        </ol>
    );
};

interface SpacerProps {
    depth: number;
}

const Spacer = ({ depth }: SpacerProps) => {
    return <span style={{ marginLeft: 50 * depth }} />;
};

const UpdateButton = ({ path, onEdit, jsValue, clearJsValue, validEdits }: UpdaterProps) => {
    const location = useLocation();
    const worldId = location.pathname.split('/')[2];
    return (
        <div>
            <button
                onClick={() => {
                    replaceValue(worldId, path, jsValue, (response: openrpg.ReplaceResponse) => {
                        clearJsValue();
                        onEdit();
                    });
                }}
                disabled={!validEdits}
            >
                Update
            </button>
            <button>Delete</button>
        </div>
    );
};

const FieldEditorSelection = (props: ValueEditorProps) => {
    const location = useLocation();
    const worldId = location.pathname.split('/')[2];

    if (props.field.choices?.length || 0 > 0) {
        return <ChoicesEditor {...props} jsValue={props.jsValue} setJsValue={props.setJsValue} />;
    }
    switch (props.field.value_type) {
        case 'string':
            return <StringFieldEditor {...props} />;
        case 'text':
            return <TextFieldEditor {...props} />;
        case 'boolean':
            return <BooleanValueEditor {...props} />;
        case 'float':
            return <FloatValueEditor {...props} />;
        case 'integer':
            return <IntegerValueEditor {...props} />;
        case 'list':
            return <div />;
        case 'object':
            return <div />;
        case 'entities_dictionary':
            return (
                <Link
                    to={
                        '/world/' +
                        worldId +
                        '/entities/' +
                        props.field.entity_dictionary_type?.name
                    }
                >
                    Edit {props.field.entity_dictionary_type?.label}
                </Link>
            );
        default:
            return <label>Unknown editor</label>;
    }
};

export interface UpdaterSelectionProps {
    updateProps: UpdaterProps;
    value_type: openrpg.GeneratedValueEditor;
}

const UpdaterSelection = ({ value_type, updateProps }: UpdaterSelectionProps) => {
    switch (value_type) {
        case 'string':
            return <UpdateButton {...updateProps} />;
        case 'text':
            return <UpdateButton {...updateProps} />;
        case 'boolean':
            return <UpdateButton {...updateProps} />;
        case 'float':
            return <UpdateButton {...updateProps} />;
        case 'integer':
            return <UpdateButton {...updateProps} />;
        // List adder should be split up so the add button is with the update button, and the editor is aligns with the others
        case 'list':
            return <ListAdder {...updateProps} />;
        case 'object':
            return <div />;
        case 'entities_dictionary':
            return <div />;
        default:
            return <label>Unknown value type: {value_type}</label>;
    }
};

const Field = (props: FieldProps) => {
    const [jsValue, setJsValue] = React.useState<string>('');
    const location = useLocation();
    const worldId = location.pathname.split('/')[2];

    // Could have summaries for containers...
    // have generate multiple...
    let validEdits = jsValue !== props.field.value_js;
    try {
        JSON.parse(jsValue);
    } catch (e) {
        validEdits = false;
    }
    const updateProps: UpdaterProps = {
        path: props.field.edit_path,
        jsValue: jsValue,
        clearJsValue: () => setJsValue(''),
        validEdits,
        add_value_type: props.field.add_value_type,
    };
    return (
        <>
            <label>
                {props.depth > 0 && <Spacer depth={props.depth} />}
                {props.field.label}
            </label>
            <label>{JSON.parse(props.field.value_js)}</label>
            <FieldEditorSelection {...props} jsValue={jsValue} setJsValue={setJsValue} />
            <UpdaterSelection updateProps={updateProps} value_type={props.field.value_type} />
            <Validations validationErrors={props.field.validation_errors} />
            <StructuredGenerationField generatedField={props.field} setJsValue={setJsValue} />

            {props.field.children?.map((value, index) => (
                // Maybe this should be a field list item?
                // <button>Remove</button>
                <Field key={index} {...props} field={value} depth={props.depth + 1} />
            ))}
        </>
    );
};

export interface FieldsProps {
    fields: openrpg.GeneratedField[];
}

export const FieldsEditor = ({ fields }: FieldsProps) => {
    return (
        <div style={FIELD_STYLES}>
            <label>Field</label>
            <label>Current value</label>
            <label>Updates</label>
            <div />
            <div />
            <div />
            {fields?.map((field) => (
                <Field key={field.label} field={field} depth={0} />
            ))}
        </div>
    );
};
