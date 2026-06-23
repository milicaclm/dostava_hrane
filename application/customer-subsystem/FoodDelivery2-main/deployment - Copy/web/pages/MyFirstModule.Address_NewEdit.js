import { createElement } from "react";
const React = { createElement };

import { PageFragment } from "mendix/PageFragment";
import { ActionProperty } from "mendix/ActionProperty";
import { AssociationObjectProperty } from "mendix/AssociationObjectProperty";
import { AssociationProperty } from "mendix/AssociationProperty";
import { AttributeProperty } from "mendix/AttributeProperty";
import { DatabaseObjectListProperty } from "mendix/DatabaseObjectListProperty";
import { DerivedUniqueIdProperty } from "mendix/DerivedUniqueIdProperty";
import { ExpressionProperty } from "mendix/ExpressionProperty";
import { ListAttributeProperty } from "mendix/ListAttributeProperty";
import { TextProperty } from "mendix/TextProperty";
import { ValidationProperty } from "mendix/ValidationProperty";

import { ActionButton } from "mendix/widgets/web/ActionButton";
import * as ComboboxWidgetModule from "C:/Users/Korisnik/Mendix/FoodDelivery2-main/deployment/web/widgets/com/mendix/widget/web/combobox/Combobox.mjs";
const Combobox = Object.getOwnPropertyDescriptor(ComboboxWidgetModule, "Combobox")?.value || Object.getOwnPropertyDescriptor(ComboboxWidgetModule, "default")?.value;   
import "C:/Users/Korisnik/Mendix/FoodDelivery2-main/deployment/web/widgets/com/mendix/widget/web/combobox/Combobox.css";
import { DataView } from "mendix/widgets/web/DataView";
import { Div } from "mendix/widgets/web/Div";
import { FormGroup } from "mendix/widgets/web/FormGroup";
import { TextBox } from "mendix/widgets/web/TextBox";
import { addEnumerations, asPluginWidgets, t } from "mendix";

import { content as parentContent } from "../layouts/Atlas_Core.PopupLayout.js";

const { $Div, $DataView, $FormGroup, $TextBox, $Combobox, $ActionButton } = asPluginWidgets({ Div, DataView, FormGroup, TextBox, Combobox, ActionButton });

