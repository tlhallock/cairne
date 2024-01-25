import classNames from 'classnames';
import styles from './entity-editor.module.scss';
import { useLocation, useNavigate } from 'react-router-dom';
import * as openrpg from '../../openrpg/schema/schema';
import React from 'react';
import {
    listTemplates,
    getTemplate,
    createTemplate,
    deleteTemplate,
    updateTemplate,
    listGeneratorTypes,
    structuredGenerate,
} from '../../openrpg/client';
import { StructuredGenerationSettings } from '../structured-generation-settings/structured-generation-settings';
import { useSelector, useDispatch } from 'react-redux';

import * as generation from '../../openrpg/generation';
import { StructuredGenerationField } from '../structured-generation-field/structured-generation-field';
import { GenerateStatus } from '../generate-status/generate-status';

import { HEADER_STYLES } from '../editor/base';
import { FieldsEditor, FieldsProps } from '../editor/editor';
import { RootState } from '../../store';
import {
    editTemplate,
    fetchGeneration,
    fetchTemplate,
    listEntityGenerations,
    listEntityTemplates,
    viewGeneration,
} from '../../openrpg/reducers/templates';

export interface GenerationTemplateProps {
    // templateId: openrpg.TemplateId3 | null;
    // setTemplateId: (templateId: openrpg.TemplateId3 | null) => void;
    // generationId: openrpg.GenerationId | null;
    // setGenerationId: (generationId: openrpg.GenerationId) => void;
    // onDelete: () => void;
    // refreshTemplates: () => void;
}

