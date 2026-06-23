import { createElement } from "react";
const React = { createElement };

import { PageFragment } from "mendix/PageFragment";
import { ActionProperty } from "mendix/ActionProperty";
import { AttributeProperty } from "mendix/AttributeProperty";
import { DerivedUniqueIdProperty } from "mendix/DerivedUniqueIdProperty";
import { ExpressionProperty } from "mendix/ExpressionProperty";
import { NanoflowObjectProperty } from "mendix/NanoflowObjectProperty";
import { TextProperty } from "mendix/TextProperty";
import { ValidationProperty } from "mendix/ValidationProperty";
import { WebIconProperty } from "mendix/WebIconProperty";

import { ActionButton } from "mendix/widgets/web/ActionButton";
import { ConditionalVisibilityWrapper } from "mendix/widgets/web/ConditionalVisibilityWrapper";
import { Container } from "mendix/widgets/web/Container";
import { DataView } from "mendix/widgets/web/DataView";
import { Div } from "mendix/widgets/web/Div";
import { FormGroup } from "mendix/widgets/web/FormGroup";
import * as ImageWidgetModule from "C:/Users/Korisnik/Mendix/FoodDelivery2-main/deployment/web/widgets/com/mendix/widget/web/image/Image.mjs";
const Image = Object.getOwnPropertyDescriptor(ImageWidgetModule, "Image")?.value || Object.getOwnPropertyDescriptor(ImageWidgetModule, "default")?.value;   
import "C:/Users/Korisnik/Mendix/FoodDelivery2-main/deployment/web/widgets/com/mendix/widget/web/image/Image.css";
import { Label } from "mendix/widgets/web/Label";
import { Text } from "mendix/widgets/web/Text";
import { TextArea } from "mendix/widgets/web/TextArea";
import { TextBox } from "mendix/widgets/web/TextBox";
import { addEnumerations, asPluginWidgets, t } from "mendix";

import { content as parentContent } from "../layouts/Atlas_Core.PopupLayout.js";
import { DS_Feedback_Populate } from "../nanoflows/FeedbackModule.DS_Feedback_Populate.js";
import { ACT_Feedback_TriggerScreenshotMode } from "../nanoflows/FeedbackModule.ACT_Feedback_TriggerScreenshotMode.js";
import { ACT_Feedback_UploadImage } from "../nanoflows/FeedbackModule.ACT_Feedback_UploadImage.js";
import { ACT_Feedback_ClearImage } from "../nanoflows/FeedbackModule.ACT_Feedback_ClearImage.js";
import { ACT_Feedback_ClearForm } from "../nanoflows/FeedbackModule.ACT_Feedback_ClearForm.js";
import { ACT_SubmitFeedback } from "../nanoflows/FeedbackModule.ACT_SubmitFeedback.js";
import { OCH_Feedback_SaveToLocalStorage } from "../nanoflows/FeedbackModule.OCH_Feedback_SaveToLocalStorage.js";

const { $Div, $DataView, $Container, $Text, $FormGroup, $TextBox, $TextArea, $Label, $ConditionalVisibilityWrapper, $ActionButton, $Image } = asPluginWidgets({ Div, DataView, Container, Text, FormGroup, TextBox, TextArea, Label, ConditionalVisibilityWrapper, ActionButton, Image });

