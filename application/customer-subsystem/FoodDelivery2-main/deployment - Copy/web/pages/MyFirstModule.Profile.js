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
import { Title } from "mendix/widgets/web/Title";
import { addEnumerations, asPluginWidgets, t } from "mendix";

import { content as parentContent } from "../layouts/Atlas_Core.Atlas_Default.js";

const { $Div, $Title, $DataView, $FormGroup, $TextBox, $ConditionalVisibilityWrapper, $ActionButton } = asPluginWidgets({ Div, Title, DataView, FormGroup, TextBox, ConditionalVisibilityWrapper, ActionButton });

const region$Main = (historyId) => (<PageFragment renderKey={historyId}>{[
    <$Div key="p.MyFirstModule.Profile.layoutGrid2"
        $widgetId="p.MyFirstModule.Profile.layoutGrid2"
        class={"mx-name-layoutGrid2 mx-layoutgrid mx-layoutgrid-fluid container-fluid"}
        content={[
            <$Div key="p.MyFirstModule.Profile.layoutGrid2$row0"
                $widgetId="p.MyFirstModule.Profile.layoutGrid2$row0"
                class={"row"}
                content={[
                    <$Div key="p.MyFirstModule.Profile.layoutGrid2$row0$column0"
                        $widgetId="p.MyFirstModule.Profile.layoutGrid2$row0$column0"
                        class={"col-lg col-md col"}
                        content={[
                            <$Title key="p.MyFirstModule.Profile.pageTitle1"
                                $widgetId="p.MyFirstModule.Profile.pageTitle1"
                                class={"mx-name-pageTitle1"}
                                caption={ExpressionProperty({
                                    "expression": { "expr": { "type": "variable", "variable": "pageTitle" }, "args": {} }
                                })} />
                        ]} />
                ]} />
        ]} />,
    <$Div key="p.MyFirstModule.Profile.layoutGrid1"
        $widgetId="p.MyFirstModule.Profile.layoutGrid1"
        class={"mx-name-layoutGrid1 mx-layoutgrid mx-layoutgrid-fluid container-fluid"}
        content={[
            <$Div key="p.MyFirstModule.Profile.layoutGrid1$row0"
                $widgetId="p.MyFirstModule.Profile.layoutGrid1$row0"
                class={"row"}
                content={[
                    <$Div key="p.MyFirstModule.Profile.layoutGrid1$row0$column0"
                        $widgetId="p.MyFirstModule.Profile.layoutGrid1$row0$column0"
                        class={"col-lg-12 col-md-12 col-12"}
                        content={[
                            <$DataView key="p.MyFirstModule.Profile.dataView1"
                                $widgetId="p.MyFirstModule.Profile.dataView1"
                                class={"mx-name-dataView1 form-horizontal"}
                                object={AssociationObjectProperty({
                                    "dataSourceId": "p.18",
                                    "scope": "$User",
                                    "editable": true
                                })}
                                emptyMessage={TextProperty({
                                    "value": ""
                                })}
                                body={[
                                    <$FormGroup key="p.MyFirstModule.Profile.textBox1$formGroup"
                                        $widgetId="p.MyFirstModule.Profile.textBox1$formGroup"
                                        class={"mx-name-textBox1 mx-textbox"}
                                        control={[
                                            <$TextBox key="p.MyFirstModule.Profile.textBox1"
                                                $widgetId="p.MyFirstModule.Profile.textBox1"
                                                inputValue={AttributeProperty({
                                                    "scope": "p.MyFirstModule.Profile.dataView1",
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
                                                    "widgetId": "p.MyFirstModule.Profile.textBox1"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "First name" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.MyFirstModule.Profile.textBox1"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.MyFirstModule.Profile.textBox1"
                                        })} />,
                                    <$FormGroup key="p.MyFirstModule.Profile.textBox2$formGroup"
                                        $widgetId="p.MyFirstModule.Profile.textBox2$formGroup"
                                        class={"mx-name-textBox2 mx-textbox"}
                                        control={[
                                            <$TextBox key="p.MyFirstModule.Profile.textBox2"
                                                $widgetId="p.MyFirstModule.Profile.textBox2"
                                                inputValue={AttributeProperty({
                                                    "scope": "p.MyFirstModule.Profile.dataView1",
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
                                                    "widgetId": "p.MyFirstModule.Profile.textBox2"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Last name" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.MyFirstModule.Profile.textBox2"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.MyFirstModule.Profile.textBox2"
                                        })} />,
                                    <$FormGroup key="p.MyFirstModule.Profile.textBox3$formGroup"
                                        $widgetId="p.MyFirstModule.Profile.textBox3$formGroup"
                                        class={"mx-name-textBox3 mx-textbox"}
                                        control={[
                                            <$TextBox key="p.MyFirstModule.Profile.textBox3"
                                                $widgetId="p.MyFirstModule.Profile.textBox3"
                                                inputValue={AttributeProperty({
                                                    "scope": "p.MyFirstModule.Profile.dataView1",
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
                                                    "widgetId": "p.MyFirstModule.Profile.textBox3"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Email" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.MyFirstModule.Profile.textBox3"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.MyFirstModule.Profile.textBox3"
                                        })} />,
                                    <$FormGroup key="p.MyFirstModule.Profile.textBox4$formGroup"
                                        $widgetId="p.MyFirstModule.Profile.textBox4$formGroup"
                                        class={"mx-name-textBox4 mx-textbox"}
                                        control={[
                                            <$TextBox key="p.MyFirstModule.Profile.textBox4"
                                                $widgetId="p.MyFirstModule.Profile.textBox4"
                                                inputValue={AttributeProperty({
                                                    "scope": "p.MyFirstModule.Profile.dataView1",
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
                                                    "widgetId": "p.MyFirstModule.Profile.textBox4"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Phone number" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.MyFirstModule.Profile.textBox4"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.MyFirstModule.Profile.textBox4"
                                        })} />
                                ]}
                                hideFooter={false}
                                footer={[
                                    <$ConditionalVisibilityWrapper key="p.MyFirstModule.Profile.actionButton1$visibility"
                                        $widgetId="p.MyFirstModule.Profile.actionButton1$visibility"
                                        visible={ExpressionProperty({
                                            "expression": { "expr": { "type": "function", "name": "_hasSomeRole", "parameters": [ { "type": "literal", "value": "Korisnik" } ] }, "args": {} }
                                        })}
                                        contents={[
                                            <$ActionButton key="p.MyFirstModule.Profile.actionButton1"
                                                $widgetId="p.MyFirstModule.Profile.actionButton1"
                                                buttonId={"p.MyFirstModule.Profile.actionButton1"}
                                                class={"mx-name-actionButton1"}
                                                renderType={"button"}
                                                buttonClass={"btn-inverse"}
                                                caption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Edit Profile" }, "args": {} }
                                                })}
                                                tooltip={TextProperty({
                                                    "value": ""
                                                })}
                                                action={ActionProperty({
                                                    "action": { "type": "openPage", "argMap": { "param$User": { "widget": "$User", "source": "object" } }, "config": { "name": "MyFirstModule/User_NewEdit.page.xml", "location": "modal", "resizable": true, "allowedRoles": [ "Korisnik" ] }, "disabledDuringExecution": true },
                                                    "abortOnServerValidation": true
                                                })} />
                                        ]} />
                                ]} />
                        ]} />
                ]} />
        ]} />
]}</PageFragment>);

export const title = t([
    "Profile"
]);

export const classes = "layout-atlas layout-atlas-responsive-default";

export const style = {};
export const content = { ...parentContent,
    "Atlas_Core.Atlas_Default.Main": region$Main,
};
