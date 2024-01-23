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

import { FIELD_STYLES, HEADER_STYLES } from './base';
import { FieldProps } from './base';
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

interface UpdaterProps {
    path: openrpg.GeneratablePath;
    jsValue: string;
    clearJsValue: () => void;
    validEdits: boolean;
}

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
    };
    return (
        <>
            <label>
                {props.depth > 0 && <Spacer depth={props.depth} />}
                {props.field.label}
            </label>
            <label>{JSON.parse(props.field.value_js)}</label>
            {
                props.field.choices?.length || 0 > 0 ? (
                    <ChoicesEditor {...props} jsValue={jsValue} setJsValue={setJsValue} />
                ) : (
                    {
                        string: (
                            <StringFieldEditor
                                {...props}
                                jsValue={jsValue}
                                setJsValue={setJsValue}
                            />
                        ),
                        text: (
                            <TextFieldEditor {...props} jsValue={jsValue} setJsValue={setJsValue} />
                        ),
                        boolean: (
                            <BooleanValueEditor
                                {...props}
                                jsValue={jsValue}
                                setJsValue={setJsValue}
                            />
                        ),
                        float: (
                            <FloatValueEditor
                                {...props}
                                jsValue={jsValue}
                                setJsValue={setJsValue}
                            />
                        ),
                        integer: (
                            <IntegerValueEditor
                                {...props}
                                jsValue={jsValue}
                                setJsValue={setJsValue}
                            />
                        ),
                        list: <div />,
                        object: <div />,
                        entities_dictionary: (
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
                        ),
                    }[props.field.value_type]
                )
                //  || <span>{"Unknown value type: " + props.field.value_type}}</span>
            }
            {{
                string: <UpdateButton {...updateProps} />,
                text: <UpdateButton {...updateProps} />,
                boolean: <UpdateButton {...updateProps} />,
                float: <UpdateButton {...updateProps} />,
                integer: <UpdateButton {...updateProps} />,
                // List adder should be split up so the add button is with the update button, and the editor is aligns with the others
                list: <ListAdder {...props} />,
                object: <div />,
                entities_dictionary: <div />,
            }[props.field.value_type] || (
                <label>Unknown value type: {props.field.value_type}</label>
            )}

            <Validations validationErrors={props.field.validation_errors} />
            <StructuredGenerationField generatedField={props.field} />

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
