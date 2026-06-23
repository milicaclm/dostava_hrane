import { createElement } from "react";
const React = { createElement };

import { PageFragment } from "mendix/PageFragment";
import { ActionProperty } from "mendix/ActionProperty";
import { AssociationObjectProperty } from "mendix/AssociationObjectProperty";
import { AttributeProperty } from "mendix/AttributeProperty";
import { DerivedUniqueIdProperty } from "mendix/DerivedUniqueIdProperty";
import { ExpressionProperty } from "mendix/ExpressionProperty";
import { TextProperty } from "mendix/TextProperty";
import { ValidationProperty } from "mendix/ValidationProperty";

import { ActionButton } from "mendix/widgets/web/ActionButton";
import { ConditionalVisibilityWrapper } from "mendix/widgets/web/ConditionalVisibilityWrapper";
import { DataView } from "mendix/widgets/web/DataView";
import { Div } from "mendix/widgets/web/Div";
import { FormGroup } from "mendix/widgets/web/FormGroup";
import { TextBox } from "mendix/widgets/web/TextBox";
import { addEnumerations, asPluginWidgets, t } from "mendix";

import { content as parentContent } from "../layouts/Atlas_Core.PopupLayout.js";

const { $Div, $DataView, $FormGroup, $TextBox, $ConditionalVisibilityWrapper, $ActionButton } = asPluginWidgets({ Div, DataView, FormGroup, TextBox, ConditionalVisibilityWrapper, ActionButton });