const region$Main = (historyId) => (<PageFragment renderKey={historyId}>{[
    <$Div key="p.MyFirstModule.Address_NewEdit.layoutGrid1"
        $widgetId="p.MyFirstModule.Address_NewEdit.layoutGrid1"
        class={"mx-name-layoutGrid1 mx-layoutgrid mx-layoutgrid-fluid container-fluid"}
        content={[
            <$Div key="p.MyFirstModule.Address_NewEdit.layoutGrid1$row0"
                $widgetId="p.MyFirstModule.Address_NewEdit.layoutGrid1$row0"
                class={"row"}
                content={[
                    <$Div key="p.MyFirstModule.Address_NewEdit.layoutGrid1$row0$column0"
                        $widgetId="p.MyFirstModule.Address_NewEdit.layoutGrid1$row0$column0"
                        class={"col-lg col-md col"}
                        content={[
                            <$DataView key="p.MyFirstModule.Address_NewEdit.dataView1"
                                $widgetId="p.MyFirstModule.Address_NewEdit.dataView1"
                                class={"mx-name-dataView1 form-horizontal"}
                                object={AssociationObjectProperty({
                                    "dataSourceId": "p.13",
                                    "scope": "$Address",
                                    "editable": true
                                })}
                                emptyMessage={TextProperty({
                                    "value": ""
                                })}
                                body={[
                                    <$FormGroup key="p.MyFirstModule.Address_NewEdit.textBox1$formGroup"
                                        $widgetId="p.MyFirstModule.Address_NewEdit.textBox1$formGroup"
                                        class={"mx-name-textBox1 mx-textbox"}
                                        control={[
                                            <$TextBox key="p.MyFirstModule.Address_NewEdit.textBox1"
                                                $widgetId="p.MyFirstModule.Address_NewEdit.textBox1"
                                                inputValue={AttributeProperty({
                                                    "scope": "p.MyFirstModule.Address_NewEdit.dataView1",
                                                    "path": "",
                                                    "entity": "MyFirstModule.Address",
                                                    "attribute": "City",
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
                                                    "widgetId": "p.MyFirstModule.Address_NewEdit.textBox1"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "City" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.MyFirstModule.Address_NewEdit.textBox1"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.MyFirstModule.Address_NewEdit.textBox1"
                                        })} />,
                                    <$FormGroup key="p.MyFirstModule.Address_NewEdit.textBox2$formGroup"
                                        $widgetId="p.MyFirstModule.Address_NewEdit.textBox2$formGroup"
                                        class={"mx-name-textBox2 mx-textbox"}
                                        control={[
                                            <$TextBox key="p.MyFirstModule.Address_NewEdit.textBox2"
                                                $widgetId="p.MyFirstModule.Address_NewEdit.textBox2"
                                                inputValue={AttributeProperty({
                                                    "scope": "p.MyFirstModule.Address_NewEdit.dataView1",
                                                    "path": "",
                                                    "entity": "MyFirstModule.Address",
                                                    "attribute": "Street",
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
                                                    "widgetId": "p.MyFirstModule.Address_NewEdit.textBox2"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Street" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.MyFirstModule.Address_NewEdit.textBox2"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.MyFirstModule.Address_NewEdit.textBox2"
                                        })} />,
                                    <$FormGroup key="p.MyFirstModule.Address_NewEdit.textBox3$formGroup"
                                        $widgetId="p.MyFirstModule.Address_NewEdit.textBox3$formGroup"
                                        class={"mx-name-textBox3 mx-textbox"}
                                        control={[
                                            <$TextBox key="p.MyFirstModule.Address_NewEdit.textBox3"
                                                $widgetId="p.MyFirstModule.Address_NewEdit.textBox3"
                                                inputValue={AttributeProperty({
                                                    "scope": "p.MyFirstModule.Address_NewEdit.dataView1",
                                                    "path": "",
                                                    "entity": "MyFirstModule.Address",
                                                    "attribute": "StreetNumber",
                                                    "onChange": { "type": "doNothing", "argMap": {}, "config": {}, "disabledDuringExecution": false },
                                                    "isList": false,
                                                    "validation": null,
                                                    "formatting": {
                                                        "numberFormat": {
                                                            "groupDigits": false
                                                        }
                                                    }
                                                })}
                                                isPassword={false}
                                                placeholder={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                mask={""}
                                                readOnlyStyle={"control"}
                                                autocomplete={"on"}
                                                submitWhileEditing={false}
                                                submitDelay={300}
                                                id={DerivedUniqueIdProperty({
                                                    "widgetId": "p.MyFirstModule.Address_NewEdit.textBox3"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "Street number" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.MyFirstModule.Address_NewEdit.textBox3"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.MyFirstModule.Address_NewEdit.textBox3"
                                        })} />,
                                    <$FormGroup key="p.MyFirstModule.Address_NewEdit.comboBox1$formGroup"
                                        $widgetId="p.MyFirstModule.Address_NewEdit.comboBox1$formGroup"
                                        class={"mx-name-comboBox1"}
                                        control={[
                                            <$Combobox key="p.MyFirstModule.Address_NewEdit.comboBox1"
                                                $widgetId="p.MyFirstModule.Address_NewEdit.comboBox1"
                                                source={"context"}
                                                optionsSourceType={"association"}
                                                optionsSourceAssociationCaptionType={"attribute"}
                                                optionsSourceDatabaseCaptionType={"attribute"}
                                                optionsSourceAssociationCaptionAttribute={ListAttributeProperty({
                                                    "path": "",
                                                    "entity": "MyFirstModule.User",
                                                    "attribute": "FirstName",
                                                    "attributeType": "String",
                                                    "sortable": true,
                                                    "filterable": true,
                                                    "dataSourceId": "p.0",
                                                    "isList": false
                                                })}
                                                attributeAssociation={AssociationProperty({
                                                    "type": "Reference",
                                                    "entity": "MyFirstModule.Address",
                                                    "path": "",
                                                    "attribute": "MyFirstModule.Address_User",
                                                    "endpointEntity": "MyFirstModule.User",
                                                    "selectableObjectsId": "p.0",
                                                    "scope": "p.MyFirstModule.Address_NewEdit.dataView1",
                                                    "onChange": { "type": "doNothing", "argMap": {}, "config": {}, "disabledDuringExecution": false }
                                                })}
                                                optionsSourceAssociationDataSource={DatabaseObjectListProperty({
                                                    "dataSourceId": "p.0",
                                                    "entity": "MyFirstModule.User",
                                                    "scope": "p.MyFirstModule.Address_NewEdit.dataView1",
                                                    "operationId": "w8QVuiT53FWbN3ydm68JlA",
                                                    "sort": []
                                                })}
                                                optionsSourceStaticDataSource={[]}
                                                emptyOptionText={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                noOptionsText={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "" }, "args": {} }
                                                })}
                                                clearable={true}
                                                optionsSourceAssociationCustomContentType={"no"}
                                                optionsSourceDatabaseCustomContentType={"no"}
                                                staticDataSourceCustomContentType={"no"}
                                                showFooter={false}
                                                selectionMethod={"checkbox"}
                                                selectedItemsStyle={"text"}
                                                selectAllButton={false}
                                                selectAllButtonCaption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Select all" }, "args": {} }
                                                })}
                                                customEditability={"default"}
                                                customEditabilityExpression={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": false }, "args": {} }
                                                })}
                                                readOnlyStyle={"bordered"}
                                                ariaRequired={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": false }, "args": {} }
                                                })}
                                                ariaLabel={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Combo box" }, "args": {} }
                                                })}
                                                clearButtonAriaLabel={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Clear selection" }, "args": {} }
                                                })}
                                                removeValueAriaLabel={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Remove value" }, "args": {} }
                                                })}
                                                a11ySelectedValue={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Selected value:" }, "args": {} }
                                                })}
                                                a11yOptionsAvailable={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Number of options available:" }, "args": {} }
                                                })}
                                                a11yInstructions={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Use up and down arrow keys to navigate. Press Enter or Space Bar keys to select." }, "args": {} }
                                                })}
                                                lazyLoading={true}
                                                loadingType={"spinner"}
                                                selectedItemsSorting={"none"}
                                                filterType={"contains"}
                                                id={DerivedUniqueIdProperty({
                                                    "widgetId": "p.MyFirstModule.Address_NewEdit.comboBox1"
                                                })} />
                                        ]}
                                        caption={ExpressionProperty({
                                            "expression": { "expr": { "type": "literal", "value": "User" }, "args": {} }
                                        })}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.MyFirstModule.Address_NewEdit.comboBox1"
                                        })}
                                        width={3}
                                        orientation={"horizontal"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.MyFirstModule.Address_NewEdit.comboBox1"
                                        })} />
                                ]}
                                hideFooter={false}
                                footer={[
                                    <$ActionButton key="p.MyFirstModule.Address_NewEdit.actionButton1"
                                        $widgetId="p.MyFirstModule.Address_NewEdit.actionButton1"
                                        buttonId={"p.MyFirstModule.Address_NewEdit.actionButton1"}
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
                                            "action": { "type": "saveChanges", "argMap": { "$object": { "widget": "p.MyFirstModule.Address_NewEdit.dataView1", "source": "object" } }, "config": { "operationId": "STcfWcQWslqxDyktPhrGGQ", "closePage": true }, "disabledDuringExecution": true },
                                            "abortOnServerValidation": true
                                        })} />,
                                    <$ActionButton key="p.MyFirstModule.Address_NewEdit.actionButton2"
                                        $widgetId="p.MyFirstModule.Address_NewEdit.actionButton2"
                                        buttonId={"p.MyFirstModule.Address_NewEdit.actionButton2"}
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
                                            "action": { "type": "cancelChanges", "argMap": {}, "config": { "operationId": "S/8PaW+SN1CBGq3kWn8k3Q", "closePage": true }, "disabledDuringExecution": true },
                                            "abortOnServerValidation": true
                                        })} />
                                ]} />
                        ]} />
                ]} />
        ]} />
]}</PageFragment>);

export const title = t([
    "Edit Address"
]);

export const classes = "";

export const cancelChangesOperationId = "8b87D2y+Pl+uoQtc4gLCnw";
export const style = {};
export const content = { ...parentContent,
    "Atlas_Core.PopupLayout.Main": region$Main,
};