export const GenerationTemplate = ({}: // onDelete,
GenerationTemplateProps) => {
    const location = useLocation();
    const worldId = location.pathname.split('/')[2];
    const entityType = location.pathname.split('/')[4];
    const entityId = location.pathname.split('/')[5];

    const templatesState = useSelector((state: RootState) => state.templates);
    const templateId = templatesState?.entities[entityId]?.editingTemplateId;
    const generationId = templatesState?.entities[entityId]?.currentGenerationId;
    const template = templatesState?.templatesCache[templateId];
    const dispatch = useDispatch();

    const [generationModels, setGenerationModels] = React.useState<openrpg.GenerateModelChoice[]>(
        []
    );
    const [newPrompt, setNewPrompt] = React.useState<string>('');
    const [editingPrompt, setEditingPrompt] = React.useState<boolean>(false);
    const [showInstructions, setShowInstructions] = React.useState<boolean>(false);
    const promptToDisplay = editingPrompt ? newPrompt : template?.prompt ?? '';

    // React.useEffect(() => {
    //     if (!templateId) {
    //         dispatch(editTemplate(entityId, null));
    //         return;
    //     }
    //     dispatch(fetchTemplate(templateId));
    //         // if (!editingPrompt) {
    //         //     setNewPrompt(response.template.prompt ?? '');
    //         // }
    // }, [templateId]);

    React.useEffect(() => {
        listGeneratorTypes((response: openrpg.ListGenerationModels) => {
            if (!response.models) {
                return;
            }
            setGenerationModels(response.models);
        });
    }, []);

    const deleteTemplateCallback = () => {
        if (!templateId) {
            return;
        }
        deleteTemplate(templateId, (response: openrpg.DeleteTemplateResponse) => {
            dispatch(editTemplate(entityId, null));
            dispatch(listEntityTemplates(worldId, entityId));
        });
    };

    const currentGeneratorModel = generationModels.find(
        (model) => model.value === template?.generator_model.generator_type
    )!;

    const requestGeneratorModel = (generatorModel: string) => {
        if (!templateId) {
            return;
        }

        const updates: openrpg.UpdateTemplateRequest = {
            template_id: templateId,
            new_name: null,
            generator_model: {
                generator_type: null,
                g_model_id: generatorModel,
            },
            include_fields: null,
            exclude_fields: null,
            number_to_generate: null,
            instructions_to_include: null,
            instructions_to_exclude: null,
            prompt: null,
            parameter_updates: null,
        };
        updateTemplate(updates, (response: openrpg.UpdateTemplateResponse) => {
            console.log('Updated template', templateId);
            dispatch(fetchTemplate(templateId));
        });
    };
    const requestGeneratorType = (generatorType: openrpg.GeneratorType) => {
        if (!templateId) {
            return;
        }

        const updates: openrpg.UpdateTemplateRequest = {
            template_id: templateId,
            new_name: null,
            generator_model: {
                generator_type: generatorType,
                g_model_id: null,
            },
            include_fields: null,
            exclude_fields: null,
            number_to_generate: null,
            instructions_to_include: null,
            instructions_to_exclude: null,
            prompt: null,
            parameter_updates: null,
        };
        updateTemplate(updates, (response: openrpg.UpdateTemplateResponse) => {
            console.log('Updated template', templateId);
            dispatch(fetchTemplate(templateId));
        });
    };
    const requestNewPrompt = () => {
        if (!templateId) {
            return;
        }

        const updates: openrpg.UpdateTemplateRequest = {
            template_id: templateId,
            new_name: null,
            generator_model: null,
            include_fields: null,
            exclude_fields: null,
            number_to_generate: null,
            instructions_to_include: null,
            instructions_to_exclude: null,
            prompt: newPrompt,
            parameter_updates: null,
        };
        updateTemplate(updates, (response: openrpg.UpdateTemplateResponse) => {
            console.log('Updated template', templateId);

            setEditingPrompt(false);
            dispatch(fetchTemplate(templateId));
        });
    };

    const generate = () => {
        if (!templateId) {
            return;
        }
        const generateRequest: openrpg.GenerateRequest = {
            template_id: templateId,
            target_entity_id: entityId,
        };

        structuredGenerate(generateRequest, (response: openrpg.GenerateResponse) => {
            dispatch(listEntityGenerations(worldId, entityId));
            dispatch(viewGeneration(entityId, response.generation_id));
        });
    };

    if (!template) {
        return <div>No template selected.</div>;
    }

    return (
        <>
            <button onClick={deleteTemplateCallback}>Delete</button>
            <br />

            <label>Generator Type</label>
            <select
                disabled={!currentGeneratorModel}
                name="generator-type"
                id="generator-type"
                value={template.generator_model.generator_type}
                onChange={({ target: { value } }) => {
                    requestGeneratorType(value as openrpg.GeneratorType);
                }}
            >
                {generationModels.map((generatorType) => (
                    <option key={generatorType.value} value={generatorType.value}>
                        {generatorType.label}
                    </option>
                ))}
            </select>
            <br />
            {currentGeneratorModel && (
                <>
                    <label>Model</label>
                    <select
                        name="generator-model"
                        id="generator-model"
                        value={template.generator_model.g_model_id}
                        onChange={(e) => {
                            requestGeneratorModel(e.target.value);
                        }}
                    >
                        {currentGeneratorModel.models.map((generatorModel) => (
                            <option key={generatorModel} value={generatorModel}>
                                {generatorModel}
                            </option>
                        ))}
                    </select>
                </>
            )}
            <br />
            <label>Predefined Instructions</label>
            {!showInstructions && <button onClick={() => setShowInstructions(true)}>Show</button>}
            {showInstructions && <button onClick={() => setShowInstructions(false)}>Hide</button>}
            <br />
            {showInstructions &&
                (template.instructions || []).map(
                    ({ name, label, preview, valid, included }: openrpg.InstructionView) => {
                        const toggleInstruction = () => {};
                        return (
                            <div key={name}>
                                {/* <span>{label}</span> */}
                                <span>{preview}</span>
                                <input
                                    type="checkbox"
                                    disabled={!valid}
                                    checked={!!included && valid}
                                    onChange={toggleInstruction}
                                />
                            </div>
                        );
                    }
                )}
            <br />
            <label>Custom Instructions</label>
            <br />
            <textarea
                value={promptToDisplay}
                onChange={(e) => {
                    setNewPrompt(e.target.value);
                    setEditingPrompt(e.target.value !== template.prompt);
                }}
            />
            <button onClick={requestNewPrompt} disabled={!editingPrompt}>
                Save
            </button>

            <br />
            {generationId && <GenerateStatus generationId={generationId} />}
            <br />
            <button onClick={generate} disabled={!templateId}>
                Generate!
            </button>
        </>
    );
};
