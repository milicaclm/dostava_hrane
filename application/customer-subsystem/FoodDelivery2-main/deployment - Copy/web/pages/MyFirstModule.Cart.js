import { createElement } from "react";
const React = { createElement };

import { PageFragment } from "mendix/PageFragment";
import { ActionProperty } from "mendix/ActionProperty";
import { AssociationObjectListProperty } from "mendix/AssociationObjectListProperty";
import { AssociationObjectProperty } from "mendix/AssociationObjectProperty";
import { AttributeProperty } from "mendix/AttributeProperty";
import { DerivedUniqueIdProperty } from "mendix/DerivedUniqueIdProperty";
import { ExpressionProperty } from "mendix/ExpressionProperty";
import { TemplatedWidgetProperty } from "mendix/TemplatedWidgetProperty";
import { TextProperty } from "mendix/TextProperty";
import { ValidationProperty } from "mendix/ValidationProperty";

import { ActionButton } from "mendix/widgets/web/ActionButton";
import * as ComboboxWidgetModule from "C:/Users/Korisnik/Mendix/FoodDelivery2-main/deployment/web/widgets/com/mendix/widget/web/combobox/Combobox.mjs";
const Combobox = Object.getOwnPropertyDescriptor(ComboboxWidgetModule, "Combobox")?.value || Object.getOwnPropertyDescriptor(ComboboxWidgetModule, "default")?.value;   
import "C:/Users/Korisnik/Mendix/FoodDelivery2-main/deployment/web/widgets/com/mendix/widget/web/combobox/Combobox.css";
import { ConditionalVisibilityWrapper } from "mendix/widgets/web/ConditionalVisibilityWrapper";
import { DataView } from "mendix/widgets/web/DataView";
import { Div } from "mendix/widgets/web/Div";
import { FormGroup } from "mendix/widgets/web/FormGroup";
import { ListView } from "mendix/widgets/web/ListView";
import { Text } from "mendix/widgets/web/Text";
import { Title } from "mendix/widgets/web/Title";
import { addEnumerations, asPluginWidgets, t } from "mendix";

import { content as parentContent } from "../layouts/Atlas_Core.Atlas_Default.js";

const { $Div, $Title, $DataView, $ListView, $Text, $FormGroup, $Combobox, $ConditionalVisibilityWrapper, $ActionButton } = asPluginWidgets({ Div, Title, DataView, ListView, Text, FormGroup, Combobox, ConditionalVisibilityWrapper, ActionButton });