const region$Main = (historyId) => (<PageFragment renderKey={historyId}>{[
    <$Div key="p.FeedbackModule.ShareFeedback.layoutGrid1"
        $widgetId="p.FeedbackModule.ShareFeedback.layoutGrid1"
        class={"mx-name-layoutGrid1 mx-layoutgrid mx-layoutgrid-fluid container-fluid"}
        content={[
            <$Div key="p.FeedbackModule.ShareFeedback.layoutGrid1$row0"
                $widgetId="p.FeedbackModule.ShareFeedback.layoutGrid1$row0"
                class={"row"}
                content={[
                    <$Div key="p.FeedbackModule.ShareFeedback.layoutGrid1$row0$column0"
                        $widgetId="p.FeedbackModule.ShareFeedback.layoutGrid1$row0$column0"
                        class={"col-lg col-md col"}
                        content={[
                            <$DataView key="p.FeedbackModule.ShareFeedback.dataView5"
                                $widgetId="p.FeedbackModule.ShareFeedback.dataView5"
                                class={"mx-name-dataView5 form-vertical"}
                                object={NanoflowObjectProperty({
                                    "dataSourceId": "p.20",
                                    "editable": true,
                                    "source": { "nanoflow": () => DS_Feedback_Populate, "allowedRoles": [ "User" ] },
                                    "argMap": {}
                                })}
                                emptyMessage={TextProperty({
                                    "value": ""
                                })}
                                body={[
                                    <$Container key="p.FeedbackModule.ShareFeedback.container5"
                                        $widgetId="p.FeedbackModule.ShareFeedback.container5"
                                        class={"mx-name-container5 spacing-outer-bottom-medium"}
                                        renderMode={"div"}
                                        content={[
                                            <$Text key="p.FeedbackModule.ShareFeedback.text1"
                                                $widgetId="p.FeedbackModule.ShareFeedback.text1"
                                                class={"mx-name-text1"}
                                                caption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Help us make your experience better and share your feedback with us!" }, "args": {} }
                                                })}
                                                renderMode={"p"} />,
                                            <$FormGroup key="p.FeedbackModule.ShareFeedback.feedback_subject$formGroup"
                                                $widgetId="p.FeedbackModule.ShareFeedback.feedback_subject$formGroup"
                                                class={"mx-name-feedback_subject mx-textbox"}
                                                control={[
                                                    <$TextBox key="p.FeedbackModule.ShareFeedback.feedback_subject"
                                                        $widgetId="p.FeedbackModule.ShareFeedback.feedback_subject"
                                                        inputValue={AttributeProperty({
                                                            "scope": "p.FeedbackModule.ShareFeedback.dataView5",
                                                            "path": "",
                                                            "entity": "FeedbackModule.Feedback",
                                                            "attribute": "Subject",
                                                            "onChange": { "type": "callNanoflow", "argMap": { "Feedback": { "widget": "p.FeedbackModule.ShareFeedback.dataView5", "source": "object" } }, "config": { "nanoflow": () => OCH_Feedback_SaveToLocalStorage, "allowedRoles": [ "User" ] }, "disabledDuringExecution": false },
                                                            "isList": false,
                                                            "validation": null,
                                                            "formatting": { }
                                                        })}
                                                        isPassword={false}
                                                        placeholder={ExpressionProperty({
                                                            "expression": { "expr": { "type": "literal", "value": "Summarize your feedback in a few words" }, "args": {} }
                                                        })}
                                                        mask={""}
                                                        readOnlyStyle={"control"}
                                                        maxLength={200}
                                                        autocomplete={"on"}
                                                        submitWhileEditing={true}
                                                        submitDelay={300}
                                                        id={DerivedUniqueIdProperty({
                                                            "widgetId": "p.FeedbackModule.ShareFeedback.feedback_subject"
                                                        })} />
                                                ]}
                                                caption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Subject" }, "args": {} }
                                                })}
                                                labelFor={DerivedUniqueIdProperty({
                                                    "widgetId": "p.FeedbackModule.ShareFeedback.feedback_subject"
                                                })}
                                                orientation={"vertical"}
                                                hasError={ValidationProperty({
                                                    "inputWidgetId": "p.FeedbackModule.ShareFeedback.feedback_subject"
                                                })} />,
                                            <$FormGroup key="p.FeedbackModule.ShareFeedback.textArea2$formGroup"
                                                $widgetId="p.FeedbackModule.ShareFeedback.textArea2$formGroup"
                                                class={"mx-name-textArea2 mx-textarea"}
                                                control={[
                                                    <$TextArea key="p.FeedbackModule.ShareFeedback.textArea2"
                                                        $widgetId="p.FeedbackModule.ShareFeedback.textArea2"
                                                        inputValue={AttributeProperty({
                                                            "scope": "p.FeedbackModule.ShareFeedback.dataView5",
                                                            "path": "",
                                                            "entity": "FeedbackModule.Feedback",
                                                            "attribute": "Description",
                                                            "onChange": { "type": "callNanoflow", "argMap": { "Feedback": { "widget": "p.FeedbackModule.ShareFeedback.dataView5", "source": "object" } }, "config": { "nanoflow": () => OCH_Feedback_SaveToLocalStorage, "allowedRoles": [ "User" ] }, "disabledDuringExecution": false },
                                                            "isList": false,
                                                            "validation": null
                                                        })}
                                                        numberOfLines={5}
                                                        autoGrow={false}
                                                        placeholder={ExpressionProperty({
                                                            "expression": { "expr": { "type": "literal", "value": "Please add a detailed description, including steps you took before finding issue, or how this idea would help improve the experience for you and other users" }, "args": {} }
                                                        })}
                                                        readOnlyStyle={"control"}
                                                        submitWhileEditing={true}
                                                        submitDelay={300}
                                                        id={DerivedUniqueIdProperty({
                                                            "widgetId": "p.FeedbackModule.ShareFeedback.textArea2"
                                                        })} />
                                                ]}
                                                caption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Description" }, "args": {} }
                                                })}
                                                labelFor={DerivedUniqueIdProperty({
                                                    "widgetId": "p.FeedbackModule.ShareFeedback.textArea2"
                                                })}
                                                orientation={"vertical"}
                                                hasError={ValidationProperty({
                                                    "inputWidgetId": "p.FeedbackModule.ShareFeedback.textArea2"
                                                })} />
                                        ]}
                                        ariaHidden={false} />,
                                    <$Container key="p.FeedbackModule.ShareFeedback.container4"
                                        $widgetId="p.FeedbackModule.ShareFeedback.container4"
                                        class={"mx-name-container4 col-left spacing-outer-bottom"}
                                        renderMode={"div"}
                                        content={[
                                            <$Label key="p.FeedbackModule.ShareFeedback.label1"
                                                $widgetId="p.FeedbackModule.ShareFeedback.label1"
                                                class={"mx-name-label1 text-semibold spacing-outer-bottom-none"}
                                                id={DerivedUniqueIdProperty({
                                                    "widgetId": "p.FeedbackModule.ShareFeedback.label1"
                                                })}
                                                caption={TextProperty({
                                                    "value": "Attachment"
                                                })} />,
                                            <$Text key="p.FeedbackModule.ShareFeedback.text2"
                                                $widgetId="p.FeedbackModule.ShareFeedback.text2"
                                                class={"mx-name-text2 text-light"}
                                                caption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Upload a jpg, jpeg, png or gif image file of max. 5MB." }, "args": {} }
                                                })}
                                                renderMode={"span"} />
                                        ]}
                                        ariaHidden={false} />,
                                    <$Container key="p.FeedbackModule.ShareFeedback.container2"
                                        $widgetId="p.FeedbackModule.ShareFeedback.container2"
                                        class={"mx-name-container2 flexcontainer justify-content-start spacing-outer-bottom-medium"}
                                        style={{
                                            "gap": "8px"
                                        }}
                                        renderMode={"div"}
                                        content={[
                                            <$ConditionalVisibilityWrapper key="p.FeedbackModule.ShareFeedback.actionButton4$visibility"
                                                $widgetId="p.FeedbackModule.ShareFeedback.actionButton4$visibility"
                                                visible={ExpressionProperty({
                                                    "expression": { "expr": { "type": "function", "name": "_hasSomeRole", "parameters": [ { "type": "literal", "value": "User" } ] }, "args": {} }
                                                })}
                                                contents={[
                                                    <$ActionButton key="p.FeedbackModule.ShareFeedback.actionButton4"
                                                        $widgetId="p.FeedbackModule.ShareFeedback.actionButton4"
                                                        buttonId={"p.FeedbackModule.ShareFeedback.actionButton4"}
                                                        class={"mx-name-actionButton4"}
                                                        renderType={"button"}
                                                        buttonClass={"btn-default"}
                                                        caption={ExpressionProperty({
                                                            "expression": { "expr": { "type": "literal", "value": "Take Screenshot" }, "args": {} }
                                                        })}
                                                        tooltip={TextProperty({
                                                            "value": ""
                                                        })}
                                                        icon={WebIconProperty({
                                                            "icon": { "type": "glyph", "iconClass": "glyphicon-camera" }
                                                        })}
                                                        action={ActionProperty({
                                                            "action": { "type": "callNanoflow", "argMap": { "Feedback": { "widget": "p.FeedbackModule.ShareFeedback.dataView5", "source": "object" } }, "config": { "nanoflow": () => ACT_Feedback_TriggerScreenshotMode, "allowedRoles": [ "User" ] }, "disabledDuringExecution": true },
                                                            "abortOnServerValidation": true
                                                        })} />
                                                ]} />,
                                            <$ConditionalVisibilityWrapper key="p.FeedbackModule.ShareFeedback.actionButton5$visibility"
                                                $widgetId="p.FeedbackModule.ShareFeedback.actionButton5$visibility"
                                                visible={ExpressionProperty({
                                                    "expression": { "expr": { "type": "function", "name": "_hasSomeRole", "parameters": [ { "type": "literal", "value": "User" } ] }, "args": {} }
                                                })}
                                                contents={[
                                                    <$ActionButton key="p.FeedbackModule.ShareFeedback.actionButton5"
                                                        $widgetId="p.FeedbackModule.ShareFeedback.actionButton5"
                                                        buttonId={"p.FeedbackModule.ShareFeedback.actionButton5"}
                                                        class={"mx-name-actionButton5"}
                                                        renderType={"button"}
                                                        buttonClass={"btn-default"}
                                                        caption={ExpressionProperty({
                                                            "expression": { "expr": { "type": "literal", "value": "Upload" }, "args": {} }
                                                        })}
                                                        tooltip={TextProperty({
                                                            "value": ""
                                                        })}
                                                        icon={WebIconProperty({
                                                            "icon": { "type": "glyph", "iconClass": "glyphicon-open" }
                                                        })}
                                                        action={ActionProperty({
                                                            "action": { "type": "callNanoflow", "argMap": { "Feedback": { "widget": "p.FeedbackModule.ShareFeedback.dataView5", "source": "object" } }, "config": { "nanoflow": () => ACT_Feedback_UploadImage, "allowedRoles": [ "User" ] }, "disabledDuringExecution": true },
                                                            "abortOnServerValidation": true
                                                        })} />
                                                ]} />
                                        ]}
                                        ariaHidden={false} />,
                                    <$ConditionalVisibilityWrapper key="p.FeedbackModule.ShareFeedback.container6$visibility"
                                        $widgetId="p.FeedbackModule.ShareFeedback.container6$visibility"
                                        visible={ExpressionProperty({
                                            "expression": { "expr": { "type": "function", "name": "!=", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "ImageB64" }, { "type": "literal", "value": null } ] }, "args": { "currentObject": { "widget": "p.FeedbackModule.ShareFeedback.dataView5", "source": "object" } } }
                                        })}
                                        contents={[
                                            <$Container key="p.FeedbackModule.ShareFeedback.container6"
                                                $widgetId="p.FeedbackModule.ShareFeedback.container6"
                                                class={"mx-name-container6 mxfeedback-screenshot-preview spacing-outer-bottom-medium"}
                                                renderMode={"div"}
                                                content={[
                                                    <$Container key="p.FeedbackModule.ShareFeedback.container7"
                                                        $widgetId="p.FeedbackModule.ShareFeedback.container7"
                                                        class={"mx-name-container7"}
                                                        style={{
                                                            "position": "relative"
                                                        }}
                                                        renderMode={"div"}
                                                        content={[
                                                            <$ConditionalVisibilityWrapper key="p.FeedbackModule.ShareFeedback.actionButton1$visibility"
                                                                $widgetId="p.FeedbackModule.ShareFeedback.actionButton1$visibility"
                                                                visible={ExpressionProperty({
                                                                    "expression": { "expr": { "type": "function", "name": "_hasSomeRole", "parameters": [ { "type": "literal", "value": "User" } ] }, "args": {} }
                                                                })}
                                                                contents={[
                                                                    <$ActionButton key="p.FeedbackModule.ShareFeedback.actionButton1"
                                                                        $widgetId="p.FeedbackModule.ShareFeedback.actionButton1"
                                                                        buttonId={"p.FeedbackModule.ShareFeedback.actionButton1"}
                                                                        class={"mx-name-actionButton1 mxfeedback-screenshot-preview__delete-button"}
                                                                        renderType={"button"}
                                                                        buttonClass={"btn-default"}
                                                                        caption={ExpressionProperty({
                                                                            "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                                        })}
                                                                        tooltip={TextProperty({
                                                                            "value": ""
                                                                        })}
                                                                        icon={WebIconProperty({
                                                                            "icon": { "type": "glyph", "iconClass": "glyphicon-remove" }
                                                                        })}
                                                                        action={ActionProperty({
                                                                            "action": { "type": "callNanoflow", "argMap": { "Feedback": { "widget": "p.FeedbackModule.ShareFeedback.dataView5", "source": "object" } }, "config": { "nanoflow": () => ACT_Feedback_ClearImage, "allowedRoles": [ "User" ] }, "disabledDuringExecution": true },
                                                                            "abortOnServerValidation": true
                                                                        })} />
                                                                ]} />,
                                                            <$Image key="p.FeedbackModule.ShareFeedback.image1"
                                                                $widgetId="p.FeedbackModule.ShareFeedback.image1"
                                                                datasource={"imageUrl"}
                                                                imageUrl={ExpressionProperty({
                                                                    "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "ImageB64" }, "args": { "currentObject": { "widget": "p.FeedbackModule.ShareFeedback.dataView5", "source": "object" } } }
                                                                })}
                                                                isBackgroundImage={false}
                                                                onClickType={"action"}
                                                                alternativeText={ExpressionProperty({
                                                                    "expression": { "expr": { "type": "literal", "value": "A Preview of the Feedback image that was from the screenshot or upload" }, "args": {} }
                                                                })}
                                                                widthUnit={"auto"}
                                                                width={100}
                                                                heightUnit={"auto"}
                                                                height={100}
                                                                iconSize={14}
                                                                displayAs={"fullImage"}
                                                                responsive={true}
                                                                class={"mx-name-image1 mxfeedback-screenshot-preview__image img-center img-contain"}
                                                                style={{
                                                                    "width": "auto"
                                                                }} />
                                                        ]}
                                                        ariaHidden={false} />
                                                ]}
                                                ariaHidden={false} />
                                        ]} />,
                                    <$ConditionalVisibilityWrapper key="p.FeedbackModule.ShareFeedback.textBox1$formGroup$visibility"
                                        $widgetId="p.FeedbackModule.ShareFeedback.textBox1$formGroup$visibility"
                                        visible={ExpressionProperty({
                                            "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "_showEmail" }, "args": { "currentObject": { "widget": "p.FeedbackModule.ShareFeedback.dataView5", "source": "object" } } }
                                        })}
                                        contents={[
                                            <$FormGroup key="p.FeedbackModule.ShareFeedback.textBox1$formGroup"
                                                $widgetId="p.FeedbackModule.ShareFeedback.textBox1$formGroup"
                                                class={"mx-name-textBox1 mx-textbox"}
                                                control={[
                                                    <$TextBox key="p.FeedbackModule.ShareFeedback.textBox1"
                                                        $widgetId="p.FeedbackModule.ShareFeedback.textBox1"
                                                        inputValue={AttributeProperty({
                                                            "scope": "p.FeedbackModule.ShareFeedback.dataView5",
                                                            "path": "",
                                                            "entity": "FeedbackModule.Feedback",
                                                            "attribute": "SubmitterEmail",
                                                            "onChange": { "type": "callNanoflow", "argMap": { "Feedback": { "widget": "p.FeedbackModule.ShareFeedback.dataView5", "source": "object" } }, "config": { "nanoflow": () => OCH_Feedback_SaveToLocalStorage, "allowedRoles": [ "User" ] }, "disabledDuringExecution": false },
                                                            "isList": false,
                                                            "validation": null,
                                                            "formatting": { }
                                                        })}
                                                        isPassword={false}
                                                        placeholder={ExpressionProperty({
                                                            "expression": { "expr": { "type": "literal", "value": "name@company.com" }, "args": {} }
                                                        })}
                                                        mask={""}
                                                        readOnlyStyle={"control"}
                                                        maxLength={200}
                                                        autocomplete={"on"}
                                                        submitWhileEditing={true}
                                                        submitDelay={300}
                                                        id={DerivedUniqueIdProperty({
                                                            "widgetId": "p.FeedbackModule.ShareFeedback.textBox1"
                                                        })} />
                                                ]}
                                                caption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Email" }, "args": {} }
                                                })}
                                                labelFor={DerivedUniqueIdProperty({
                                                    "widgetId": "p.FeedbackModule.ShareFeedback.textBox1"
                                                })}
                                                orientation={"vertical"}
                                                hasError={ValidationProperty({
                                                    "inputWidgetId": "p.FeedbackModule.ShareFeedback.textBox1"
                                                })} />
                                        ]} />,
                                    <$Container key="p.FeedbackModule.ShareFeedback.container3"
                                        $widgetId="p.FeedbackModule.ShareFeedback.container3"
                                        class={"mx-name-container3 flex-row flexcontainer justify-content-end"}
                                        style={{
                                            "gap": "8px"
                                        }}
                                        renderMode={"div"}
                                        content={[
                                            <$ActionButton key="p.FeedbackModule.ShareFeedback.feedback_cancel"
                                                $widgetId="p.FeedbackModule.ShareFeedback.feedback_cancel"
                                                buttonId={"p.FeedbackModule.ShareFeedback.feedback_cancel"}
                                                class={"mx-name-feedback_cancel"}
                                                style={{
                                                    "border": "0"
                                                }}
                                                renderType={"button"}
                                                buttonClass={"btn-default"}
                                                caption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Cancel" }, "args": {} }
                                                })}
                                                tooltip={TextProperty({
                                                    "value": ""
                                                })}
                                                action={ActionProperty({
                                                    "action": { "type": "closePage", "argMap": {}, "config": {}, "disabledDuringExecution": true },
                                                    "abortOnServerValidation": true
                                                })} />,
                                            <$ConditionalVisibilityWrapper key="p.FeedbackModule.ShareFeedback.feedback_clear$visibility"
                                                $widgetId="p.FeedbackModule.ShareFeedback.feedback_clear$visibility"
                                                visible={ExpressionProperty({
                                                    "expression": { "expr": { "type": "function", "name": "_hasSomeRole", "parameters": [ { "type": "literal", "value": "User" } ] }, "args": {} }
                                                })}
                                                contents={[
                                                    <$ActionButton key="p.FeedbackModule.ShareFeedback.feedback_clear"
                                                        $widgetId="p.FeedbackModule.ShareFeedback.feedback_clear"
                                                        buttonId={"p.FeedbackModule.ShareFeedback.feedback_clear"}
                                                        class={"mx-name-feedback_clear btn-bordered"}
                                                        renderType={"button"}
                                                        buttonClass={"btn-default"}
                                                        caption={ExpressionProperty({
                                                            "expression": { "expr": { "type": "literal", "value": "Clear" }, "args": {} }
                                                        })}
                                                        tooltip={TextProperty({
                                                            "value": ""
                                                        })}
                                                        action={ActionProperty({
                                                            "action": { "type": "callNanoflow", "argMap": { "Feedback": { "widget": "p.FeedbackModule.ShareFeedback.dataView5", "source": "object" } }, "config": { "nanoflow": () => ACT_Feedback_ClearForm, "allowedRoles": [ "User" ] }, "disabledDuringExecution": true },
                                                            "abortOnServerValidation": true
                                                        })} />
                                                ]} />,
                                            <$ConditionalVisibilityWrapper key="p.FeedbackModule.ShareFeedback.feedback_submit$visibility"
                                                $widgetId="p.FeedbackModule.ShareFeedback.feedback_submit$visibility"
                                                visible={ExpressionProperty({
                                                    "expression": { "expr": { "type": "function", "name": "_hasSomeRole", "parameters": [ { "type": "literal", "value": "User" } ] }, "args": {} }
                                                })}
                                                contents={[
                                                    <$ActionButton key="p.FeedbackModule.ShareFeedback.feedback_submit"
                                                        $widgetId="p.FeedbackModule.ShareFeedback.feedback_submit"
                                                        buttonId={"p.FeedbackModule.ShareFeedback.feedback_submit"}
                                                        class={"mx-name-feedback_submit"}
                                                        renderType={"button"}
                                                        buttonClass={"btn-primary"}
                                                        caption={ExpressionProperty({
                                                            "expression": { "expr": { "type": "literal", "value": "Submit" }, "args": {} }
                                                        })}
                                                        tooltip={TextProperty({
                                                            "value": ""
                                                        })}
                                                        action={ActionProperty({
                                                            "action": { "type": "callNanoflow", "argMap": { "Feedback": { "widget": "p.FeedbackModule.ShareFeedback.dataView5", "source": "object" } }, "config": { "nanoflow": () => ACT_SubmitFeedback, "allowedRoles": [ "User" ] }, "disabledDuringExecution": true },
                                                            "abortOnServerValidation": true
                                                        })} />
                                                ]} />
                                        ]}
                                        ariaHidden={false} />
                                ]}
                                hideFooter={true} />
                        ]} />
                ]} />
        ]} />
]}</PageFragment>);

export const title = t([
    "Share your feedback"
]);

export const classes = "";

export const cancelChangesOperationId = "Ee1/lBQN6V+qdxbBxKG/oQ";
export const style = {};
export const content = { ...parentContent,
    "Atlas_Core.PopupLayout.Main": region$Main,
};