const region$Main = (historyId) => (<PageFragment renderKey={historyId}>{[
    <$Div key="p.Administration.ChangePasswordForm.layoutGrid1"
        $widgetId="p.Administration.ChangePasswordForm.layoutGrid1"
        class={"mx-name-layoutGrid1 mx-layoutgrid mx-layoutgrid-fluid container-fluid"}
        content={[
            <$Div key="p.Administration.ChangePasswordForm.layoutGrid1$row0"
                $widgetId="p.Administration.ChangePasswordForm.layoutGrid1$row0"
                class={"row"}
                content={[
                    <$Div key="p.Administration.ChangePasswordForm.layoutGrid1$row0$column0"
                        $widgetId="p.Administration.ChangePasswordForm.layoutGrid1$row0$column0"
                        class={"col-lg col-md col"}
                        content={[
                            <$DataView key="p.Administration.ChangePasswordForm.dataView2"
                                $widgetId="p.Administration.ChangePasswordForm.dataView2"
                                class={"mx-name-dataView2 form-horizontal"}
                                object={AssociationObjectProperty({
                                    "dataSourceId": "p.12",
                                    "scope": "$AccountPasswordData",
                                    "editable": true
                                })}
                                emptyMessage={TextProperty({
                                    "value": ""
                                })}
                                body={[
                                    <$FormGroup key="p.Administration.ChangePasswordForm.textBox3$formGroup"
                                        $widgetId="p.Administration.ChangePasswordForm.textBox3$formGroup"
                                        class={"mx-name-textBox3 mx-textbox"}
                                        control={[
                                            <$TextBox key="p.Administration.ChangePasswordForm.textBox3"
                                                $widgetId="p.Administration.ChangePasswordForm.textBox3"
                                                inputValue={AttributeProperty({
                                                    "scope": "p.Administration.ChangePasswordForm.dataView2",
                                                    "path": "",
                                                    "entity": "Administration.AccountPasswordData",
                                                    "attribute": "NewPassword",
                                                    "onChange": { "type": "doNothing", "argMap": {}, "config": {}, "disabledDuringExecution": false },
                                                    "isList": false,
                                                    "validation": { "message": t([ "The password cannot be empty." ]), "expression": { "expr": { "type": "function", "name": "!=", "parameters": [ { "type": "variable", "variable": "value" }, { "type": "literal", "value": null } ] }, "args": {} } },
                                                    "formatting": { }
                                                })}
                                                isPassword={true}
                                                placeholder={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                mask={""}
                                                readOnlyStyle={"text"}
                                                maxLength={200}
                                                autocomplete={"on"}
                                                submitWhileEditing={false}
                                                submitDelay={300}
                                                ariaRequired={true}
                                                id={DerivedUniqueIdProperty({
                                                    "widgetId": "p.Administration.ChangePasswordForm.textBox3"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "New password" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.Administration.ChangePasswordForm.textBox3"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.Administration.ChangePasswordForm.textBox3"
                                        })} />,
                                    <$FormGroup key="p.Administration.ChangePasswordForm.textBox1$formGroup"
                                        $widgetId="p.Administration.ChangePasswordForm.textBox1$formGroup"
                                        class={"mx-name-textBox1 mx-textbox"}
                                        control={[
                                            <$TextBox key="p.Administration.ChangePasswordForm.textBox1"
                                                $widgetId="p.Administration.ChangePasswordForm.textBox1"
                                                inputValue={AttributeProperty({
                                                    "scope": "p.Administration.ChangePasswordForm.dataView2",
                                                    "path": "",
                                                    "entity": "Administration.AccountPasswordData",
                                                    "attribute": "ConfirmPassword",
                                                    "onChange": { "type": "doNothing", "argMap": {}, "config": {}, "disabledDuringExecution": false },
                                                    "isList": false,
                                                    "validation": { "message": t([ "The password cannot be empty." ]), "expression": { "expr": { "type": "function", "name": "!=", "parameters": [ { "type": "variable", "variable": "value" }, { "type": "literal", "value": null } ] }, "args": {} } },
                                                    "formatting": { }
                                                })}
                                                isPassword={true}
                                                placeholder={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                mask={""}
                                                readOnlyStyle={"text"}
                                                maxLength={200}
                                                autocomplete={"on"}
                                                submitWhileEditing={false}
                                                submitDelay={300}
                                                ariaRequired={true}
                                                id={DerivedUniqueIdProperty({
                                                    "widgetId": "p.Administration.ChangePasswordForm.textBox1"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Confirm password" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.Administration.ChangePasswordForm.textBox1"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.Administration.ChangePasswordForm.textBox1"
                                        })} />
                                ]}
                                hideFooter={false}
                                footer={[
                                    <$ConditionalVisibilityWrapper key="p.Administration.ChangePasswordForm.microflowButton1$visibility"
                                        $widgetId="p.Administration.ChangePasswordForm.microflowButton1$visibility"
                                        visible={ExpressionProperty({
                                            "expression": { "expr": { "type": "function", "name": "_hasSomeRole", "parameters": [ { "type": "literal", "value": "Administrator" } ] }, "args": {} }
                                        })}
                                        contents={[
                                            <$ActionButton key="p.Administration.ChangePasswordForm.microflowButton1"
                                                $widgetId="p.Administration.ChangePasswordForm.microflowButton1"
                                                buttonId={"p.Administration.ChangePasswordForm.microflowButton1"}
                                                class={"mx-name-microflowButton1"}
                                                renderType={"button"}
                                                buttonClass={"btn-success"}
                                                caption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Change" }, "args": {} }
                                                })}
                                                tooltip={TextProperty({
                                                    "value": ""
                                                })}
                                                action={ActionProperty({
                                                    "action": { "type": "callMicroflow", "argMap": { "AccountPasswordData": { "widget": "$AccountPasswordData", "source": "object" } }, "config": { "operationId": "hcne495YMlub+dLnC0sQ3A", "validate": "view", "allowedRoles": [ "Administrator" ] }, "disabledDuringExecution": false },
                                                    "abortOnServerValidation": true
                                                })} />
                                        ]} />,
                                    <$ActionButton key="p.Administration.ChangePasswordForm.cancelButton1"
                                        $widgetId="p.Administration.ChangePasswordForm.cancelButton1"
                                        buttonId={"p.Administration.ChangePasswordForm.cancelButton1"}
                                        class={"mx-name-cancelButton1"}
                                        renderType={"button"}
                                        buttonClass={"btn-default"}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Cancel" }, "args": {} }
                                        })}
                                        tooltip={TextProperty({
                                            "value": ""
                                        })}
                                        action={ActionProperty({
                                            "action": { "type": "cancelChanges", "argMap": {}, "config": { "operationId": "JSFEmbJBXFuNQCdO8zJQMA", "closePage": true }, "disabledDuringExecution": true },
                                            "abortOnServerValidation": true
                                        })} />
                                ]} />
                        ]} />
                ]} />
        ]} />
]}</PageFragment>);

export const title = t([
    "Change Password"
]);

export const classes = "";

export const cancelChangesOperationId = "sTtyemiCd12jUz9MdIB+KA";
export const closeButton = "p.Administration.ChangePasswordForm.cancelButton1";
export const style = {};
export const content = { ...parentContent,
    "Atlas_Core.PopupLayout.Main": region$Main,
};
