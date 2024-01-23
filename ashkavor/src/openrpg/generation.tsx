//

import * as openrpg from './schema/schema';
import React from 'react';

export interface GeneratorTypeChoice {
    label: string;
    value: openrpg.GeneratorType;
    defaultModel: string;
    models: string[];
}

// export const DEFAULT_GENERATOR_TYPES: GeneratorTypeChoice[] = [
//     {
//         label: 'Open AI',
//         value: 'openai',
//         defaultModel: 'gpt-3.5-turbo-1106',
//         models: [
//             'gpt-4-1106-preview',
//             'gpt-4-vision-preview',
//             'gpt-4',
//             'gpt-4-0314',
//             'gpt-4-0613',
//             'gpt-4-32k',
//             'gpt-4-32k-0314',
//             'gpt-4-32k-0613',
//             'gpt-3.5-turbo',
//             'gpt-3.5-turbo-16k',
//             'gpt-3.5-turbo-0301',
//             'gpt-3.5-turbo-0613',
//             'gpt-3.5-turbo-1106',
//             'gpt-3.5-turbo-16k-0613',
//         ],
//     },
//     {
//         label: 'Hugging Face',
//         value: 'hugging_face',
//         defaultModel: 'foobar',
//         models: ['foobar'],
//     },
//     { label: 'Ollama', value: 'ollama', defaultModel: 'raboof', models: ['raboof'] },
// ];

export interface StructuredGenerationField {
    unique_path_key: string;
    path: openrpg.GeneratablePath;
    generate: boolean;
    generated?: openrpg.GeneratedField;
}

export interface StructuredGenerationFields {
    [unique_path_key: string]: StructuredGenerationField;
}

export interface GenerationState {
    structured: boolean;
    generatorTypeChoice: GeneratorTypeChoice;
    generationModel: string;
}

// export const DEFAULT_GENERATION_STATE: GenerationState = {
//     structured: false,
//     generatorTypeChoice: DEFAULT_GENERATOR_TYPES[0],
//     generationModel: DEFAULT_GENERATOR_TYPES[0].defaultModel,
// };

export const setStructured = (state: GenerationState, structured: boolean): GenerationState => ({
    ...state,
    structured,
});

// export const setGenerationType = (
//     state: GenerationState,
//     generationType: openrpg.GeneratorType
// ): GenerationState => {
//     for (const generatorType of DEFAULT_GENERATOR_TYPES) {
//         if (generatorType.value === generationType) {
//             return {
//                 ...state,
//                 generatorTypeChoice: generatorType,
//                 generationModel: generatorType.defaultModel,
//             };
//         }
//     }
//     throw `Unknown generator type ${generationType}`;
// };

export const setGenerationModel = (
    state: GenerationState,
    generationModel: string
): GenerationState => ({
    ...state,
    generationModel,
});

// const updateField = (
//     state: GenerationState,
//     field: StructuredGenerationField
// ): GenerationState => ({
//     ...state,
//     generationFields: { ...state.generationFields, [field.unique_path_key]: field },
// });

// const removeField = (state: GenerationState, unique_path_key: string): GenerationState => ({
//     ...state,
//     fieldsToGenerate: state.fieldsToGenerate.filter((f) => f !== field),
// });

// export const isFieldGenerated = (
//     state: GenerationState,
//     field: StructuredGenerationField
// ): boolean => {
//     return state.generationFields[field.unique_path_key]?.generate || false;
// };

// export const toggleGenerateField = (
//     state: GenerationState,
//     field: StructuredGenerationField
// ): GenerationState => {
//     const newField = {
//         ...field,
//         generate: !isFieldGenerated(state, field),
//     };
//     return updateField(state, newField);
// };
