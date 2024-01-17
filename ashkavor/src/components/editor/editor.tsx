import classNames from 'classnames';
import styles from './entity-editor.module.scss';
import { useLocation, useNavigate } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import { getEntity, deleteEntity, structuredGenerate } from '../../openrpg/client';
import { StructuredGenerationSettings } from '../structured-generation-settings/structured-generation-settings';

import * as generation from '../../openrpg/generation';
import { StructuredGenerationField } from '../structured-generation-field/structured-generation-field';
import { GenerateStatus } from '../generate-status/generate-status';

import { FIELD_STYLES, SPLITTER_STYLES, HEADER_STYLES } from './base';
import { FieldProps } from './value-editors';
import {
    StringFieldEditor,
    BooleanValueEditor,
    FloatValueEditor,
    IntegerValueEditor,
    TextFieldEditor,
} from './value-editors';

import { ListValueEditor } from './list-editor';

const MapValueEditor = ({ field, onEdit }: FieldProps) => {
    return (
        <div style={FIELD_STYLES}>
            <label>{field.label}</label>
            <ul>
                {field.children?.map((value, index) => (
                    <li key={index}>
                        <Field field={value} onEdit={onEdit} />
                        <button>Remove</button>
                    </li>
                ))}
            </ul>
            <button>Add</button>
        </div>
    );
};

export const Field = ({ field, onEdit }: FieldProps) => {
    switch (field.value_type) {
        case 'string':
            return <StringFieldEditor field={field} onEdit={onEdit} />;
        case 'text':
            return <TextFieldEditor field={field} onEdit={onEdit} />;
        case 'boolean':
            return <BooleanValueEditor field={field} onEdit={onEdit} />;
        case 'float':
            return <FloatValueEditor field={field} onEdit={onEdit} />;
        case 'integer':
            return <IntegerValueEditor field={field} onEdit={onEdit} />;
        case 'list':
            return <ListValueEditor field={field} onEdit={onEdit} />;
        case 'object':
            return <StringFieldEditor field={field} onEdit={onEdit} />;
        case 'entities_dictionary':
            return <MapValueEditor field={field} onEdit={onEdit} />;
    }

    return (
        <div
            style={{
                border: '1px solid red',
                padding: '5px',
                margin: '5px',
                backgroundColor: 'lightgray',
                width: '100%',
            }}
        >
            <label>{field.label}</label>
            <label>Unknown editor</label>
        </div>
    );
};

export interface FieldsProps {
    fields: openrpg.GeneratedField[];
    onEdit: () => void;
    generatorState: generation.GenerationState;
    setGeneratorState: (state: generation.GenerationState) => void;
}

export const FieldsEditor = ({
    fields,
    onEdit,
    generatorState,
    setGeneratorState,
}: FieldsProps) => {
    return (
        <>
            <div style={SPLITTER_STYLES}>
                <div style={HEADER_STYLES}>
                    <label>Field</label>
                    <label>Current value</label>
                    <label>Updates</label>
                </div>
            </div>
            {fields?.map((field) => (
                <li key={field.label} style={SPLITTER_STYLES}>
                    <Field field={field} onEdit={onEdit} />
                    <StructuredGenerationField
                        generatedField={field}
                        generationState={generatorState}
                        setGenerationState={setGeneratorState}
                    />
                </li>
            ))}
        </>
    );
};
