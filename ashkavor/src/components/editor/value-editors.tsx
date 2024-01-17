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

import { FIELD_STYLES } from './base';

export interface FieldProps {
    field: openrpg.GeneratedField;
    onEdit: () => void;
}

export const StringFieldEditor = ({ field, onEdit }: FieldProps) => {
    return (
        <div style={FIELD_STYLES}>
            <label>{field.label}</label>
            <label>{field.value_js}</label>
            <div>
                <input />
                <button>Replace</button>
            </div>
        </div>
    );
};

export const TextFieldEditor = ({ field, onEdit }: FieldProps) => {
    return (
        <div style={FIELD_STYLES}>
            <label>{field.label}</label>
            <label>{field.value_js}</label>
            <div>
                <input type="text" />
                <button>Replace</button>
            </div>
        </div>
    );
};

export const BooleanValueEditor = ({ field, onEdit }: FieldProps) => {
    return (
        <div style={FIELD_STYLES}>
            <label>{field.label}</label>
            <label>{field.value_js}</label>
            <div>
                <input type="checkbox" />
                <button>Set</button>
            </div>
        </div>
    );
};

export const IntegerValueEditor = ({ field, onEdit }: FieldProps) => {
    return (
        <div style={FIELD_STYLES}>
            <label>{field.label}</label>
            <label>{field.value_js}</label>
            <div>
                <input type="number" />
                <button>Set</button>
            </div>
        </div>
    );
};

export const FloatValueEditor = ({ field, onEdit }: FieldProps) => {
    return (
        <div style={FIELD_STYLES}>
            <label>{field.label}</label>
            <label>{field.value_js}</label>
            <div>
                <input type="number" />
                <button>Set</button>
            </div>
        </div>
    );
};
