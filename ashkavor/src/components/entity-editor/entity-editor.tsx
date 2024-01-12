import classNames from 'classnames';
import styles from './entity-editor.module.scss';
import { useLocation, useNavigate } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import { getEntity, deleteEntity } from '../../openrpg/client';

const COMMON_STYLES = {
    padding: '5px',
    margin: '5px',
    width: '90%',
    display: 'grid',
    gridTemplateColumns: '1fr 1fr 1fr',
};
const FIELD_STYLES = {
    ...COMMON_STYLES,
    // border: '1px solid red',
    // backgroundColor: 'lightgray',
};
const HEADER_STYLES = {
    ...COMMON_STYLES,
    border: '1px solid red',
    // backgroundColor: 'lightblue',
};

export interface FieldProps {
    field: openrpg.GeneratedField;
    onEdit: () => void;
}

const StringFieldEditor = ({ field, onEdit }: FieldProps) => {
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

const BooleanValueEditor = ({ field, onEdit }: FieldProps) => {
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

const IntegerValueEditor = ({ field, onEdit }: FieldProps) => {
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

const FloatValueEditor = ({ field, onEdit }: FieldProps) => {
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

const ListValueEditor = ({ field, onEdit }: FieldProps) => {
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
            <ListAdder path={field.edit_path} add_type={field.add_value_type} onEdit={onEdit} />
        </div>
    );
};

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

const Field = ({ field, onEdit }: FieldProps) => {
    switch (field.value_type) {
        case 'string':
            return <StringFieldEditor field={field} onEdit={onEdit} />;
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

export interface EntityEditorProps {
    className?: string;
}

/**
 * This component was created using Codux's Default new component template.
 * To create custom component templates, see https://help.codux.com/kb/en/article/kb16522
 */
export const EntityEditor = ({ className }: EntityEditorProps) => {
    const location = useLocation();
    const navigate = useNavigate();
    const [entity, setEntity] = React.useState<openrpg.GeneratedEntity>();
    const [refreshCounter, setRefreshCounter] = React.useState<number>(0);

    const worldId = location.pathname.split('/')[2];
    const entityType = location.pathname.split('/')[4];
    const entityId = location.pathname.split('/')[5];

    React.useEffect(() => {
        if (!worldId || !entityId) {
            return;
        }
        getEntity(worldId, entityId, (response: openrpg.GetEntityResponse) => {
            if (!response.entity) {
                return;
            }
            setEntity(response.entity);
            console.log('Generated entity', response.entity);
        });
    }, [refreshCounter]);

    const onEdit = () => {
        setRefreshCounter(refreshCounter + 1);
    };

    const onDelete = (response: openrpg.DeleteEntityResponse) => {
        navigate('/world/' + worldId + '/entities/' + entityType);
    };

    return (
        <div className={classNames(styles.root, className)}>
            <button onClick={() => navigate('/world/' + worldId + '/entities/' + entityType)}>
                Back
            </button>
            <button onClick={() => deleteEntity(worldId, entityId, onDelete)}>Delete</button>
            <br />
            <ul>
                <li>
                    <div style={HEADER_STYLES}>
                        <label>Field</label>
                        <label>Current value</label>
                        <label>Updates</label>
                    </div>
                </li>
                {entity?.fields?.map((field) => (
                    <li key={field.label}>
                        <Field field={field} onEdit={onEdit} />
                    </li>
                ))}
            </ul>
            {entity?.name || entity?.entity_id}
        </div>
    );
};
