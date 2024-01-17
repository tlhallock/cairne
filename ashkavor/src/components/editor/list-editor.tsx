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
import { FieldProps } from './value-editors';
import { Field } from './editor';

export interface ListAdderProps {
    path: openrpg.GeneratablePath;
    onEdit: () => void;
}

const StringAdder = ({ path, onEdit }: ListAdderProps) => {
    const [value, setValue] = React.useState<string>('');
    return (
        <div>
            <input type="text" value={value} onChange={(e) => setValue(e.target.value)} />
            <button>Add</button>
        </div>
    );
};

const BooleanAdder = ({ path, onEdit }: ListAdderProps) => {
    return (
        <div>
            <button>Add true</button>
            <button>Add false</button>
        </div>
    );
};

const IntegerAdder = ({ path, onEdit }: ListAdderProps) => {
    const [value, setValue] = React.useState<number>(0);
    return (
        <div>
            <input type="number" value={value} onChange={(e) => setValue(e.target.valueAsNumber)} />
            <button>Add</button>
        </div>
    );
};

const FloatAdder = ({ path, onEdit }: ListAdderProps) => {
    const [value, setValue] = React.useState<number>(0);
    return (
        <div>
            <input type="number" value={value} onChange={(e) => setValue(e.target.valueAsNumber)} />
            <button>Add</button>
        </div>
    );
};

export interface AnyListAdderProps {
    path: openrpg.GeneratablePath;
    add_type: openrpg.GeneratedValueEditor;
    onEdit: () => void;
}

const ListAdder = ({ path, add_type, onEdit }: AnyListAdderProps) => {
    switch (add_type) {
        case 'string':
            return <StringAdder path={path} onEdit={onEdit} />;
        case 'boolean':
            return <BooleanAdder path={path} onEdit={onEdit} />;
        case 'float':
            return <FloatAdder path={path} onEdit={onEdit} />;
        case 'integer':
            return <IntegerAdder path={path} onEdit={onEdit} />;
    }
    return (
        <div>
            <label>Unknown Add Type: {add_type}</label>
        </div>
    );
};

export const ListValueEditor = ({ field, onEdit }: FieldProps) => {
    return (
        <>
            <div style={FIELD_STYLES}>
                <label>{field.label}</label>
                <div />
                <ListAdder path={field.edit_path} add_type={field.add_value_type} onEdit={onEdit} />
            </div>
            {field.children?.map((value, index) => (
                <div style={FIELD_STYLES}>
                    <Field field={value} onEdit={onEdit} />

                    {/* <div>
                        <button>Remove</button>
                    </div> */}
                </div>
            ))}
            <div />
        </>
    );
};
