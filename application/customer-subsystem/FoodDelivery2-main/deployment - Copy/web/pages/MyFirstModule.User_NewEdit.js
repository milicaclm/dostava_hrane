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
import { DataView } from "mendix/widgets/web/DataView";
import { Div } from "mendix/widgets/web/Div";
import { FormGroup } from "mendix/widgets/web/FormGroup";
import { TextBox } from "mendix/widgets/web/TextBox";
import { addEnumerations, asPluginWidgets, t } from "mendix";

import { content as parentContent } from "../layouts/Atlas_Core.PopupLayout.js";

const { $Div, $DataView, $FormGroup, $TextBox, $ActionButton } = asPluginWidgets({ Div, DataView, FormGroup, TextBox, ActionButton });

const region$Main = (historyId) => (<PageFragment renderKey={historyId}>{[
    <$Div key="p.MyFirstModule.User_NewEdit.layoutGrid1"
        $widgetId="p.MyFirstModule.User_NewEdit.layoutGrid1"
        class={"mx-name-layoutGrid1 mx-layoutgrid mx-layoutgrid-fluid container-fluid"}
        content={[
            <$Div key="p.MyFirstModule.User_NewEdit.layoutGrid1$row0"
                $widgetId="p.MyFirstModule.User_NewEdit.layoutGrid1$row0"
                class={"row"}
                content={[
                    <$Div key="p.MyFirstModule.User_NewEdit.layoutGrid1$row0$column0"
                        $widgetId="p.MyFirstModule.User_NewEdit.layoutGrid1$row0$column0"
                        class={"col-lg col-md col"}
                        content={[
                            <$DataView key="p.MyFirstModule.User_NewEdit.dataView1"
                                $widgetId="p.MyFirstModule.User_NewEdit.dataView1"
                                class={"mx-name-dataView1 form-horizontal"}
                                object={AssociationObjectProperty({
                                    "dataSourceId": "p.12",
                                    "scope": "$User",
                                    "editable": true
                                })}
                                emptyMessage={TextProperty({
                                    "value": ""
                                })}
                                body={[
                                    <$FormGroup key="p.MyFirstModule.User_NewEdit.textBox1$formGroup"
                                        $widgetId="p.MyFirstModule.User_NewEdit.textBox1$formGroup"
                                        class={"mx-name-textBox1 mx-textbox"}
                                        control={[
                                            <$TextBox key="p.MyFirstModule.User_NewEdit.textBox1"
                                                $widgetId="p.MyFirstModule.User_NewEdit.textBox1"
                                                inputValue={AttributeProperty({
                                                    "scope": "p.MyFirstModule.User_NewEdit.dataView1",
                                                    "path": "",
                                                    "entity": "MyFirstModule.User",
                                                    "attribute": "FirstName",
                                                    "onChange": { "type": "doNothing", "argMap": {}, "config": {}, "disabledDuringExecution": false },
                                                    "isList": false,
                                                    "validation": null,
                                                    "formatting": { }
                                                })}
                                                isPassword={false}
                                                placeholder={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                mask={""}
                                                readOnlyStyle={"control"}
                                                maxLength={200}
                                                autocomplete={"on"}
                                                submitWhileEditing={false}
                                                submitDelay={300}
                                                id={DerivedUniqueIdProperty({
                                                    "widgetId": "p.MyFirstModule.User_NewEdit.textBox1"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "First name" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.MyFirstModule.User_NewEdit.textBox1"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.MyFirstModule.User_NewEdit.textBox1"
                                        })} />,
                                    <$FormGroup key="p.MyFirstModule.User_NewEdit.textBox2$formGroup"
                                        $widgetId="p.MyFirstModule.User_NewEdit.textBox2$formGroup"
                                        class={"mx-name-textBox2 mx-textbox"}
                                        control={[
                                            <$TextBox key="p.MyFirstModule.User_NewEdit.textBox2"
                                                $widgetId="p.MyFirstModule.User_NewEdit.textBox2"
                                                inputValue={AttributeProperty({
                                                    "scope": "p.MyFirstModule.User_NewEdit.dataView1",
                                                    "path": "",
                                                    "entity": "MyFirstModule.User",
                                                    "attribute": "LastName",
                                                    "onChange": { "type": "doNothing", "argMap": {}, "config": {}, "disabledDuringExecution": false },
                                                    "isList": false,
                                                    "validation": null,
                                                    "formatting": { }
                                                })}
                                                isPassword={false}
                                                placeholder={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                mask={""}
                                                readOnlyStyle={"control"}
                                                maxLength={200}
                                                autocomplete={"on"}
                                                submitWhileEditing={false}
                                                submitDelay={300}
                                                id={DerivedUniqueIdProperty({
                                                    "widgetId": "p.MyFirstModule.User_NewEdit.textBox2"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Last name" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.MyFirstModule.User_NewEdit.textBox2"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.MyFirstModule.User_NewEdit.textBox2"
                                        })} />,
                                    <$FormGroup key="p.MyFirstModule.User_NewEdit.textBox3$formGroup"
                                        $widgetId="p.MyFirstModule.User_NewEdit.textBox3$formGroup"
                                        class={"mx-name-textBox3 mx-textbox"}
                                        control={[
                                            <$TextBox key="p.MyFirstModule.User_NewEdit.textBox3"
                                                $widgetId="p.MyFirstModule.User_NewEdit.textBox3"
                                                inputValue={AttributeProperty({
                                                    "scope": "p.MyFirstModule.User_NewEdit.dataView1",
                                                    "path": "",
                                                    "entity": "MyFirstModule.User",
                                                    "attribute": "Email",
                                                    "onChange": { "type": "doNothing", "argMap": {}, "config": {}, "disabledDuringExecution": false },
                                                    "isList": false,
                                                    "validation": null,
                                                    "formatting": { }
                                                })}
                                                isPassword={false}
                                                placeholder={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                mask={""}
                                                readOnlyStyle={"control"}
                                                maxLength={200}
                                                autocomplete={"on"}
                                                submitWhileEditing={false}
                                                submitDelay={300}
                                                id={DerivedUniqueIdProperty({
                                                    "widgetId": "p.MyFirstModule.User_NewEdit.textBox3"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Email" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.MyFirstModule.User_NewEdit.textBox3"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.MyFirstModule.User_NewEdit.textBox3"
                                        })} />,
                                    <$FormGroup key="p.MyFirstModule.User_NewEdit.textBox4$formGroup"
                                        $widgetId="p.MyFirstModule.User_NewEdit.textBox4$formGroup"
                                        class={"mx-name-textBox4 mx-textbox"}
                                        control={[
                                            <$TextBox key="p.MyFirstModule.User_NewEdit.textBox4"
                                                $widgetId="p.MyFirstModule.User_NewEdit.textBox4"
                                                inputValue={AttributeProperty({
                                                    "scope": "p.MyFirstModule.User_NewEdit.dataView1",
                                                    "path": "",
                                                    "entity": "MyFirstModule.User",
                                                    "attribute": "PhoneNumber",
                                                    "onChange": { "type": "doNothing", "argMap": {}, "config": {}, "disabledDuringExecution": false },
                                                    "isList": false,
                                                    "validation": null,
                                                    "formatting": { }
                                                })}
                                                isPassword={false}
                                                placeholder={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                mask={""}
                                                readOnlyStyle={"control"}
                                                maxLength={200}
                                                autocomplete={"on"}
                                                submitWhileEditing={false}
                                                submitDelay={300}
                                                id={DerivedUniqueIdProperty({
                                                    "widgetId": "p.MyFirstModule.User_NewEdit.textBox4"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Phone number" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.MyFirstModule.User_NewEdit.textBox4"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.MyFirstModule.User_NewEdit.textBox4"
                                        })} />,
                                    <$FormGroup key="p.MyFirstModule.User_NewEdit.textBox5$formGroup"
                                        $widgetId="p.MyFirstModule.User_NewEdit.textBox5$formGroup"
                                        class={"mx-name-textBox5 mx-textbox"}
                                        control={[
                                            <$TextBox key="p.MyFirstModule.User_NewEdit.textBox5"
                                                $widgetId="p.MyFirstModule.User_NewEdit.textBox5"
                                                inputValue={AttributeProperty({
                                                    "scope": "p.MyFirstModule.User_NewEdit.dataView1",
                                                    "path": "",
                                                    "entity": "MyFirstModule.User",
                                                    "attribute": "Password",
                                                    "onChange": { "type": "doNothing", "argMap": {}, "config": {}, "disabledDuringExecution": false },
                                                    "isList": false,
                                                    "validation": null,
                                                    "formatting": { }
                                                })}
                                                isPassword={false}
                                                placeholder={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                mask={""}
                                                readOnlyStyle={"control"}
                                                maxLength={200}
                                                autocomplete={"on"}
                                                submitWhileEditing={false}
                                                submitDelay={300}
                                                id={DerivedUniqueIdProperty({
                                                    "widgetId": "p.MyFirstModule.User_NewEdit.textBox5"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Password" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.MyFirstModule.User_NewEdit.textBox5"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.MyFirstModule.User_NewEdit.textBox5"
                                        })} />
                                ]}
                                hideFooter={false}
                                footer={[
                                    <$ActionButton key="p.MyFirstModule.User_NewEdit.actionButton1"
                                        $widgetId="p.MyFirstModule.User_NewEdit.actionButton1"
                                        buttonId={"p.MyFirstModule.User_NewEdit.actionButton1"}
                                        class={"mx-name-actionButton1"}
                                        renderType={"button"}
                                        buttonClass={"btn-success"}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Save" }, "args": {} }
                                        })}
                                        tooltip={TextProperty({
                                            "value": ""
                                        })}
                                        action={ActionProperty({
                                            "action": { "type": "saveChanges", "argMap": { "$object": { "widget": "p.MyFirstModule.User_NewEdit.dataView1", "source": "object" } }, "config": { "operationId": "rPx7/JgK61aiht1PHPp3yg", "closePage": true }, "disabledDuringExecution": true },
                                            "abortOnServerValidation": true
                                        })} />,
                                    <$ActionButton key="p.MyFirstModule.User_NewEdit.actionButton2"
                                        $widgetId="p.MyFirstModule.User_NewEdit.actionButton2"
                                        buttonId={"p.MyFirstModule.User_NewEdit.actionButton2"}
                                        class={"mx-name-actionButton2"}
                                        renderType={"button"}
                                        buttonClass={"btn-default"}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Cancel" }, "args": {} }
                                        })}
                                        tooltip={TextProperty({
                                            "value": ""
                                        })}
                                        action={ActionProperty({
                                            "action": { "type": "cancelChanges", "argMap": {}, "config": { "operationId": "/XUg8ctNEFiJirSo+w3ekA", "closePage": true }, "disabledDuringExecution": true },
                                            "abortOnServerValidation": true
                                        })} />
                                ]} />
                        ]} />
                ]} />
        ]} />
]}</PageFragment>);

export const title = t([
    "Edit User"
]);

export const classes = "";

export const cancelChangesOperationId = "7Iyql02I41iibPEhHD4dKQ";
export const style = {};
export const content = { ...parentContent,
    "Atlas_Core.PopupLayout.Main": region$Main,
};
