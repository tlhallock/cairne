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

import { FieldProps, UpdaterProps } from './base';

export interface ListAdderProps {
    path: openrpg.GeneratablePath;
}

const StringAdder = ({ path }: ListAdderProps) => {
    const [value, setValue] = React.useState<string>('');
    return (
        <div>
            <input type="text" value={value} onChange={(e) => setValue(e.target.value)} />

            <button>Add</button>
        </div>
    );
};

const BooleanAdder = ({ path }: ListAdderProps) => {
    return (
        <div>
            <button>Add true</button>
            <button>Add false</button>
        </div>
    );
};

const IntegerAdder = ({ path }: ListAdderProps) => {
    const [value, setValue] = React.useState<number>(0);
    return (
        <div>
            <input type="number" value={value} onChange={(e) => setValue(e.target.valueAsNumber)} />
            <button>Add</button>
        </div>
    );
};

const FloatAdder = ({ path }: ListAdderProps) => {
    const [value, setValue] = React.useState<number>(0);
    return (
        <div>
            <input type="number" value={value} onChange={(e) => setValue(e.target.valueAsNumber)} />
            <button>Add</button>
        </div>
    );
};

export const ListAdder = (props: UpdaterProps) => {
    switch (props.add_value_type) {
        case 'string':
            return <StringAdder path={props.path} />;
        case 'boolean':
            return <BooleanAdder path={props.path} />;
        case 'float':
            return <FloatAdder path={props.path} />;
        case 'integer':
            return <IntegerAdder path={props.path} />;
    }
    return (
        <div>
            <label>Unknown Add Type: {props.add_value_type}</label>
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