const region$Main = (historyId) => (<PageFragment renderKey={historyId}>{[
    <$Div key="p.MyFirstModule.Cart.layoutGrid1"
        $widgetId="p.MyFirstModule.Cart.layoutGrid1"
        class={"mx-name-layoutGrid1 mx-layoutgrid mx-layoutgrid-fluid container-fluid"}
        content={[
            <$Div key="p.MyFirstModule.Cart.layoutGrid1$row0"
                $widgetId="p.MyFirstModule.Cart.layoutGrid1$row0"
                class={"row"}
                content={[
                    <$Div key="p.MyFirstModule.Cart.layoutGrid1$row0$column0"
                        $widgetId="p.MyFirstModule.Cart.layoutGrid1$row0$column0"
                        class={"col-lg-12 col-md-12 col-12"}
                        content={[
                            <$Title key="p.MyFirstModule.Cart.Cart"
                                $widgetId="p.MyFirstModule.Cart.Cart"
                                class={"mx-name-Cart"}
                                caption={ExpressionProperty({
                                    "expression": { "expr": { "type": "variable", "variable": "pageTitle" }, "args": {} }
                                })} />,
                            <$DataView key="p.MyFirstModule.Cart.dataView1"
                                $widgetId="p.MyFirstModule.Cart.dataView1"
                                class={"mx-name-dataView1 form-horizontal"}
                                object={AssociationObjectProperty({
                                    "dataSourceId": "p.11",
                                    "scope": "$Order",
                                    "editable": true
                                })}
                                emptyMessage={TextProperty({
                                    "value": ""
                                })}
                                hideFooter={false}
                                footer={[
                                    <$ListView key="p.MyFirstModule.Cart.listView1"
                                        $widgetId="p.MyFirstModule.Cart.listView1"
                                        class={"mx-name-listView1"}
                                        listValue={AssociationObjectListProperty({
                                            "dataSourceId": "p.0",
                                            "entity": "MyFirstModule.ItemAPI",
                                            "scope": "p.MyFirstModule.Cart.dataView1",
                                            "operationId": "mSA3/DdsB1O9KzXLkH4/rQ"
                                        })}
                                        itemTemplate={TemplatedWidgetProperty({
                                            "dataSourceId": "p.0",
                                            "editable": false,
                                            "children": () => [
                                                <$Text key="p.MyFirstModule.Cart.text2"
                                                    $widgetId="p.MyFirstModule.Cart.text2"
                                                    class={"mx-name-text2"}
                                                    caption={ExpressionProperty({
                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "Name" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Cart.listView1", "source": "object" } } }
                                                    })}
                                                    renderMode={"h2"} />,
                                                <$Text key="p.MyFirstModule.Cart.text3"
                                                    $widgetId="p.MyFirstModule.Cart.text3"
                                                    class={"mx-name-text3"}
                                                    caption={ExpressionProperty({
                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "description" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Cart.listView1", "source": "object" } } }
                                                    })}
                                                    renderMode={"span"} />,
                                                <$Text key="p.MyFirstModule.Cart.text4"
                                                    $widgetId="p.MyFirstModule.Cart.text4"
                                                    class={"mx-name-text4"}
                                                    caption={ExpressionProperty({
                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "category" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Cart.listView1", "source": "object" } } }
                                                    })}
                                                    renderMode={"span"} />,
                                                <$Text key="p.MyFirstModule.Cart.text5"
                                                    $widgetId="p.MyFirstModule.Cart.text5"
                                                    class={"mx-name-text5"}
                                                    caption={ExpressionProperty({
                                                        "expression": { "expr": { "type": "function", "name": "_format", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "available" }, { "type": "literal", "value": "{}" } ] }, "args": { "currentObject": { "widget": "p.MyFirstModule.Cart.listView1", "source": "object" } } }
                                                    })}
                                                    renderMode={"span"} />,
                                                <$Text key="p.MyFirstModule.Cart.text6"
                                                    $widgetId="p.MyFirstModule.Cart.text6"
                                                    class={"mx-name-text6"}
                                                    caption={ExpressionProperty({
                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "imageUrl" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Cart.listView1", "source": "object" } } }
                                                    })}
                                                    renderMode={"span"} />,
                                                <$Text key="p.MyFirstModule.Cart.text7"
                                                    $widgetId="p.MyFirstModule.Cart.text7"
                                                    class={"mx-name-text7"}
                                                    caption={ExpressionProperty({
                                                        "expression": { "expr": { "type": "function", "name": "_format", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "price" }, { "type": "literal", "value": "{\"decimalPrecision\":2}" } ] }, "args": { "currentObject": { "widget": "p.MyFirstModule.Cart.listView1", "source": "object" } } }
                                                    })}
                                                    renderMode={"span"} />,
                                                <$Text key="p.MyFirstModule.Cart.text8"
                                                    $widgetId="p.MyFirstModule.Cart.text8"
                                                    class={"mx-name-text8"}
                                                    caption={ExpressionProperty({
                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "MyFirstModule.ItemAPI_RestaurantAPI/MyFirstModule.RestaurantAPI/name" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Cart.listView1", "source": "object" } } }
                                                    })}
                                                    renderMode={"span"} />,
                                                <$Text key="p.MyFirstModule.Cart.text9"
                                                    $widgetId="p.MyFirstModule.Cart.text9"
                                                    class={"mx-name-text9"}
                                                    caption={ExpressionProperty({
                                                        "expression": { "expr": { "type": "variable", "variable": "currentObject", "path": "MyFirstModule.ItemAPI_Order/MyFirstModule.Order/DriverAvailability" }, "args": { "currentObject": { "widget": "p.MyFirstModule.Cart.listView1", "source": "object" } } }
                                                    })}
                                                    renderMode={"span"} />
                                            ]
                                        })}
                                        pageSize={10} />
                                ]} />
                        ]} />
                ]} />
        ]} />,
    <$DataView key="p.MyFirstModule.Cart.dataView2"
        $widgetId="p.MyFirstModule.Cart.dataView2"
        class={"mx-name-dataView2 form-horizontal"}
        object={AssociationObjectProperty({
            "dataSourceId": "p.34",
            "scope": "$Order",
            "editable": true
        })}
        emptyMessage={TextProperty({
            "value": ""
        })}
        body={[
            <$Text key="p.MyFirstModule.Cart.TotalPrice"
                $widgetId="p.MyFirstModule.Cart.TotalPrice"
                class={"mx-name-TotalPrice text-capitalize"}
                caption={ExpressionProperty({
                    "expression": { "expr": { "type": "function", "name": "+", "parameters": [ { "type": "function", "name": "+", "parameters": [ { "type": "literal", "value": "Total: " }, { "type": "function", "name": "_format", "parameters": [ { "type": "variable", "variable": "currentObject", "path": "TotalPrice" }, { "type": "literal", "value": "{\"decimalPrecision\":2}" } ] } ] }, { "type": "literal", "value": " RSD" } ] }, "args": { "currentObject": { "widget": "p.MyFirstModule.Cart.dataView2", "source": "object" } } }
                })}
                renderMode={"h4"} />
        ]}
        hideFooter={false}
        footer={[
            <$Div key="p.MyFirstModule.Cart.layoutGrid4"
                $widgetId="p.MyFirstModule.Cart.layoutGrid4"
                class={"mx-name-layoutGrid4 mx-layoutgrid mx-layoutgrid-fluid container-fluid"}
                content={[
                    <$Div key="p.MyFirstModule.Cart.layoutGrid4$row0"
                        $widgetId="p.MyFirstModule.Cart.layoutGrid4$row0"
                        class={"row"}
                        content={[
                            <$Div key="p.MyFirstModule.Cart.layoutGrid4$row0$column0"
                                $widgetId="p.MyFirstModule.Cart.layoutGrid4$row0$column0"
                                class={"col-lg col-md col"}
                                content={[
                                    <$FormGroup key="p.MyFirstModule.Cart.comboBox1$formGroup"
                                        $widgetId="p.MyFirstModule.Cart.comboBox1$formGroup"
                                        class={"mx-name-comboBox1 pull-left spacing-outer-right-large spacing-outer-left-none spacing-inner-right-large spacing-inner-left-large"}
                                        control={[
                                            <$Combobox key="p.MyFirstModule.Cart.comboBox1"
                                                $widgetId="p.MyFirstModule.Cart.comboBox1"
                                                source={"context"}
                                                optionsSourceType={"enumeration"}
                                                attributeEnumeration={AttributeProperty({
                                                    "scope": "p.MyFirstModule.Cart.dataView2",
                                                    "path": "",
                                                    "entity": "MyFirstModule.Order",
                                                    "attribute": "PaymentMethod",
                                                    "onChange": { "type": "doNothing", "argMap": {}, "config": {}, "disabledDuringExecution": false },
                                                    "isList": false
                                                })}
                                                optionsSourceAssociationCaptionType={"attribute"}
                                                optionsSourceDatabaseCaptionType={"attribute"}
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
                                                readOnlyStyle={"text"}
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
                                                    "widgetId": "p.MyFirstModule.Cart.comboBox1"
                                                })} />
                                        ]}
                                        labelFor={DerivedUniqueIdProperty({
                                            "widgetId": "p.MyFirstModule.Cart.comboBox1"
                                        })}
                                        width={3}
                                        orientation={"vertical"}
                                        hasError={ValidationProperty({
                                            "inputWidgetId": "p.MyFirstModule.Cart.comboBox1"
                                        })} />
                                ]} />
                        ]} />,
                    <$Div key="p.MyFirstModule.Cart.layoutGrid4$row1"
                        $widgetId="p.MyFirstModule.Cart.layoutGrid4$row1"
                        class={"row"}
                        content={[
                            <$Div key="p.MyFirstModule.Cart.layoutGrid4$row1$column0"
                                $widgetId="p.MyFirstModule.Cart.layoutGrid4$row1$column0"
                                class={"col-lg col-md col"}
                                content={[
                                    <$ConditionalVisibilityWrapper key="p.MyFirstModule.Cart.actionButton1$visibility"
                                        $widgetId="p.MyFirstModule.Cart.actionButton1$visibility"
                                        visible={ExpressionProperty({
                                            "expression": { "expr": { "type": "function", "name": "_hasSomeRole", "parameters": [ { "type": "literal", "value": "Administrator" }, { "type": "literal", "value": "User" }, { "type": "literal", "value": "Korisnik" } ] }, "args": {} }
                                        })}
                                        contents={[
                                            <$ActionButton key="p.MyFirstModule.Cart.actionButton1"
                                                $widgetId="p.MyFirstModule.Cart.actionButton1"
                                                buttonId={"p.MyFirstModule.Cart.actionButton1"}
                                                class={"mx-name-actionButton1"}
                                                renderType={"button"}
                                                buttonClass={"btn-inverse"}
                                                caption={ExpressionProperty({
                                                    "expression": { "expr": { "type": "literal", "value": "Confirm Order" }, "args": {} }
                                                })}
                                                tooltip={TextProperty({
                                                    "value": ""
                                                })}
                                                action={ActionProperty({
                                                    "action": { "type": "callMicroflow", "argMap": { "Order": { "widget": "$Order", "source": "object" } }, "config": { "operationId": "eCVspiI6q1y4c+bjr/rNpQ", "validate": "view", "allowedRoles": [ "Administrator", "User", "Korisnik" ] }, "disabledDuringExecution": true },
                                                    "abortOnServerValidation": true
                                                })} />
                                        ]} />
                                ]} />
                        ]} />
                ]} />
        ]} />
]}</PageFragment>);

export const title = t([
    "Cart"
]);

export const classes = "layout-atlas layout-atlas-responsive-default";

export const style = {};
export const content = { ...parentContent,
    "Atlas_Core.Atlas_Default.Main": region$Main,
};
