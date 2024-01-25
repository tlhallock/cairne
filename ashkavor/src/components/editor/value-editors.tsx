import * as openrpg from '../../openrpg/schema/schema';

export interface ValueEditorProps {
    field: openrpg.GeneratedField;
    depth: number;
    setJsValue: (value: string) => void;
    jsValue: string;
}

export const ChoicesEditor = ({ setJsValue, jsValue, field }: ValueEditorProps) => {
    let value = null;
    try {
        value = JSON.parse(jsValue);
    } catch (e) {
        value = 'none';
    }
    return (
        <select
            value={value}
            onChange={(event) => {
                if (setJsValue) {
                    setJsValue(JSON.stringify(event.target.value));
                }
            }}
        >
            {field.choices?.map(({ label, value }: openrpg.GeneratedFieldChoice) => (
                <option key={value} value={value}>
                    {label}
                </option>
            ))}
            <option value="none">None</option>
        </select>
    );
};

export const StringFieldEditor = ({ setJsValue, jsValue }: ValueEditorProps) => {
    let value = null;
    try {
        value = JSON.parse(jsValue);
    } catch (e) {
        value = '';
    }
    return (
        <input
            value={value}
            onChange={(event) => {
                if (setJsValue) {
                    setJsValue(JSON.stringify(event.target.value));
                }
            }}
        />
    );
};

export const TextFieldEditor = ({ field }: ValueEditorProps) => {
    return <input type="text" />;
};

export const BooleanValueEditor = ({ field }: ValueEditorProps) => {
    return <input type="checkbox" />;
};

export const IntegerValueEditor = ({ field }: ValueEditorProps) => {
    return <input type="number" />;
};

export const FloatValueEditor = ({ setJsValue, jsValue, field }: ValueEditorProps) => {
    let value = null;
    try {
        value = JSON.parse(jsValue);
    } catch (e) {
        value = 0.0;
    }
    return (
        <input
            type="number"
            value={value}
            onChange={(event) => {
                if (setJsValue) {
                    setJsValue(JSON.stringify(event.target.value));
                }
            }}
        />
    );
};
