// export const SPLITTER_STYLES = {
//     width: '90%',
//     display: 'grid',
//     gridTemplateColumns: '1fr 1fr',
// };
import * as openrpg from '../../openrpg/schema/schema';
import * as generation from '../../openrpg/generation';

const COMMON_STYLES = {
    padding: '5px',
    margin: '5px',
    width: '90%',
    display: 'grid',
    gridTemplateColumns: 'auto auto auto auto auto auto',
};

export const FIELD_STYLES = {
    ...COMMON_STYLES,
    // border: '1px solid red',
    // backgroundColor: 'lightgray',
};
export const HEADER_STYLES = {
    ...COMMON_STYLES,
    border: '1px solid red',
    // backgroundColor: 'lightblue',
};

export interface FieldProps {
    field: openrpg.GeneratedField;
    depth: number;
}
