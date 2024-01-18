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

export const ListAdder = (props: FieldProps) => {
    switch (props.field.add_value_type) {
        case 'string':
            return <StringAdder path={props.field.edit_path} onEdit={props.onEdit} />;
        case 'boolean':
            return <BooleanAdder path={props.field.edit_path} onEdit={props.onEdit} />;
        case 'float':
            return <FloatAdder path={props.field.edit_path} onEdit={props.onEdit} />;
        case 'integer':
            return <IntegerAdder path={props.field.edit_path} onEdit={props.onEdit} />;
    }
    return (
        <div>
            <label>Unknown Add Type: {props.field.add_value_type}</label>
            <div />
        </div>
    );
};

// export const ListValueEditor = (props: FieldProps) => {
//     return (
//         <>
//             <label>{props.field.label}</label>
//             <div />
//             <ListAdder path=h} add_type={} onEdit={props.onEdit} />
//             <div />
//             {props.field.children?.map((value, index) => (
//                 // Maybe this should be a field list item?
//                 // <button>Remove</button>
//                 <Field key={index} {...props} field={value} depth={props.depth + 1} />
//             ))}
//         </>
//     );
// };
